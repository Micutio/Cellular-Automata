__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import sys


class EventHandler:
    def __init__(self, main):
        self.mx = 0
        self.my = 0
        self.main = main
        self.disease = "b"
        self.old_hive_pos = None

    def process_input(self):
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
        self.mx, self.my = pygame.mouse.get_pos()
        self.mx = (self.mx / self.main.gc.CELL_SIZE)
        self.my = (self.my / self.main.gc.CELL_SIZE)

    def mouse_action(self, button):
        # Click on left mouse button.
        # -> set food of cell to max.
        if button == 1:
            #print(self.main.ca.ca_grid[int(self.mx), int(self.my)].pheromones[0])
            #print(self.main.ca.ca_grid[int(self.mx), int(self.my)].pheromones[1])
            self.main.ca.ca_grid[int(self.mx), int(self.my)].food = self.main.gc.MAX_FOOD
        # Click on right mouse button
        # -> toggle cell to be a hive
        elif button == 3:
            if self.old_hive_pos:
                old_cell = self.main.ca.ca_grid[self.old_hive_pos]
                old_cell.is_hive = False
                old_cell.food = 0
            self.old_hive_pos = (int(self.mx), int(self.my))
            cell = self.main.ca.ca_grid[int(self.mx), int(self.my)]
            cell.is_hive = True
            cell.food = 0
            for _, agent in self.main.abm.agent_dict.items():
                agent.hive_pos = self.old_hive_pos

    def keyboard_action(self, active_key):
        if active_key == pygame.K_SPACE:
            self.main.gc.RUN_SIMULATION = not self.main.gc.RUN_SIMULATION
            if self.main.gc.RUN_SIMULATION:
                print(" < simulation resumed")
            else:
                print(" < simulation paused")

        # r key is pressed, reset the simulation
        if active_key == pygame.K_r:
            self.main.reset_simulation()

        if active_key == pygame.K_s:
            self.main.step_simulation()
            self.main.render_simulation()