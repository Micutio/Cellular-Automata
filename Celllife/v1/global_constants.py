__author__ = 'Michael Wagner'

from cab_global_constants import GlobalConstants


class CellLifeGC(GlobalConstants):
    def __init__(self):
        super().__init__()
        self.VERSION = "version: 09-2014"
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.ONE_AGENT_PER_CELL = False
        ################################
        #         CA CONSTANTS         #
        ################################
        # Default properties
        self.USE_MOORE_NEIGHBORHOOD = True
        self.USE_CA_BORDERS = False
        self.DIM_X = 50  # How many cells is the ca wide?
        self.DIM_Y = 50  # How many cells is the ca high?
        self.CELL_SIZE = 15  # How long/wide is one cell?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        # Simulation specific properties
        self.DIFFUSION = 0.01
        self.EVAPORATION = 0.01
        ################################
        #        ABM CONSTANTS         #
        ################################
        ################################
        #      UTILITY CONSTANTS       #
        ################################