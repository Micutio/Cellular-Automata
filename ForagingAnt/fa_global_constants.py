__author__ = 'Michael Wagner'
__version__ = '1.0'


class GlobalConstants:
    def __init__(self):
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.MAX_ANTS = 50
        self.CELL_SIZE = 20
        self.DIM_X = 50  # How many cells is the ca wide?
        self.DIM_Y = 50  # How many cells is the ca high?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        # ABM_BOUNDS (x1, x2, y1, y2) describe a rectangle spanning
        # between the two points (x1, y1) and (x2, y2)
        # We use two rectangles to mark the areas the agents are spawning in.
        ################################
        #        ABM CONSTANTS         #
        ################################
        self.VISION = 1
        self.MAX_PHEROMONE = 100
        self.MAX_FOOD = 10000
        ################################
        #         CA CONSTANTS         #
        ################################
        self.DIFFUSION = 0.001
        self.EVAPORATION = 0.001
        ################################
        #      UTILITY CONSTANTS       #
        ################################