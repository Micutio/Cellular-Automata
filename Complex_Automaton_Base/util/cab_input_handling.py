"""
This module contains a generic InputHandler which handles all keyboard and mouse input to the simulation.
"""

__author__ = 'Michael Wagner'

import pygame
import sys


class InputHandler:
    def __init__(self, cab_system):
        self.mx = 0
        self.my = 0
        self.sys = cab_system
        self.disease = "b"
        self.old_hive_pos = None

    def process_input(self):
        """
        Method to process input. Do not overwrite!
        """
        for event in pygame.event.get():
            # The 'x' on the window is clicked
            if event.type == pygame.QUIT:
                sys.exit()
            # Mouse motion
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_motion()
            # Mouse action
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_action(event.button)
            # Keyboard key is pressed
            elif event.type == pygame.KEYUP:
                # space bar is pressed
                self.keyboard_action(event.key)

    def mouse_motion(self):
        """
        Method to track mouse motion. Do not overwrite!
        """
        self.mx, self.my = pygame.mouse.get_pos()
        self.mx = (self.mx / self.sys.gc.CELL_SIZE)
        self.my = (self.my / self.sys.gc.CELL_SIZE)

    def mouse_action(self, button):
        """
        Processing Mouse action. Extend module here!
        """
        # Click on left mouse button.
        if button == 1:
            raise NotImplementedError

        # Click on right mouse button
        elif button == 3:
            raise NotImplementedError

    def keyboard_action(self, active_key):
        """
        Method to process all the keyboard inputs.
        Define additional keys here!
        """
        if active_key == pygame.K_SPACE:
            self.sys.gc.RUN_SIMULATION = not self.sys.gc.RUN_SIMULATION
            if self.sys.gc.RUN_SIMULATION:
                print(" < simulation resumed")
            else:
                print(" < simulation paused")

        # Simulation Standard: 'r' resets the simulation
        if active_key == pygame.K_r:
            self.sys.reset_simulation()

        # Simulation Standard: 's' advances the simulation by one step
        if active_key == pygame.K_s:
            self.sys.step_simulation()
            self.sys.render_simulation()