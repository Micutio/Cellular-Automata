__author__ = 'Michael Wagner'
__version__ = '1.0'


class GlobalConstants:
    def __init__(self):
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.NUM_AGENTS = 25
        self.NUM_TRIBES = 2
        self.CELL_SIZE = 12
        self.DIM_X = 50  # How many cells is the ca wide?
        self.DIM_Y = 50  # How many cells is the ca high?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        # ABM_BOUNDS (x1, x2, y1, y2) describe a rectangle spanning
        # between the two points (x1, y1) and (x2, y2)
        # We use two rectangles to mark the areas the agents are spawning in.
        half_x = int(self.DIM_X / 2)
        half_y = int(self.DIM_Y / 2)
        self.ABM_BOUNDS = [(half_x, self.DIM_X, 0, half_y), (0, half_x, half_y, self.DIM_Y)]
        ################################
        #        ABM CONSTANTS         #
        ################################
        self.VISION = 1
        ################################
        #         CA CONSTANTS         #
        ################################
        self.MAX_PHEROMONE = 100
        self.MAX_FOOD = 100
        self.IN_FLUX = 0.1
        self.OUT_FLUX = 0.1
        ################################
        #      UTILITY CONSTANTS       #
        ################################