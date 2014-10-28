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
        ################################
        #        ABM CONSTANTS         #
        ################################
        self.NUM_AGENTS = 100
        ################################
        #         CA CONSTANTS         #
        ################################
        self.USE_MOORE_NEIGHBORHOOD = True
        self.DIM_X = 50  # How many cells is the ca wide?
        self.DIM_Y = 50  # How many cells is the ca high?
        self.CELL_SIZE = 15
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        ################################
        #      UTILITY CONSTANTS       #
        ################################