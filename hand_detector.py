import cv2
import mediapipe as mp
import math


class HandDetector:
    """
    Hand detection and gesture recognition using MediaPipe.
    Detects open palm (5 fingers) and closed fist (0 fingers).
    """
    
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        """
        Initialize the hand detector.
        
        Args:
            max_hands: Maximum number of hands to detect
            detection_confidence: Minimum confidence for hand detection
            tracking_confidence: Minimum confidence for hand tracking
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips
        self.finger_pips = [2, 6, 10, 14, 18]  # PIP joints for comparison
        
    def find_hands(self, img, draw=True):
        """
        Detect hands in the image and optionally draw landmarks.
        
        Args:
            img: Input image (BGR format)
            draw: Whether to draw hand landmarks on the image
            
        Returns:
            Processed image with landmarks (if draw=True)
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        return img
    
    def get_finger_positions(self, img):
        """
        Get the positions of all hand landmarks.
        
        Args:
            img: Input image
            
        Returns:
            List of landmark positions [(id, x, y), ...]
        """
        landmark_list = []
        
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]  # Get first hand
            h, w, c = img.shape
            
            for id, lm in enumerate(hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append((id, cx, cy))
        
        return landmark_list
    
    def count_fingers(self, landmark_list):
        """
        Count the number of extended fingers.
        
        Args:
            landmark_list: List of landmark positions from get_finger_positions()
            
        Returns:
            Number of extended fingers (0-5)
        """
        if len(landmark_list) == 0:
            return -1
        
        fingers_up = 0
        
        # THUMB - Compare with wrist
        thumb_tip_x = landmark_list[4][1]
        wrist_x = landmark_list[0][1]
        index_mcp_x = landmark_list[5][1]
        
        # Thumb is extended if it's far from palm center
        if abs(thumb_tip_x - wrist_x) > abs(index_mcp_x - wrist_x) * 0.5:
            fingers_up += 1
        
        # OTHER 4 FINGERS - Compare tip with MCP (knuckle base)
        # Using MCP instead of PIP for more reliable detection
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
        finger_mcps = [5, 9, 13, 17]   # Their MCP (knuckle) joints
        
        for i in range(4):
            tip_y = landmark_list[finger_tips[i]][2]
            mcp_y = landmark_list[finger_mcps[i]][2]
            
            # Finger is extended if tip is significantly ABOVE (lower Y than) the knuckle
            # Larger threshold for more reliable detection
            if tip_y < mcp_y - 40:
                fingers_up += 1
        
        return fingers_up
    
    def detect_gesture(self, img):
        """
        Detect hand gesture: open palm (5 fingers) or closed fist (0 fingers).
        
        Args:
            img: Input image
            
        Returns:
            Tuple of (gesture_name, finger_count, processed_image)
            gesture_name: "OPEN_PALM", "CLOSED_FIST", or "UNKNOWN"
        """
        img = self.find_hands(img, draw=True)
        landmarks = self.get_finger_positions(img)
        
        if len(landmarks) == 0:
            return "NO_HAND", -1, img
        
        finger_count = self.count_fingers(landmarks)
        
        # DEBUG: Print finger count to console
        print(f"[DEBUG] Finger count: {finger_count}", end=" | ")
        
        # Make detection more forgiving
        if finger_count >= 4:  # 4 or 5 fingers = open palm
            gesture = "OPEN_PALM"
            print("Gesture: OPEN_PALM", end=" ")
        elif finger_count <= 1:  # 0 or 1 finger = closed fist
            gesture = "CLOSED_FIST"
            print("Gesture: CLOSED_FIST", end=" ")
        else:
            gesture = "UNKNOWN"
            print("Gesture: UNKNOWN", end=" ")
        
        return gesture, finger_count, img
    
    def close(self):
        """Release resources."""
        self.hands.close()
