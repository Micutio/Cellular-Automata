#!/usr/bin/python
from v2.tc_stat import Statistics

__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is a python prototype for a complex automaton, which
# integrates a CA and ABM. The CA is supposed to simulate heat emission
# of an object passing through the CA grid.

# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"


import sys
import math

from v2.tc_ca import *
from v2.tc_abm import AgentBasedSystem
from pygame.locals import *

#########################################################################
###                       Global Variables                            ###
#########################################################################


class GlobalConstants():
    def __init__(self):
        self.grid_with = 500
        self.grid_height = 500
        self.cell_size = 10
        self.run_simulation = False

GC = GlobalConstants()

#########################################################################
###                            CLASSES                                ###
#########################################################################


#########################################################################
###                          GLOBAL METHODS                           ###
#########################################################################

class InputHandler():
    """
    Handles all mouse and keyboard input.
    :return:
    """
    def __init__(self):
        self.mx = 0
        self.my = 0

    def handle(self, ca, abm, stats):
        for event in pygame.event.get():
            # The 'x' on the window is clicked
            if event.type == QUIT:
                sys.exit()

            # Mouse is moved
            elif event.type == MOUSEMOTION:
                self.mx, self.my = pygame.mouse.get_pos()
                self.mx = (self.mx / 10)
                self.my = (self.my / 10)

            # Mouse button is pressed
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_input(event, ca, abm)

            # Keyboard key is pressed
            elif event.type == pygame.KEYUP:
                self.handle_keyboard_input(event, stats)

    def handle_mouse_input(self, event, ca, abm):
        # Click on left mouse button, set temperature of cell to max
        # Click again to disable / enable cooling of the cell
        if event.button == 1:
            px = math.floor(self.mx)
            py = math.floor(self.my)
            ax = (GC.cell_size * px) + int(GC.cell_size / 2)
            ay = (GC.cell_size * py) + int(GC.cell_size / 2)
            abm.add_agent(ax, ay, True)
            ca.ca_grid[int(self.mx), int(self.my)].temperature = 1
            print("Cell %i, %i = 1, T = %i" % (self.mx, self.my, ca.ca_grid[int(self.mx), int(self.my)].temperature))

        # Click on right mouse button
        elif event.button == 3:
            px = math.floor(self.mx)
            py = math.floor(self.my)
            ax = (GC.cell_size * px) + int(GC.cell_size / 2)
            ay = (GC.cell_size * py) + int(GC.cell_size / 2)
            abm.add_agent(ax, ay, False)
            ca.ca_grid[int(self.mx), int(self.my)].temperature = 1
            print("Cell %i, %i = 1, T = %i" % (self.mx, self.my, ca.ca_grid[int(self.mx), int(self.my)].temperature))

    def handle_keyboard_input(self, event, stats):
        # space bar is pressed
        if event.key == pygame.K_SPACE:
            GC.run_simulation = not GC.run_simulation
            if GC.run_simulation:
                print("> resumed simulation")
            else:
                print("> paused simulation")
        elif event.key == pygame.K_i:
            stats.plot()


def main():
    """
    Main method. It executes the CA.
    :return: nothing
    """
    # initialize GUI
    pygame.init()
    screen = pygame.display.set_mode((GC.grid_with, GC.grid_height))
    pygame.display.set_caption('Complex Automaton')
    ca = CellularAutomaton(GC.grid_with, GC.grid_height, GC.cell_size)
    abm = AgentBasedSystem(GC.grid_with, GC.grid_height, GC.cell_size)
    input_handler = InputHandler()
    stats = Statistics(abm, ca)
    # Add some test agents
    abm.random_scenario(25, 1, 25, ca)

    while 1:
        if GC.run_simulation:
            #ca.cycle_ca()
            abm.cycle_agents(ca)
            stats.update_records()
        input_handler.handle(ca, abm, stats)
        render_simulation(ca, abm, screen)


def render_simulation(ca, abm, screen):
    ca.draw_cells(screen)
    abm.draw_agents(screen)
    pygame.display.flip()

if __name__ == '__main__':
    main()
