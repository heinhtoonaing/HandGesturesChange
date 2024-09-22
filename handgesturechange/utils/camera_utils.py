# utils/camera_utils.py

import cv2

def initialize_camera(width=1280, height=720, fps=30):
    """
    Initializes the webcam with specified resolution and frame rate.

    Args:
        width (int): Width of the camera frame.
        height (int): Height of the camera frame.
        fps (int): Frames per second.

    Returns:
        cv2.VideoCapture: The initialized camera object.

    Raises:
        IOError: If the webcam cannot be accessed.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)

    return cap
