"""
ComplexAutomaton module of the Complex Automaton Base.
Contains the automaton itself.
"""

__author__ = 'Michael Wagner'


import pygame

from ca.cab_ca import CA
from abm.cab_abm import ABM
from util.cab_input_handling import InputHandler
from util.cab_visualization import Visualization


class ComplexAutomaton:
    """
    The main class of Sugarscape. This controls everything.
    """
    def __init__(self, global_constants, proto_cell=None, proto_agent=None, proto_visualizer=None, proto_handler=None):
        """
        Standard initializer.
        :param global_constants: All constants or important variables that control the simulation.
        """
        self.gc = global_constants

        pygame.init()
        self.screen = pygame.display.set_mode((self.gc.GRID_WIDTH, self.gc.GRID_HEIGHT), pygame.RESIZABLE, 32)
        pygame.display.set_caption('Complex Automaton Base')

        if proto_visualizer is None:
            self.visualizer = Visualization(self.screen, self.gc)
        else:
            self.visualizer = proto_visualizer.clone(self.screen, self.gc)

        if proto_cell is None:
            self.ca = CA(self.gc, self.visualizer)
        else:
            self.ca = CA(self.gc, self.visualizer, proto_cell=proto_cell)

        if proto_agent is None:
            self.abm = ABM(self.gc, self.visualizer)
        else:
            self.abm = ABM(self.gc, self.visualizer, proto_agent=proto_agent)

        if proto_handler is None:
            self.handler = InputHandler(self)
        else:
            self.handler = proto_handler.clone(self)

        self.display_info()
        return

    def display_info(self):
        print("\n-------------------------[Complex Automaton Base]------------------------------"
              "\n > %s"
              "\n-------------------------------------------------------------------------------"
              "\n [COMMANDS]------------------------------------------------------------------- "
              "\n  [SIMULATION CONTROL]-------------------------------------------------------  "
              "\n   > [SPACE] pause/resume simulation                                           "
              "\n  ---------------------------------------------------------------------------  "
              "\n" % self.gc.VERSION)

    def reset_simulation(self):
        self.ca.__init__(self.gc, self.visualizer)
        self.abm.__init__(self.gc, self.visualizer)

    def step_simulation(self):
        self.abm.cycle_system(self.ca)
        self.ca.cycle_automaton()

    def render_simulation(self):
        self.ca.draw_cells()
        self.abm.draw_agents()
        pygame.display.flip()

    def run_main_loop(self):
        """
        Main method. It executes the CA.
        """
        print("------------------------------[SIMULATION LOG]---------------------------------\n"
              "                                                                               ")
        while 1:
            if self.gc.RUN_SIMULATION:
                self.step_simulation()
            self.render_simulation()
            self.handler.process_input()