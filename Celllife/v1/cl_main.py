from v1.abm.cl_abm import ABM
from v1.ca.cl_ca import CA
from v1.cl_global_constants import GlobalConstants
from v1.util.cl_io_handling import EventHandler
from v1.util.cl_visualization import Visualization

__author__ = 'Michael Wagner'
__version__ = '1.0'


import pygame


class ForagingAnt:
    """
    The main class of Sugarscape. This controls everything.
    """

    def __init__(self, global_constants):
        """
        Standard initializer.
        :param global_constants: All constants or important variables that control the simulation.
        """
        self.gc = global_constants
        self.version = "09-2014"
        pygame.init()
        self.screen = pygame.display.set_mode((self.gc.GRID_WIDTH, self.gc.GRID_HEIGHT), pygame.RESIZABLE, 32)
        pygame.display.set_caption('CellLife Simulation')

        self.visualizer = Visualization(self.screen, self.gc)
        self.ca = CA(self.visualizer, self.gc)
        self.abm = ABM(self.visualizer, self.gc)
        self.handler = EventHandler(self)
        self.display_info()
        return

    def display_info(self):
        print("\n---------------------------[CELL LIFE SIMULATION]------------------------------"
              "\n > version " + self.version + ""
              "\n-------------------------------------------------------------------------------"
              "\n [COMMANDS]------------------------------------------------------------------- "
              "\n  [SIMULATION CONTROL]-------------------------------------------------------  "
              "\n   > [SPACE] pause/resume simulation"
              "\n   > [r] reset simulation"
              "\n   > [s] perform single simulation step"
              "\n  ---------------------------------------------------------------------------  "
              "\n                                                                               ")

    def reset_simulation(self):
        self.ca.__init__(self.visualizer, self.gc)
        self.abm.__init__(self.visualizer, self.gc)

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
            # This block performs a simulation step.
            if GC.RUN_SIMULATION:
                self.step_simulation()
            self.render_simulation()
            self.handler.process_input()


if __name__ == '__main__':

    # Initialize simulation parameters and simulation itself.
    GC = GlobalConstants()
    simulation = ForagingAnt(GC)

    # Start the Simulation and enjoy!
    simulation.run_main_loop()