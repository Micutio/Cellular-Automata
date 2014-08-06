__author__ = 'Michael Wagner'
__version__ = '1.0'

# This is a python prototype for a complex automaton, which
# integrates a CA and ABM. Together they form the SugarScape.

# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"

import pygame
import sys
from pygame.locals import *
from v2.abm.sc_abm import ABM
from v2.ca.sc_ca import CA
from v2.util.sc_stat import Statistics
from v2.sc_global_constants import GlobalConstants


#########################################################################
###                       Global Variables                            ###
#########################################################################

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
        self.mx = (self.mx / GC.CELL_SIZE)
        self.my = (self.my / GC.CELL_SIZE)

    def mouse_action(self, button, ca):
        # Click on left mouse button
        # -> display cell information
        if button == 1:
            print("> cell %i, %i = 1, T = %i" % (self.mx, self.my, ca.ca_grid[int(self.mx), int(self.my)].sugar))
            #ca[int(mx), int(my)].sugar = MAX_SUGAR

        # Click on right mouse button
        # -> display cell information
        elif button == 3:
            print("> cell %i, %i = 1, T = %i" % (self.mx, self.my, ca.ca_grid[int(self.mx), int(self.my)].sugar))
            #ca[int(mx), int(my)].sugar = 0

    def keyboard_action(self, active_key, ca, abm, stats, screen):
        # TODO: add switching of visualizing modes
        if active_key == pygame.K_SPACE:
            GC.RUN_SIMULATION = not GC.RUN_SIMULATION
            if GC.RUN_SIMULATION:
                print("> simulation started")
            else:
                print("> simulation paused")
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
            print("+ > ticks: " + str(GC.TICKS) + " remaining agents: " + str(len(abm.agent_dict)))
            print("+ > fertile agents: " + str(i) + ", richest: " + str(max_wealth) + ", poorest: " + str(min_wealth))
            print("+----------------------------------------------------------------------")
            stats.plot()
        # r key is pressed, reset the simulation
        if active_key == pygame.K_r:
            ca.__init__(GC.LANDSCAPE_MODE, GC.GRID_WIDTH, GC.GRID_HEIGHT, GC.CELL_SIZE)
            abm.__init__(GC.NUM_AGENTS, GC.CELL_SIZE, GC.ABM_BOUNDS[0], GC.ABM_BOUNDS[1], GC.ABM_BOUNDS[2], GC.ABM_BOUNDS[3])
            stats.__init__(abm, ca)
            GC.TICKS = 0
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
    screen = pygame.display.set_mode((GC.GRID_WIDTH, GC.GRID_HEIGHT), pygame.RESIZABLE, 32)
    pygame.display.set_caption('Sugarscape')

    # Initialize the ca grid.
    ca = CA(GC.LANDSCAPE_MODE, GC.GRID_WIDTH, GC.GRID_HEIGHT, GC.CELL_SIZE)
    #abm = ABM(GLOBAL_CONSTANTS.num_agents, GLOBAL_CONSTANTS.grid_width, GLOBAL_CONSTANTS.grid_height)
    abm = ABM(GC.NUM_AGENTS, GC.CELL_SIZE, GC.ABM_BOUNDS[0], GC.ABM_BOUNDS[1], GC.ABM_BOUNDS[2], GC.ABM_BOUNDS[3])
    handler = EventHandler()
    stats = Statistics(abm, ca)
    update = True

    # TODO: fix simulation loop
    # Initialize other simulation related objects
    while 1:
        # This block performs a simulation step.
        if GC.RUN_SIMULATION:
            step_simulation(ca, abm)
            if update:
                stats.update_records()
            update = not update
            GC.TICKS += 1
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
