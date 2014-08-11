__author__ = 'Michael Wagner'
__version__ = '1.0'

# This is a python prototype for a complex automaton, which
# integrates a CA and ABM. Together they form the SugarScape.

# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"

# Also thanks to David Grotzki for comprehensive advice on biology and especially genetics.

import pygame

from v2.abm.sc_abm import ABM
from v2.ca.sc_ca import CA
from v2.util.sc_stat import Statistics
from v2.sc_global_constants import GlobalConstants
from v2.util.sc_io_handler import EventHandler
from v2.util.sc_visualization import Visualization


class Sugarscape:
    """
    The main class of Sugarscape. This controls everything.
    """

    def __init__(self, global_constants):
        """
        Standard initializer.
        :param global_constants: All constants or important variables that control the simulation.
        """
        self.gc = global_constants

        pygame.init()
        self.screen = pygame.display.set_mode((self.gc.GRID_WIDTH, self.gc.GRID_HEIGHT), pygame.RESIZABLE, 32)
        pygame.display.set_caption('Sugarscape Simulation')

        self.visualizer = Visualization(self.screen, self.gc)
        self.ca = CA(self.visualizer, self.gc)
        self.abm = ABM(self.visualizer, self.gc)
        self.handler = EventHandler(self)
        self.stats = Statistics(self.abm, self.ca, self.gc)
        return

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
        while 1:
            # This block performs a simulation step.
            if GC.RUN_SIMULATION:
                self.step_simulation()
                self.stats.update_records()
                self.gc.TICKS += 1
            self.render_simulation()
            self.handler.process_input()


if __name__ == '__main__':

    # Initialize simulation parameters and simulation itself.
    GC = GlobalConstants()
    simulation = Sugarscape(GC)

    # Start the Simulation and enjoy!
    simulation.run_main_loop()