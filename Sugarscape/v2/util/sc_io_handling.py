__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import sys
import math
import random
import pickle
import os
import os.path
from abm.sc_diseases import Virus, Bacteria


class EventHandler:
    def __init__(self, main):
        self.mx = 0
        self.my = 0
        self.main = main
        self.disease = "b"

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
        self.mx = int(self.mx / self.main.gc.CELL_SIZE)
        self.my = int(self.my / self.main.gc.CELL_SIZE)

    def mouse_action(self, button):
        # Click on left mouse button
        # -> display cell information and agent information
        if button == 1:
            print("[SIMULATION][MODEL][CELL INFO]-------------------------------------------------")
            print(" > cell(%i, %i): sugar = %i, spice = %i" %
                  (self.mx, self.my,
                   self.main.ca.ca_grid[self.mx, self.my].sugar,
                   self.main.ca.ca_grid[self.mx, self.my].spice))
            print("-------------------------------------------------------------------------------")
            if (self.mx, self.my) in self.main.abm.agent_dict:
                agent_attributes = vars(self.main.abm.agent_dict[self.mx, self.my].chromosome)
                print("[SIMULATION][MODEL][AGENT INFO]------------------------------------------------")
                for key in sorted(agent_attributes):
                    if not ("att_map" in key or "immune_system" in key or "genomes" in key):
                        print("+ %s: %s" % (key, agent_attributes[key]))
                print("-------------------------------------------------------------------------------")
        # Click on right mouse button
        # -> display cell information
        elif button == 3:
            # Create disease and infect selected agent.
            if (self.mx, self.my) in self.main.abm.agent_dict:
                dis_genome = [random.getrandbits(1) for _ in range(self.main.gc.DISEASE_GENOME_LENGTH)]
                if self.disease == "b":
                    bacteria = Bacteria(dis_genome)
                    self.main.abm.agent_dict[self.mx, self.my].diseases[bacteria.genome_string] = bacteria
                    print(" < bacterial infection spawned: %s" % bacteria.genome_string)
                if self.disease == "v":
                    virus = Virus(dis_genome)
                    self.main.abm.agent_dict[self.mx, self.my].diseases[virus.genome_string] = virus
                    print(" < viral infection spawned: %s" % virus.genome_string)

    def keyboard_action(self, active_key):
        if active_key == pygame.K_SPACE:
            self.main.gc.RUN_SIMULATION = not self.main.gc.RUN_SIMULATION
            if self.main.gc.RUN_SIMULATION:
                print(" < simulation resumed")
            else:
                print(" < simulation paused")

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
            # TODO: Improve info screen
            print("[SIMULATION][RUN][INFO]--------------------------------------------------------")
            print(" > experiment nr.: %i, ticks: %i" % (self.main.gc.EXPERIMENT_RUN, self.main.gc.TICKS))
            print(" > remaining agents: %i, fertile: %i, richest: %i, poorest: %i" %
                  (len(self.main.abm.agent_dict), i, max_wealth, min_wealth))
            print("-------------------------------------------------------------------------------")

        # p key is pressed, plot graphs
        if active_key == pygame.K_p:
            print(" > plotting statistics")
            self.main.stats.plot()

        # r key is pressed, reset the simulation
        if active_key == pygame.K_r:
            self.main.reset_simulation()

        # s key is pressed, perform one step of the simulation
        # if ctrl + s is pressed, save the current configuration
        if active_key == pygame.K_s:
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.save_sim_status_to_file()
            else:
                self.main.step_simulation()
                self.main.render_simulation()

        # l key is pressed, load saved configuration
        if active_key == pygame.K_l:
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.load_sim_status_from_file()

        # v key is pressed, set disease-to-be-spawned to virus
        if active_key == pygame.K_v:
            self.disease = "v"
            print(" < set spawn-able disease to 'virus'")

        # b key is pressed, set disease-to-be-spawned to bacteria
        if active_key == pygame.K_b:
            self.disease = "b"
            print(" < set spawn-able disease to 'bacteria'")

        # NUMBER KEYS
        # 0 is pressed
        if active_key == pygame.K_0:
            print(" < set draw cell and agent mode to 'disabled'")
            self.main.visualizer.draw_agent_mode = 0
            self.main.visualizer.draw_cell_mode = 0
            self.main.screen.fill((0, 0, 0))
        # 1 key is pressed
        if active_key == pygame.K_1:
            # ctrl is pressed
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                # ctrl + 1: change draw agent mode
                self.main.visualizer.draw_agent_mode = 1
                print(" < set draw agent mode to 0 (tribe and age)")
            # shift is pressed
            elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                # shift + 1: change landscape mode
                self.main.gc.LANDSCAPE_MODE = 1
                print(" < set landscape mode to 1 (plain)")
            else:
                # only 1: change draw cells mode
                self.main.visualizer.draw_cell_mode = 1
                print(" < set draw cell mode to 0 (resources)")
        # 2 key is pressed
        if active_key == pygame.K_2:
            # ctrl is also pressed
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                # ctrl + 2: change draw agent mode
                self.main.visualizer.draw_agent_mode = 2
                print(" < set draw agent mode to 1 (gender)")
            # shift is pressed
            elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                # shift + 2: change landscape mode
                self.main.gc.LANDSCAPE_MODE = 2
                print(" < set landscape mode to 2 (procedurally random)")
            else:
                # only 2: change draw cells mode
                self.main.visualizer.draw_cell_mode = 2
                print(" < set draw cell mode to 1 (tribal territories)")
        # 3 key is pressed
        if active_key == pygame.K_3:
            # ctrl is also pressed
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                # ctrl + 3: change draw agent mode
                self.main.visualizer.draw_agent_mode = 3
                print(" < set draw agent mode to 2 (tribe)")
            # shift is pressed
            elif pygame.key.get_mods() & pygame.KMOD_SHIFT:
                # shift + 3: change landscape mode
                self.main.gc.LANDSCAPE_MODE = 3
                print(" < set landscape mode to 3 (two hills)")
            else:
                # only 3: change draw cells mode
                self.main.visualizer.draw_cell_mode = 3
                print(" < set draw cell mode to 2 (heat-map)")
        # 4 key is pressed
        if active_key == pygame.K_4:
            # ctrl is also pressed
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                # ctrl + 4: change draw agent mode
                self.main.visualizer.draw_agent_mode = 4
                print(" < set draw agent mode to 3 (diseases)")
            else:
                # only 3: change draw cells mode
                self.main.visualizer.draw_cell_mode = 4
                print(" < set draw cell mode to 3 (diseases)")
        if active_key == pygame.K_5:
            self.main.visualizer.draw_cell_mode = 5
            print(" < set draw cell mode to 4 (pollution)")
        if active_key == pygame.K_6:
            self.main.visualizer.draw_cell_mode = 6
            print(" < set draw cell mode to 5 (variable cell size)")

    def save_sim_status_to_file(self):
        filename = self.main.gc.FILE_PATH + "sgrscp_" + str(self.main.gc.TICKS) + ".sav"
        sim_state = {"ca_sugar": self.main.ca.landscape_sugar,
                     "ca_spice": self.main.ca.landscape_spice,
                     "random_state": self.main.random_state}
        with open(filename, "wb") as handle:
            pickle.dump(sim_state, handle)
        print(" > saved landscape to file")

    def load_sim_status_from_file(self):
        found_files = [name for name in os.listdir(self.main.gc.FILE_PATH)
                       if os.path.isfile(name) and "sgrscp_" in name]
        l = len(found_files)
        if l == 0:
            print(" < ERROR: no file found")
            return
        elif l == 1:
            file = found_files[0]
        else:
            print(" > found multiple files:")
            for name in found_files:
                print(" >> [" + str(found_files.index(name)) + "] " + name)
            index = int(input(" < enter number of file to load: "))
            file = found_files[index]

        print(" < loading file: " + file)

        # If we found a file to load, load it.
        # First reset the simulation and then insert the loaded properties into the simulation run.
        with open(file, "rb") as handle:
            sim_state = pickle.load(handle)
            self.main.reset_simulation(sim_state)


class Terminal:
    def __init__(self):
        self.red = "\x1b[0;31m"
        self.green = "\x1b[0;32m"
        self.yellow = "\x1b[0;33m"
        self.blue = "\x1b[0;34m"
        self.pink = "\x1b[0;35m"
        self.teal = "\x1b[0;36"
        self.white = "\x1b[0;37m"
        self.endc = "\x1b[0m"