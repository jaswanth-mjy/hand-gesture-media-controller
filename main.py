#!/usr/bin/env python3
"""
Pause or Play - Hand Gesture Media Controller
Controls media playback using hand gestures detected through webcam.

Gestures:
- Open palm (5 fingers) = PLAY
- Closed fist (0 fingers) = PAUSE

Press 'q' to quit the application.
"""

import cv2
import sys
from hand_detector import HandDetector
from media_controller import MediaController


def main():
    """Main application loop."""
    
    # Initialize components
    print("=" * 60)
    print("🎬 PAUSE OR PLAY - Hand Gesture Media Controller")
    print("=" * 60)
    print("\nInitializing camera and hand detection...")
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam!")
        print("Please check if your camera is connected and not being used by another application.")
        return
    
    print("✅ Camera initialized")
    
    # Initialize hand detector and media controller
    detector = HandDetector(max_hands=1, detection_confidence=0.7, tracking_confidence=0.7)
    controller = MediaController(cooldown=2.5)  # 2.5 second cooldown between commands
    
    print("✅ Hand detector initialized")
    print("✅ Media controller initialized")
    print("\n" + "=" * 70)
    print("GESTURES & CONTROLS:")
    print("  ✊ CLOSED FIST (0-1 fingers)    → PLAY ▶")
    print("  👋 OPEN PALM (4-5 fingers)     → PAUSE ⏸")
    print("  ✌️  PEACE SIGN (2 fingers)      → REWIND 10s ⏪")
    print("  🤟 THREE FINGERS (3 fingers)   → FORWARD 10s ⏩")
    print("\n  Press 'Q' to quit")
    print("=" * 70 + "\n")
    
    # State tracking
    last_gesture = None
    gesture_stable_frames = 0
    stability_threshold = 12  # Number of consecutive frames needed to confirm gesture (increased for accuracy)
    command_executed_for_current_gesture = False  # Prevent repeat commands
    
    while True:
        # Read frame from camera
        success, img = cap.read()
        
        if not success:
            print("❌ Error: Could not read frame from camera!")
            break
        
        # Flip the image horizontally for a mirror view
        img = cv2.flip(img, 1)
        
        # Detect hand gesture
        gesture, finger_count, img = detector.detect_gesture(img)
        
        # Track gesture stability
        if gesture == last_gesture:
            gesture_stable_frames += 1
        else:
            gesture_stable_frames = 0
            last_gesture = gesture
            command_executed_for_current_gesture = False  # Reset when gesture changes
        
        # Debug output - print finger count for troubleshooting
        if finger_count >= 0:
            gesture_display = f"{gesture} ({finger_count}F)"
            confidence = "✓" if gesture_stable_frames >= stability_threshold else "..."
            print(f"Detection: {gesture_display:25} | Stable: {gesture_stable_frames:2}/{stability_threshold} {confidence} | State: {controller.current_state or 'UNKNOWN':8}", end='\r')
        
        # Execute command ONCE when gesture is stable and command not yet executed
        if gesture_stable_frames >= stability_threshold and not command_executed_for_current_gesture:
            if gesture == "CLOSED_FIST" and controller.current_state != "PLAYING":
                # CLOSED FIST = PLAY (if video is NOT already playing)
                if controller.play():
                    print("\n✅ PLAY command sent - Closed fist detected")
                    command_executed_for_current_gesture = True
            elif gesture == "OPEN_PALM" and controller.current_state != "PAUSED":
                # OPEN PALM = PAUSE (if video is NOT already paused)
                if controller.pause():
                    print("\n✅ PAUSE command sent - Open palm detected")
                    command_executed_for_current_gesture = True
            elif gesture == "PEACE_SIGN":
                # PEACE SIGN (2 fingers) = REWIND 10 seconds
                if controller.skip_backward():
                    print("\n⏪ REWIND 10 seconds - Peace sign detected")
                    command_executed_for_current_gesture = True
            elif gesture == "THREE_FINGERS":
                # THREE FINGERS = FORWARD 10 seconds
                if controller.skip_forward():
                    print("\n⏩ FORWARD 10 seconds - Three fingers detected")
                    command_executed_for_current_gesture = True
        
        # Display information on screen
        h, w, c = img.shape
        
        # Background for text (increased height for finger indicator)
        cv2.rectangle(img, (10, 10), (w - 10, 200), (0, 0, 0), -1)
        cv2.rectangle(img, (10, 10), (w - 10, 200), (255, 255, 255), 2)
        
        # Display gesture and finger count
        if gesture == "NO_HAND":
            text = "NO HAND DETECTED"
            color = (0, 165, 255)  # Orange
        elif gesture == "OPEN_PALM":
            text = f"OPEN PALM ({finger_count} fingers) - PAUSE ⏸"
            color = (0, 255, 0)  # Green
        elif gesture == "CLOSED_FIST":
            text = f"CLOSED FIST ({finger_count} fingers) - PLAY ▶"
            color = (0, 0, 255)  # Red
        elif gesture == "PEACE_SIGN":
            text = f"PEACE SIGN ({finger_count} fingers) - REWIND ⏪"
            color = (255, 0, 255)  # Magenta
        elif gesture == "THREE_FINGERS":
            text = f"THREE FINGERS ({finger_count} fingers) - FORWARD ⏩"
            color = (255, 255, 0)  # Yellow
        else:
            text = f"UNKNOWN GESTURE ({finger_count} fingers)"
            color = (128, 128, 128)  # Gray
        
        cv2.putText(img, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.9, color, 2, cv2.LINE_AA)
        
        # Display finger count with visual indicator
        if finger_count >= 0:
            finger_text = f"Fingers Detected: {finger_count}"
            cv2.putText(img, finger_text, (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Visual finger indicator
            finger_indicator = "○ " * finger_count + "● " * (5 - finger_count)
            cv2.putText(img, finger_indicator, (20, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 255), 1, cv2.LINE_AA)
        
        # Display state
        state_text = f"State: {controller.current_state if controller.current_state else 'UNKNOWN'}"
        cv2.putText(img, state_text, (20, 125),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Display stability indicator
        stability_text = f"Stability: {gesture_stable_frames}/{stability_threshold}"
        stability_color = (0, 255, 0) if gesture_stable_frames >= stability_threshold else (100, 100, 100)
        cv2.putText(img, stability_text, (w - 300, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, stability_color, 2, cv2.LINE_AA)
        
        # Display gesture guide at bottom
        guide_y = h - 80
        cv2.rectangle(img, (10, guide_y - 10), (w - 10, h - 10), (0, 0, 0), -1)
        cv2.rectangle(img, (10, guide_y - 10), (w - 10, h - 10), (255, 255, 255), 1)
        cv2.putText(img, "Gestures: Fist=Play | Palm=Pause | 2 Fingers=Rewind | 3 Fingers=Forward | Q=Quit", 
                    (20, guide_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)
        
        # Show the frame
        cv2.imshow("Pause or Play - Hand Gesture Control", img)
        
        # Check for quit command
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print("\n👋 Exiting application...")
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    detector.close()
    print("✅ Application closed successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Application interrupted by user (Ctrl+C)")
        cv2.destroyAllWindows()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        cv2.destroyAllWindows()
        sys.exit(1)
