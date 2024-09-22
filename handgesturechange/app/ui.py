# app/ui.py

import pygame
from pygame.locals import *
import cv2
import numpy as np

class UI:
    def __init__(self):
        """
        Initializes the UI with predefined buttons.
        """
        # Define UI buttons with positions, sizes, colors, and associated actions
        self.buttons = {
            "button1": {
                "position": (100, 500),
                "size": (150, 75),
                "color": (255, 0, 0),
                "action": self.button1_action
            },
            "button2": {
                "position": (300, 500),
                "size": (150, 75),
                "color": (0, 255, 0),
                "action": self.button2_action
            },
            # Add more buttons as needed
        }

        # Initialize Pygame font
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)

    def render(self, screen, hands_data):
        """
        Renders the UI elements and handles interactions based on hand gestures.

        Args:
            screen (pygame.Surface): The main display surface.
            hands_data (list): List of detected hands with landmarks and gestures.
        """
        # Create a transparent surface for UI
        ui_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        ui_surface = ui_surface.convert_alpha()

        # Draw buttons
        for button_name, button in self.buttons.items():
            pygame.draw.rect(
                ui_surface,
                button["color"],
                (*button["position"], *button["size"]),
                border_radius=5
            )
            # Add button labels
            text_surface = self.font.render(button_name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(
                center=(
                    button["position"][0] + button["size"][0] / 2,
                    button["position"][1] + button["size"][1] / 2
                )
            )
            ui_surface.blit(text_surface, text_rect)

        # Detect gestures to interact with UI
        for hand in hands_data:
            gesture = hand['gesture']
            landmarks = hand['landmarks']
            if gesture == "circle":
                # Example: Trigger button1
                self.buttons["button1"]["action"]()
            elif gesture == "square":
                # Example: Trigger button2
                self.buttons["button2"]["action"]()
            elif gesture == "triangle":
                # Example: Trigger other buttons or actions
                pass
            # Add more gestures as needed

        # Blit the UI surface onto the main screen
        screen.blit(ui_surface, (0, 0))

    def button1_action(self):
        """
        Action to perform when button1 is triggered.
        """
        print("Button 1 Action Triggered")

    def button2_action(self):
        """
        Action to perform when button2 is triggered.
        """
        print("Button 2 Action Triggered")
