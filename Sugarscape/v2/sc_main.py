from v2.abm.sc_abm import ABM

__author__ = 'Michael Wagner'
__version__ = '1.0'

# This is a python prototype for a complex automaton, which
# integrates a CA and ABM. Together they form the SugarScape.

# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"

# Also thanks to David Grotzki for comprehensive advice on biology and especially genetics.

import pygame

from ca.sc_ca import CA
from util.sc_stat import Statistics
from sc_global_constants import GlobalConstants
from util.sc_visualization import Visualization
from util.sc_io_handler import EventHandler


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

    def reset_simulation(self):
        self.ca.__init__(self.visualizer, self.gc)
        self.abm.__init__(self.visualizer, self.gc)
        self.stats.__init__(self.abm, self.ca, self.gc)
        self.gc.TICKS = 0
        self.gc.EXPERIMENT_RUN += 1
        #render_simulation(ca, abm, screen)
        print("+-[SYSTEM]---------------------------------------------------------------------+")
        print("+ > simulation ended after %i ticks" % self.gc.TICKS)
        print("+ > starting experiment run %i" % self.gc.EXPERIMENT_RUN)
        print("+------------------------------------------------------------------------------+")

    def run_main_loop(self):
        """
        Main method. It executes the CA.
        """
        print("\n+--------------------------[SUGARSCAPE SIMULATION]-----------------------------+"
              "\n+ > version 08-2014                                                            +"
              "\n+------------------------------------------------------------------------------+"
              "\n+-[commands]-------------------------------------------------------------------+"
              "\n++-[rendering]----------------------------------------------------------------++"
              "\n++ > [1] cells show resources                                                 ++"
              "\n++ > [2] cells show tribal territories                                        ++"
              "\n++ > [3] cells show population density                                        ++"
              "\n++ > [5] cells show pollution                                                 ++"
              "\n++ > [CTRL] + [1] agents show age, gender and tribe                           ++"
              "\n++ > [CTRL] + [2] agents show tribe                                           ++"
              "\n++ > [CTRL] + [3] agents show gender                                          ++"
              "\n++ > [CTRL] + [4] agents show diseases                                        ++"
              "\n++-[simulation control]-------------------------------------------------------++"
              "\n++ > [SPACE] pause/resume simulation                                          ++"
              "\n++ > [SHIFT] + [1] plain resource distribution                                ++"
              "\n++ > [SHIFT] + [2] random resource distribution                               ++"
              "\n++ > [SHIFT] + [3] classic 'two-hill' resource distribution                   ++"
              "\n++ > [RIGHT MOUSE BUTTON] infect agent with disease (default=bacteria)        ++"
              "\n++ > [b] set disease infection on mouse click to 'bacteria'                   ++"
              "\n++ > [v] set disease infection on mouse click to 'virus'                      ++"
              "\n++-[simulation info]----------------------------------------------------------++"
              "\n++ > [LEFT MOUSE BUTTON] show information about selected cell and agent       ++"
              "\n++ > [i] show simulation statistics                                           ++"
              "\n++ > [p] plot graphs with statistics and additional information               ++"
              "\n+------------------------------------------------------------------------------+"
              "\n+-----------------------------[Simulation LOG]---------------------------------+")
        while 1:
            # This block performs a simulation step.
            if GC.RUN_SIMULATION:
                self.step_simulation()
                self.stats.update_records()
                self.gc.TICKS += 1
            self.render_simulation()
            self.handler.process_input()

            if len(self.abm.agent_dict) == 0:
                self.reset_simulation()


if __name__ == '__main__':

    # Initialize simulation parameters and simulation itself.
    GC = GlobalConstants()
    simulation = Sugarscape(GC)

    # Start the Simulation and enjoy!
    simulation.run_main_loop()