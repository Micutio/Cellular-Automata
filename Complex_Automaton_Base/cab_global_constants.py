"""
Put a short description here
"""

__author__ = 'Michael Wagner'


class GlobalConstants:
    def __init__(self):
        self.VERSION = "version: 09-2014"
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.TIME_STEP = 0
        self.ONE_AGENT_PER_CELL = False
        ################################
        #         CA CONSTANTS         #
        ################################
        self.USE_MOORE_NEIGHBORHOOD = True
        self.USE_CA_BORDERS = True
        self.DIM_X = 50  # How many cells is the ca wide?
        self.DIM_Y = 50  # How many cells is the ca high?
        self.CELL_SIZE = 15  # How long/wide is one cell?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        ################################
        # Specifically for HEX CAs     #
        ################################
        self.HEX_DIRECTIONS = [(+1, -1, 0), (+1, 0, -1), (0, +1, -1),
                               (-1, +1, 0), (-1, 0, +1), (0, -1, +1)]
        ################################
        #        ABM CONSTANTS         #
        ################################
        ################################
        #      UTILITY CONSTANTS       #
        ################################