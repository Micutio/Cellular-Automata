__author__ = 'Michael Wagner'
__version__ = '1.0'


class GlobalConstants:
    def __init__(self):
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.NUM_AGENTS = 200
        self.NUM_TRIBES = 2
        self.LANDSCAPE_MODE = 3  # 3 = two hills, 2 = procedural, 1 = randomized
        self.RUN_SIMULATION = False
        self.CELL_SIZE = 10
        self.GRID_WIDTH = int(500 / 10) * self.CELL_SIZE
        self.GRID_HEIGHT = int(500 / 10) * self.CELL_SIZE
        #self.ABM_BOUNDS = (0, 10, 40, 50)
        #self.ABM_BOUNDS = (0, 50, 0, 50)
        self.ABM_BOUNDS = (15, 35, 15, 35)
        self.TICKS = 1
        self.MS_PER_TICK = 60
        self.TRIBE_COLORS = {0: (0, 0, 0),
                             1: (255, 255, 255),
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
        ################################
        #         CA CONSTANTS         #
        ################################
        self.MAX_SUGAR = 4
        self.GROWTH_PER_TICK = 1
        self.GROWTH_PERIOD = 1
        self.TOROIDAL = False