__author__ = 'Michael Wagner'
__version__ = '1.0'

# This is a python prototype for a complex automaton, which
# integrates a CA and ABM. Together they form the SugarScape.

# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"

# Also thanks to David Grotzki for comprehensive advice on biology and especially genetics.

import pygame
import random
import time

from abm.sc_abm import ABM
from ca.sc_ca import CA
from util.sc_stat import Statistics
from sc_global_constants import GlobalConstants
from util.sc_visualization import Visualization
from util.sc_io_handling import EventHandler, Terminal

# TODO: Add loaning and inheritable colors to the agents.


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

        # Init random seed
        random.seed(a="Sugarscape", version=2)
        # Save random state at the beginning of the run in case
        # we want to save and load the exact same sim instance later.
        self.random_state = random.getstate()
        self.terminal = Terminal()

        pygame.init()
        width = self.gc.DIM_X * self.gc.CELL_SIZE
        height = self.gc.DIM_Y * self.gc.CELL_SIZE
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE, 32)
        pygame.display.set_caption('Sugarscape Simulation')

        self.visualizer = Visualization(self.screen, self.gc)
        self.ca = CA(self.visualizer, self.gc)
        self.abm = ABM(self.visualizer, self.gc)
        self.handler = EventHandler(self)
        self.stats = Statistics(self.abm, self.ca, self.gc)
        self.display_info()
        return

    def display_info(self):
        print("\n--------------------------[SUGARSCAPE SIMULATION]------------------------------"
              "\n > version 08-2014                                                             "
              "\n-------------------------------------------------------------------------------"
              "\n [COMMANDS]------------------------------------------------------------------- "
              "\n  [RENDERING]----------------------------------------------------------------  "
              "\n   > [0] no rendering at all (speeds up the simulation)                        "
              "\n   > [1] cells show resources                                                  "
              "\n   > [2] cells show tribal territories                                         "
              "\n   > [3] cells show population density                                         "
              "\n   > [5] cells show pollution                                                  "
              "\n   > [CTRL] + [1] agents show age, gender and tribe                            "
              "\n   > [CTRL] + [2] agents show tribe                                            "
              "\n   > [CTRL] + [3] agents show gender                                           "
              "\n   > [CTRL] + [4] agents show diseases                                         "
              "\n                                                                               "
              "\n  [SIMULATION CONTROL]-------------------------------------------------------  "
              "\n   > [SPACE] pause/resume simulation                                           "
              "\n   > [RIGHT MOUSE BUTTON] infect agent with disease (default=bacteria)         "
              "\n   > [b] set disease infection on mouse click to 'bacteria'                    "
              "\n   > [v] set disease infection on mouse click to 'virus'                       "
              "\n   > [SHIFT] + [1] initialize next run with plain resource distribution        "
              "\n   > [SHIFT] + [2] initialize next run with random resource distribution       "
              "\n   > [SHIFT] + [3] initialize next run with classic 'two-hill' resource dist.  "
              "\n   > [CTRL] + [s] save simulation configuration into file                      "
              "\n   > [CTRL] + [l] load simulation configuration from file                      "
              "\n                                                                               "
              "\n  [SIMULATION INFO]----------------------------------------------------------  "
              "\n   > [LEFT MOUSE BUTTON] show information about selected cell and agent        "
              "\n   > [i] show simulation statistics                                            "
              "\n   > [p] plot graphs with statistics and additional information                "
              "\n  ---------------------------------------------------------------------------  "
              "\n                                                                               ")

    def step_simulation(self):
        self.abm.cycle_system(self.ca)
        self.ca.cycle_automaton()

    def render_simulation(self):
        self.ca.draw_cells()
        self.abm.draw_agents()
        pygame.display.flip()

    def reset_simulation(self, loaded=False):
        # Finalize current simulation run.
        self.gc.EXPERIMENT_RUN += 1
        # Important for experiments: in case we found a configuration tha ran longer than all before, save it!
        if self.gc.TICKS > self.gc.MAX_MEASURED_TICKS:
            self.gc.MAX_MEASURED_TICKS = self.gc.TICKS
            self.handler.save_sim_status_to_file()

        # Print out some information about the reset.
        print("[SIMULATION][SYSTEM]---------------------------------------------------------")
        print(" > simulation ended after %i ticks (longest ever recorded: %i)"
              % (self.gc.TICKS, self.gc.MAX_MEASURED_TICKS))
        print(" > starting experiment run %i" % self.gc.EXPERIMENT_RUN)
        print("-----------------------------------------------------------------------------")
        self.gc.TICKS = 0

        # Save random state at the beginning of the run in case
        # we want to save and load the exact same sim instance later.
        self.random_state = random.getstate()
        # In case the simulation is reset to load previously saved one, the loaded values are applied.
        if loaded:
            random.setstate(loaded["random_state"])
            self.ca.__init__(self.visualizer, self.gc, ls_sugar=loaded["ca_sugar"], ls_spice=loaded["ca_spice"])
        # In case we have landscape mode 4, use the same configuration as last time.
        elif self.gc.LANDSCAPE_MODE == 4:
            self.ca.__init__(self.visualizer, self.gc, self.ca.landscape_sugar, self.ca.landscape_spice)
        # Or else initialize completely new landscape
        else:
            self.ca.__init__(self.visualizer, self.gc)
        self.abm.__init__(self.visualizer, self.gc)
        self.stats.__init__(self.abm, self.ca, self.gc)

    def run_main_loop(self):
        """
        Main method. It executes the CA.
        """

        print("------------------------------[SIMULATION LOG]---------------------------------\n"
              "                                                                               ")

        while 1:
            #t1 = time.time()
            # This block performs a simulation step.
            if GC.RUN_SIMULATION:
                self.step_simulation()
                self.stats.update_records()
                self.gc.TICKS += 1
            self.render_simulation()
            self.handler.process_input()

            if len(self.abm.agent_dict) == 0:
                self.reset_simulation()
            #t2 = time.time()
            #print("> time per cycle: {0:.5}".format(t2 - t1))


if __name__ == '__main__':

    # Initialize simulation parameters and simulation itself.
    GC = GlobalConstants()
    simulation = Sugarscape(GC)

    # Start the Simulation and enjoy!
    simulation.run_main_loop()