# utils/gesture_recognition.py

class GestureTracker:
    def __init__(self):
        self.previous_wrist_pos = None

    def recognize_gestures(self, landmarks):
        """
        Recognizes hand gestures based on landmark positions.

        Args:
            landmarks (list of mediapipe.framework.formats.landmark_pb2.NormalizedLandmark):
                List containing hand landmarks.

        Returns:
            str: Recognized gesture name ("circle", "square", "triangle", "swipe_left", "swipe_right", "swipe_up", "swipe_down", "none").
        """
        index_finger_tip = landmarks[8]  # Index finger tip
        thumb_tip = landmarks[4]          # Thumb tip
        pinky_tip = landmarks[20]         # Pinky tip
        wrist = landmarks[0]              # Wrist

        current_wrist_pos = (wrist.x, wrist.y)

        # Detect swipes based on wrist movement
        if self.previous_wrist_pos:
            dx = current_wrist_pos[0] - self.previous_wrist_pos[0]
            dy = current_wrist_pos[1] - self.previous_wrist_pos[1]

            if abs(dx) > 0.1:  # Adjust threshold as needed
                if dx > 0:
                    gesture = "swipe_right"
                else:
                    gesture = "swipe_left"
            elif abs(dy) > 0.1:
                if dy > 0:
                    gesture = "swipe_up"
                else:
                    gesture = "swipe_down"
            else:
                gesture = "none"
        else:
            gesture = "none"

        # Store current wrist position for next frame
        self.previous_wrist_pos = current_wrist_pos

        # Example Gesture: Circle
        if (index_finger_tip.y < wrist.y and
            thumb_tip.x < index_finger_tip.x and
            pinky_tip.x > index_finger_tip.x):
            return "circle"

        # Example Gesture: Square
        elif (index_finger_tip.y < wrist.y and
              thumb_tip.x > index_finger_tip.x and
              pinky_tip.x < index_finger_tip.x):
            return "square"

        # Example Gesture: Triangle
        elif index_finger_tip.y > wrist.y:
            return "triangle"

        # No recognized gesture
        return gesture if gesture != "none" else "none"
