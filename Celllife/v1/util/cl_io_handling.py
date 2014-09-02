__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import math
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
        # -> increase amount of o2
        if button == 1:
            #self.main.ca.ca_grid[int(self.mx), int(self.my)].o2 += 1
            agent_x = int(self.mx)
            agent_y = int(self.my)
            if (agent_x, agent_y) in self.main.abm.agent_dict:
                for agent in self.main.abm.agent_dict[agent_x, agent_y]:
                    print("[SIMULATION][MODEL][AGENT]-----------------------------------------------------")
                    agent_attributes = vars(agent)
                    for key in sorted(agent_attributes):
                        print("+ %s: %s" % (key, agent_attributes[key]))
                    print("[SIMULATION][MODEL][AGENT][CHROMOSOME]-----------------------------------------")
                    agent_attributes = vars(agent.chromosome)
                    for key in sorted(agent_attributes):
                        print("+ %s: %s" % (key, agent_attributes[key]))
                    print("[SIMULATION][MODEL][AGENT][CHROMOSOME][CORE]-----------------------------------")
                    agent_attributes = vars(agent.chromosome.core)
                    for key in sorted(agent_attributes):
                        print("+ %s: %s" % (key, agent_attributes[key]))
                    print("-------------------------------------------------------------------------------")

            print("[SIMULATION][MODEL][CELL INFO]-------------------------------------------------")
            print(" > cell(%i, %i): co2 = %f,  light = %f, h2o = %f, o2 = %f, glucose = %f" %
                  (self.mx, self.my,
                   self.main.ca.ca_grid[int(self.mx), int(self.my)].co2,
                   self.main.ca.ca_grid[int(self.mx), int(self.my)].light,
                   self.main.ca.ca_grid[int(self.mx), int(self.my)].h2o,
                   self.main.ca.ca_grid[int(self.mx), int(self.my)].o2,
                   self.main.ca.ca_grid[int(self.mx), int(self.my)].glucose))
            print("-------------------------------------------------------------------------------")
        # Click on mouse scroll wheel.
        # -> increase amount of co2
        #if button == 2:
        #    self.main.ca.ca_grid[int(self.mx), int(self.my)].h2o += 1
        # Click on right mouse button
        # -> increase amount of glucose
        #elif button == 3:
        #    self.main.ca.ca_grid[int(self.mx), int(self.my)].glucose += 1

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