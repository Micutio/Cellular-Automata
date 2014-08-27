__author__ = 'Michael Wagner'
__version__ = '1.0'


class GlobalConstants:
    def __init__(self):
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.NUM_AGENTS = 200
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
        self.ABM_BOUNDS = [(half_x, 50, 0, half_y), (0, half_x, half_y, 50)]
        self.TICKS = 1
        self.EXPERIMENT_RUN = 1
        self.MAX_MEASURED_TICKS = 0
        self.MS_PER_TICK = 60
        self.TRIBE_COLORS = {0: (0, 0, 0),
                             1: (200, 200, 200),
                             2: (178, 0, 127),
                             3: (0, 178, 127),
                             4: (178, 229, 51),
                             5: (150, 102, 25)}
        ################################
        #        ABM CONSTANTS         #
        ################################
        self.MIN_METABOLISM = 1
        self.MAX_METABOLISM = 4
        self.VISION = 6
        self.M_FERTILITY_START = 15
        self.F_FERTILITY_START = 15
        self.M_FERTILITY_END = (50, 60)
        self.F_FERTILITY_END = (40, 50)
        self.MAX_AGENT_LIFE = 100
        self.STARTING_SUGAR = (20, 40)
        self.IMMUNE_SYSTEM_GENOME_LENGTH = 5
        self.DISEASE_GENOME_LENGTH = 20
        ################################
        #         CA CONSTANTS         #
        ################################
        self.LANDSCAPE_MODE = 2  # 1 = randomized, 2 = procedural, 3 = two hills, 4 = use same as last time
        self.MAX_SUGAR = 4
        self.GROWTH_PER_TICK = 1
        self.GROWTH_PERIOD = 1
        self.TOROIDAL = False
        self.POLLUTION = False
        self.POLLUTION_COEFFICIENTS = (0.003, 0.004)
        self.MAX_POLLUTION = 10
        ################################
        #      UTILITY CONSTANTS       #
        ################################
        self.FILE_PATH = "./"