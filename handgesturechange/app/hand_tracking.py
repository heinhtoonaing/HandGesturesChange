import cv2
import time
import mediapipe as mp
from utils.gesture_recognition import GestureTracker  # Make sure to import GestureTracker

class HandTracker:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, track_confidence=0.5):
        """
        Initializes the HandTracker with MediaPipe Hands.

        Args:
            mode (bool): Whether to treat the input images as a video stream.
            max_hands (int): Maximum number of hands to detect.
            detection_confidence (float): Minimum confidence value ([0.0, 1.0]) for hand detection.
            track_confidence (float): Minimum confidence value ([0.0, 1.0]) for hand tracking.
        """
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=mode,
                                        max_num_hands=max_hands,
                                        min_detection_confidence=detection_confidence,
                                        min_tracking_confidence=track_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.gesture_tracker = GestureTracker()  # Initialize gesture_tracker

    def track_hands(self, frame):
        """
        Processes the frame to detect and track hands.

        Args:
            frame (numpy.ndarray): The current video frame.

        Returns:
            tuple: The annotated frame and list of detected hands with their landmarks and gestures.
        """
        # Convert to RGB because MediaPipe works with RGB images
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe
        results = self.hands.process(rgb_frame)

        hands_data = []

        # If hands are detected, draw the landmarks and detect gesture
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(frame, hand_landmarks, self.mpHands.HAND_CONNECTIONS)
                gesture = self.detect_gesture(hand_landmarks)
                hands_data.append({'landmarks': hand_landmarks, 'gesture': gesture})
        else:
            print("No hands detected.")

        return frame, hands_data

    def detect_gesture(self, hand_landmarks):
        """
        Detects gesture based on hand landmarks.

        Args:
            hand_landmarks: The landmarks of the detected hand.

        Returns:
            str: The recognized gesture.
        """
        # Use the gesture tracker to recognize the gesture
        gesture = self.gesture_tracker.recognize_gestures(hand_landmarks.landmark)
        return gesture
