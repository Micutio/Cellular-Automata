"""
ComplexAutomaton module of the Complex Automaton Base.
Contains the automaton itself.
"""

__author__ = 'Michael Wagner'


import pygame
import math

from ca.cab_ca_hex import CAHex
from abm.cab_abm import ABM
from util.cab_input_handling import InputHandler
from util.cab_visualization import Visualization

from pygame.locals import *


class ComplexAutomaton:
    """
    The main class of Sugarscape. This controls everything.
    """
    def __init__(self, global_constants, **kwargs):  #proto_cell=None, proto_agent=None, proto_visualizer=None, proto_handler=None):
        """
        Standard initializer.
        :param global_constants: All constants or important variables that control the simulation.
        """
        self.gc = global_constants

        pygame.init()
        # pygame.display.init()
        offset = int((math.sqrt(3) / 2) * (self.gc.CELL_SIZE * 2) * self.gc.DIM_X)
        # print(offset)
        # self.screen = pygame.display.set_mode((self.gc.GRID_WIDTH * offset, self.gc.GRID_HEIGHT), pygame.RESIZABLE, 32)
        self.screen = pygame.display.set_mode((offset, self.gc.GRID_HEIGHT), HWSURFACE|DOUBLEBUF, 32)
        pygame.display.set_caption('Complex Automaton Base')

        if 'proto_visualizer' in kwargs:
            self.visualizer = kwargs['proto_visualizer'].clone(self.screen)
        else:
            self.visualizer = Visualization(self.gc, self.screen)

        if 'proto_cell' in kwargs:
            self.ca = CAHex(self.gc, self.visualizer, proto_cell=kwargs['proto_cell'])
            self.proto_cell = kwargs['proto_cell']
        else:
            self.ca = CAHex(self.gc, self.visualizer)
            self.proto_cell = None

        if 'proto_agent' in kwargs:
            self.abm = ABM(self.gc, self.visualizer, proto_agent=kwargs['proto_agent'])
            self.proto_agent = kwargs['proto_agent']
        else:
            self.abm = ABM(self.gc, self.visualizer)
            self.proto_agent = None

        if 'proto_handler' in kwargs:
            self.handler = kwargs['proto_handler'].clone(self)
        else:
            self.handler = InputHandler(cab_system=self)

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
        self.ca.__init__(self.gc, self.visualizer, self.proto_cell)
        self.abm.__init__(self.gc, self.visualizer, self.proto_agent)
        self.gc.TIME_STEP = 0

    def step_simulation(self):
        self.abm.cycle_system(self.ca)
        self.ca.cycle_automaton()
        self.gc.TIME_STEP += 1

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
        while True:
            if self.gc.RUN_SIMULATION:
                self.step_simulation()
                self.gc.TIME_STEP += 1
            self.render_simulation()
            self.handler.process_input()
