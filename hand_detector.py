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
        Count the number of extended fingers with improved accuracy.
        
        Args:
            landmark_list: List of landmark positions from get_finger_positions()
            
        Returns:
            Number of extended fingers (0-5)
        """
        if len(landmark_list) == 0:
            return -1
        
        fingers_up = []  # Store which fingers are up for better validation
        
        # Get palm base for reference (middle point between wrist and middle MCP)
        wrist_y = landmark_list[0][2]
        middle_mcp_y = landmark_list[9][2]
        palm_base_y = (wrist_y + middle_mcp_y) / 2
        
        # THUMB - Special handling for thumb (much stricter to avoid false positives)
        thumb_tip_x = landmark_list[4][1]
        thumb_tip_y = landmark_list[4][2]
        thumb_ip_x = landmark_list[3][1]
        thumb_mcp_x = landmark_list[2][1]
        wrist_x = landmark_list[0][1]
        index_mcp_x = landmark_list[5][1]
        
        # Calculate if thumb is extended horizontally (for right hand)
        # Thumb tip should be far from index finger MCP
        thumb_to_index_dist = abs(thumb_tip_x - index_mcp_x)
        palm_width = abs(index_mcp_x - wrist_x)
        
        # Thumb is extended ONLY if:
        # 1. Tip is FAR from index finger (more than 80% of palm width)
        # 2. Thumb tip is beyond thumb MCP horizontally
        # 3. Tip Y position is above palm base (not curled down)
        thumb_extended_horizontally = abs(thumb_tip_x - thumb_mcp_x) > palm_width * 0.5
        
        if thumb_to_index_dist > palm_width * 0.8 and thumb_extended_horizontally and thumb_tip_y < palm_base_y + 30:
            fingers_up.append("thumb")
        
        # OTHER 4 FINGERS - Use both PIP and MCP for better accuracy
        finger_names = ["index", "middle", "ring", "pinky"]
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
        finger_pips = [6, 10, 14, 18]  # PIP joints
        finger_mcps = [5, 9, 13, 17]   # MCP (knuckle) joints
        
        for i in range(4):
            tip_y = landmark_list[finger_tips[i]][2]
            pip_y = landmark_list[finger_pips[i]][2]
            mcp_y = landmark_list[finger_mcps[i]][2]
            
            # Finger is extended if:
            # 1. Tip is significantly above PIP (at least 25 pixels - slightly reduced)
            # 2. PIP is above or near MCP (finger is straight)
            tip_pip_diff = pip_y - tip_y
            pip_mcp_diff = mcp_y - pip_y
            
            if tip_pip_diff > 25 and pip_mcp_diff > -15:
                fingers_up.append(finger_names[i])
        
        return len(fingers_up)
    
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
        
        # Strict gesture classification to avoid confusion
        if finger_count == 5:  # Exactly 5 fingers = open palm (PAUSE)
            gesture = "OPEN_PALM"
        elif finger_count == 4:  # Exactly 4 fingers (no thumb) = SHUTDOWN
            gesture = "FOUR_FINGERS"
        elif finger_count == 0:  # Exactly 0 fingers = closed fist (PLAY)
            gesture = "CLOSED_FIST"
        elif finger_count == 1:  # 1 finger also counts as closed fist
            gesture = "CLOSED_FIST"
        elif finger_count == 2:  # Exactly 2 fingers = peace sign (REWIND)
            gesture = "PEACE_SIGN"
        elif finger_count == 3:  # Exactly 3 fingers = forward sign
            gesture = "THREE_FINGERS"
        else:
            gesture = "UNKNOWN"
        
        return gesture, finger_count, img
    
    def close(self):
        """Release resources."""
        self.hands.close()
