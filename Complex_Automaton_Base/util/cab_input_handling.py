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
        if cab_system is None:
            self.sys = None
        else:
            self.sys = cab_system

    def clone(self, cab_sys):
        return InputHandler(cab_sys)

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
                self.custom_mouse_action(event.button)
            # Keyboard key is pressed
            elif event.type == pygame.KEYUP:
                # space bar is pressed
                self.def_keyboard_action(event.key)
                self.custom_keyboard_action(event.key)

    def mouse_motion(self):
        """
        Method to track mouse motion.
        Overwrite custom_mouse_motion to add functionality here.
        """
        self.mx, self.my = pygame.mouse.get_pos()
        self.mx = (self.mx / self.sys.gc.CELL_SIZE)
        self.my = (self.my / self.sys.gc.CELL_SIZE)
        self.custom_mouse_motion()

    def custom_mouse_motion(self):
        """
        Overwrite to define additional actions on mouse movement.
        """
        pass

    def custom_mouse_action(self, button):
        """
        Processing Mouse action. Overwrite to extend!
        """
        # Click on left mouse button.
        if button == 1:
            raise NotImplementedError

        # Click on right mouse button
        elif button == 3:
            raise NotImplementedError

    def def_keyboard_action(self, active_key):
        """
        Method to process all the keyboard inputs.
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
            print(" > simulation reset")

        # Simulation Standard: 's' advances the simulation by one step
        if active_key == pygame.K_s:
            self.sys.step_simulation()
            self.sys.render_simulation()
            print(" < stepping simulation")

    def custom_keyboard_action(self, active_key):
        """
        Customizable Method to process keyboard inputs.
        Overwrite this method to add more inputs.
        """
        pass