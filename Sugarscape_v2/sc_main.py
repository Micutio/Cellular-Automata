from sc_stat import Statistics

__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is a python prototype for a complex automaton, which
# integrates a CA and ABM. The CA is supposed to simulate heat emission
# of an object passing through the CA grid.

# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"

import time

from sc_ca import *
from sc_abm import *

import pygame
from pygame.locals import *

import sys

#########################################################################
###                       Global Variables                            ###
#########################################################################


class GlobalConstants:
    def __init__(self):
        self.num_agents = 250
        self.landscape_mode = 3  # 3 = twohill, 2 = procedural, 1 = randomized
        self.run_simulation = False
        self.cell_size = 15
        self.grid_width = int(500 / 10) * self.cell_size
        self.grid_height = int(500 / 10) * self.cell_size
        #self.abm_bounds = (0, 10, 40, 50)
        self.abm_bounds = (0, 50, 0, 50)
        self.ticks = 0
        self.ms_per_tick = 60

GC = GlobalConstants()

#########################################################################
###                            CLASSES                                ###
#########################################################################


class EventHandler:
    def __init__(self):
        self.mx = 0
        self.my = 0

    def mouse_motion(self):
        self.mx, self.my = pygame.mouse.get_pos()
        self.mx = (self.mx / GC.cell_size)
        self.my = (self.my / GC.cell_size)

    def mouse_action(self, button, ca):
        # Click on left mouse button, set temperature of cell to max
        # Click again to disable / enable cooling of the cell
        if button == 1:
            print("> cell %i, %i = 1, T = %i" % (self.mx, self.my, ca.ca_grid[int(self.mx), int(self.my)].sugar))
            #ca[int(mx), int(my)].sugar = MAX_SUGAR

        # Click on right mouse button
        elif button == 3:
            print("> cell %i, %i = 1, T = %i" % (self.mx, self.my, ca.ca_grid[int(self.mx), int(self.my)].sugar))
            #ca[int(mx), int(my)].sugar = 0

    def keyboard_action(self, active_key, ca, abm, stats, screen):
        if active_key == pygame.K_SPACE:
            GC.run_simulation = not GC.run_simulation
            if GC.run_simulation:
                print("> simulation started")
            else:
                print("> simulation paused")
        # up arrow is pressed, speed up simulation
        # e key is pressed, examine the cell and agent, if there is one
        if active_key == pygame.K_e:
            px = math.floor(self.mx)
            py = math.floor(self.my)
            ax = (GC.cell_size * px) + int(GC.cell_size / 2)
            ay = (GC.cell_size * py) + int(GC.cell_size / 2)
            a = abm.get_agent_at_position(ax, ay)
            if a:
                print("+----- CELL INFO ------------------------------------------------------")
                print("+ > cell (" + str(px) + ", " + str(py) + ") : " + str(ca.ca_grid[px, py].sugar))
                print("+ > agent " + a.gene_id + ", age: " + str(a.age) + ", will die at " + str(a.dying_age) + ":")
                print("+ >> sugar(initial): " + str(a.init_sugar) + " sugar(now): " + str(a.sugar))
                print("+ >> spice(initial): " + str(a.init_spice) + " spice(now): " + str(a.spice))
                print("+ >> metab_sugar = " + str(a.metab_sugar) + ", metab_spice: " + str(a.metab_spice))
                print("+ >> gender: " + a.gender + ", fertile between " + str(a.fertility))
                print("+----------------------------------------------------------------------")
            else:
                print("+----- CELL INFO ------------------------------------------------------")
                print("+ > cell (" + str(px) + ", " + str(py) + ") : " + str(ca.ca_grid[px, py].sugar))
                print("+----------------------------------------------------------------------")
            #coords = a.visible_cells(ca)
        # i key is pressed, display general info about the automata
        if active_key == pygame.K_i:
            i = 0
            max_wealth = 0
            min_wealth = 99999
            for (_, _), a in abm.agent_dict.items():
                if a.is_fertile() and a.sugar > a.init_sugar:
                    i += 1
                if a.sugar > max_wealth:
                    max_wealth = a.sugar
                elif a.sugar < min_wealth:
                    min_wealth = a.sugar
            print("+----- GENERAL INFO ---------------------------------------------------")
            print("+ > ticks: " + str(GC.ticks) + " remaining agents: " + str(len(abm.agent_dict)))
            print("+ > fertile agents: " + str(i) + ", richest: " + str(max_wealth) + ", poorest: " + str(min_wealth))
            print("+----------------------------------------------------------------------")
            stats.plot()
        # r key is pressed, reset the simulation
        if active_key == pygame.K_r:
            ca.__init__(GC.landscape_mode, GC.grid_width, GC.grid_height, GC.cell_size)
            abm.__init__(GC.num_agents, GC.cell_size, GC.abm_bounds[0], GC.abm_bounds[1], GC.abm_bounds[2], GC.abm_bounds[3])
            GC.ticks = 0
            render_simulation(ca, abm, screen)
            print("> reset simulation")

        # s key is pressed, perform one step of the simulation
        if active_key == pygame.K_s:
            step_simulation(ca, abm)
            render_simulation(ca, abm, screen)

    def process_input(self, ca, abm, stats, screen):
        for event in pygame.event.get():
            # The 'x' on the window is clicked
            if event.type == QUIT:
                sys.exit()
            # Mouse motion
            elif event.type == MOUSEMOTION:
                self.mouse_motion()
            # Mouse action
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_action(event.button, ca)
            # Keyboard key is pressed
            elif event.type == pygame.KEYUP:
                # space bar is pressed
                self.keyboard_action(event.key, ca, abm, stats, screen)

#########################################################################
###                          GLOBAL METHODS                           ###
#########################################################################


def main():
    """
    Main method. It executes the CA.
    :return: nothing
    """
    # Initialize GUI
    pygame.init()
    screen = pygame.display.set_mode((GC.grid_width, GC.grid_height), pygame.RESIZABLE, 32)
    pygame.display.set_caption('Sugarscape')

    # Initialize the ca grid.
    ca = CA(GC.landscape_mode, GC.grid_width, GC.grid_height, GC.cell_size)
    #abm = ABM(GLOBAL_CONSTANTS.num_agents, GLOBAL_CONSTANTS.grid_width, GLOBAL_CONSTANTS.grid_height)
    abm = ABM(GC.num_agents, GC.cell_size, GC.abm_bounds[0], GC.abm_bounds[1], GC.abm_bounds[2], GC.abm_bounds[3])
    handler = EventHandler()
    stats = Statistics(abm, ca)

    # TODO: fix simulation loop
    # Initialize other simulation related objects
    while 1:
        # This block performs a simulation step.
        if GC.run_simulation:
            step_simulation(ca, abm)
            stats.update_records()
            GC.ticks += 1
        render_simulation(ca, abm, screen)
        handler.process_input(ca, abm, stats, screen)


def step_simulation(ca, abm):
    abm.cycle_system(ca)
    ca.cycle_automaton()


def render_simulation(ca, abm, screen):
    ca.draw_cells(screen)
    abm.draw_agents(screen)
    pygame.display.flip()

if __name__ == '__main__':
    main()
