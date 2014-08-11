__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import sys
import math
from pygame.locals import *


class EventHandler:
    def __init__(self, main):
        self.mx = 0
        self.my = 0
        self.main = main
        self.gc = main.gc

    def process_input(self):
        for event in pygame.event.get():
            # The 'x' on the window is clicked
            if event.type == QUIT:
                sys.exit()
            # Mouse motion
            elif event.type == MOUSEMOTION:
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
        self.mx = (self.mx / self.gc.CELL_SIZE)
        self.my = (self.my / self.gc.CELL_SIZE)

    def mouse_action(self, button):
        # Click on left mouse button
        # -> display cell information and agent information
        if button == 1:
            print("> cell %i, %i = 1, sugar = %i, spice = %i" %
                  (self.mx, self.my,
                   self.main.ca.ca_grid[int(self.mx), int(self.my)].sugar,
                   self.main.ca.ca_grid[int(self.mx), int(self.my)].spice))
            agent_x = (math.floor(self.mx) * self.gc.CELL_SIZE) + int(self.gc.CELL_SIZE / 2)
            agent_y = (math.floor(self.my) * self.gc.CELL_SIZE) + int(self.gc.CELL_SIZE / 2)
            if (agent_x, agent_y) in self.main.abm.agent_dict:
                agent_attributes = vars(self.main.abm.agent_dict[agent_x, agent_y].chromosome)
                print("+----- AGENT INFO -----------------------------------------------------")
                for key in sorted(agent_attributes):
                    if key != "att_map" or key != "immune_system":
                        print("+ %s: %s" % (key, agent_attributes[key]))
                print("+----------------------------------------------------------------------")
        # Click on right mouse button
        # -> display cell information
        elif button == 3:
            print("> cell %i, %i = 1, sugar = %i, spice = %i" %
                  (self.mx, self.my,
                   self.main.ca.ca_grid[int(self.mx), int(self.my)].sugar,
                   self.main.ca.ca_grid[int(self.mx), int(self.my)].spice))

    def keyboard_action(self, active_key):
        if active_key == pygame.K_SPACE:
            self.gc.RUN_SIMULATION = not self.gc.RUN_SIMULATION
            if self.gc.RUN_SIMULATION:
                print("> simulation started")
            else:
                print("> simulation paused")
        # i key is pressed, display general info about the automata
        if active_key == pygame.K_i:
            i = 0
            max_wealth = 0
            min_wealth = 99999
            for (_, _), a in self.main.abm.agent_dict.items():
                if a.is_fertile() and a.sugar > a.init_sugar:
                    i += 1
                if a.sugar > max_wealth:
                    max_wealth = a.sugar
                elif a.sugar < min_wealth:
                    min_wealth = a.sugar
            print("+----- GENERAL INFO ---------------------------------------------------")
            print("+ > ticks: " + str(self.gc.TICKS) + " remaining agents: " + str(len(self.main.abm.agent_dict)))
            print("+ > fertile agents: " + str(i) + ", richest: " + str(max_wealth) + ", poorest: " + str(min_wealth))
            print("+----------------------------------------------------------------------")
            self.main.stats.plot()
        if active_key == pygame.K_r:
            self.main.ca.__init__(self.main.visualizer, self.gc)
            self.main.abm.__init__(self.main.visualizer, self.gc)
            self.main.stats.__init__(self.main.abm, self.main.ca, self.gc)
            self.gc.TICKS = 0
            #render_simulation(ca, abm, screen)
            print("> reset simulation")

        # s key is pressed, perform one step of the simulation
        if active_key == pygame.K_s:
            self.main.step_simulation()
            self.main.render_simulation()

        # NUMBER KEYS
        # 1 key is pressed
        if active_key == pygame.K_1:
            # ctrl is pressed
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                # ctrl + 1: change draw agent mode
                self.main.visualizer.draw_agent_mode = 0
                print("> set draw agent mode to 0 (tribe and age)")
            # shift is pressed
            elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                # shift + 1: change landscape mode
                self.gc.LANDSCAPE_MODE = 3
                print("> set landscape mode to 3 (procedurally random)")
            else:
                # only 1: change draw cells mode
                self.main.visualizer.draw_cell_mode = 0
                print("> set draw cell mode to 0 (resources)")
        # 2 key is pressed
        if active_key == pygame.K_2:
            # ctrl is also pressed
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                # ctrl + 1: change draw agent mode
                self.main.visualizer.draw_agent_mode = 1
                print("> set draw agent mode to 1 (gender)")
            # shift is pressed
            elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                # shift + 2: change landscape mode
                self.gc.LANDSCAPE_MODE = 2
                print("> set landscape mode to 2 (two hills)")
            else:
                # only 1: change draw cells mode
                self.main.visualizer.draw_cell_mode = 1
                print("> set draw cell mode to 1 (tribal territories)")
        # 3 key is pressed
        if active_key == pygame.K_3:
            # ctrl is also pressed
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                # ctrl + 1: change draw agent mode
                self.main.visualizer.draw_agent_mode = 2
                print("> set draw agent mode to 2 (tribe)")
            # shift is pressed
            elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                # shift + 1: change landscape mode
                self.gc.LANDSCAPE_MODE = 1
                print("> set landscape mode to 1 (random)")
            else:
                # only 1: change draw cells mode
                self.main.visualizer.draw_cell_mode = 2
                print("> set draw cell mode to 2 (heat-map)")