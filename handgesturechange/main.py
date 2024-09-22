import sys
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from app.hand_tracking import HandTracker
from app.shape_renderer import ShapeRenderer
from app.ui import UI
from utils.camera_utils import initialize_camera
import cv2

def main():
    """
    Main function to run the AR Hand Tracking application.
    """
    # Initialize Pygame
    pygame.init()
    display_size = (800, 600)
    screen = pygame.display.set_mode(display_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("AR Hand Tracking Application")

    # Initialize Camera
    try:
        camera = initialize_camera(width=1280, height=720, fps=30)
    except IOError as e:
        print(f"Error initializing camera: {e}")
        sys.exit(1)

    # Initialize Hand Tracking
    hand_tracker = HandTracker()

    # Initialize Shape Renderer
    shape_renderer = ShapeRenderer(display_size=display_size)

    # Initialize UI
    ui = UI()

    clock = pygame.time.Clock()
    running = True

    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Capture Frame
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Process Hand Tracking
        annotated_frame, hands = hand_tracker.track_hands(frame)

        # Render the shape using OpenGL based on each detected gesture
        if hands:
            for hand in hands:
                gesture = hand['gesture']
                print(f"Detected gesture: {gesture}")  # Debugging line
                if gesture == "circle":
                    shape_renderer.render_shape("circle")
                elif gesture == "square":
                    shape_renderer.render_shape("square")
                elif gesture == "triangle":
                    shape_renderer.render_shape("triangle")
                elif gesture == "cube":
                    shape_renderer.render_shape("cube")
                elif gesture == "swipe_left":
                    shape_renderer.cube_rotation[1] -= 5  # Rotate left
                elif gesture == "swipe_right":
                    shape_renderer.cube_rotation[1] += 5  # Rotate right
                elif gesture == "swipe_up":
                    shape_renderer.cube_position[1] += 0.1  # Move up
                elif gesture == "swipe_down":
                    shape_renderer.cube_position[1] -= 0.1  # Move down
                # Add more gestures as needed
        else:
            # Clear the screen if no hands are detected
            shape_renderer.clear()

        # Render the UI using Pygame
        ui.render(screen, hands)

        # Swap Buffers
        pygame.display.flip()

        # Show hand-tracking in OpenCV window (optional)
        cv2.imshow('Hand Tracking', annotated_frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

        # Cap the Frame Rate
        clock.tick(30)  # Adjust as needed for smooth performance

    # Cleanup
    camera.release()
    cv2.destroyAllWindows()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
