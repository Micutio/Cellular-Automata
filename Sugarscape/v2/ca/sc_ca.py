__author__ = 'Michael Wagner'
__version__ = '1.0'

# This is a CA for a python implementation of Sugarscape.

# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"

from ca.sc_cell import ClassCell
from numpy import *
import random
import copy


class CA:
    def __init__(self, visualizer, gc, ls_sugar=None, ls_spice=None):
        """
        Initializes and returns the cellular automaton.
        The CA is a dictionary and not a list of lists
        :return: The initialized CA.
        """
        self.ca_grid = {}
        self.grid_height = gc.GRID_HEIGHT
        self.grid_width = gc.GRID_WIDTH
        self.height = int(self.grid_height / gc.CELL_SIZE)
        self.width = int(self.grid_width / gc.CELL_SIZE)
        self.cell_size = gc.CELL_SIZE
        self.season_count = 0
        self.season = 1
        self.visualizer = visualizer
        self.gc = gc
        self.landscape_sugar = []
        self.landscape_spice = []

        # In case we load a landscape from file, initialize sugar and spice accordingly.
        if ls_sugar and ls_spice:
            self.landscape_sugar = ls_sugar
            self.landscape_spice = ls_spice
        # Or else build up the landscape from scratch
        else:
            if gc.LANDSCAPE_MODE == 1:
                self.landscape_sugar = self.get_plain_landscape()
                self.landscape_spice = self.get_plain_landscape()
            elif gc.LANDSCAPE_MODE == 2:
                self.landscape_sugar = self.get_procedural_landscape()
                self.landscape_spice = self.get_procedural_landscape()
            elif gc.LANDSCAPE_MODE == 3:
                self.landscape_sugar = self.get_two_hill_landscape()
                self.landscape_spice = self.get_inverted_two_hill_landscape()

        for j in range(0, self.height):
            for i in range(0, self.width):
                self.ca_grid[i, j] = ClassCell(i, j, gc.CELL_SIZE, self.landscape_sugar[i][j],
                                               self.landscape_spice[i][j], gc.GROWTH_PER_TICK,
                                               self.season, gc.POLLUTION_COEFFICIENTS, gc.MAX_POLLUTION)

    def draw_cells(self):
        """
        Simply iterating over all cells and calling their draw() method.
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.visualizer.draw_cell(self.ca_grid[x, y])

    def cycle_automaton(self):
        """
        This method updates the cellular automaton
        """
        if self.gc.POLLUTION:
            self.update_from_neighs()
        self.update_states()
        self.switch_season()

    def switch_season(self):
        if self.season_count == 20:
            if self.season == 1:  # spring
                sugar_period = 2
                spice_period = 1
                self.season = 2
            elif self.season == 2:  # summer
                sugar_period = 1
                spice_period = 1
                self.season = 3
            elif self.season == 3:  # fall
                sugar_period = 1
                spice_period = 2
                self.season = 4
            else:  # winter
                sugar_period = 3
                spice_period = 3
                self.season = 1

            for y in range(0, self.height):
                for x in range(0, self.width):
                    self.ca_grid[x, y].sugar_period = sugar_period
                    self.ca_grid[x, y].spice_period = spice_period
            self.season_count = 0
        else:
            self.season_count += 1

    def update_states(self):
        """
        After executing update_neighs this is the actual update of the cell itself
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.ca_grid[x, y].update()

    def get_visible_cells(self, a_pos, agent_x, agent_y, v):
        """
        Delivers all cells that are in sight of cell(x,y) with sight range of v.
        Here we use the von-Neumann neighborhood
        """
        x = int(agent_x / self.cell_size)
        y = int(agent_y / self.cell_size)
        visible_cells = []
        for i in range(-v, v + 1):
            # 1. go through horizontal line of sight
            grid_x = x + i
            if (grid_x, y) in self.ca_grid:
                new_cell = self.ca_grid[grid_x, y]
                agnt_x = ((grid_x * self.cell_size) + int(self.cell_size / 2))
                if (agnt_x, agent_y) not in a_pos:
                    new_agent = False
                else:
                    new_agent = a_pos[agnt_x, agent_y]
                visible_cells.append((new_cell, new_agent))
            # 2. go through vertical line of sight. And this time skip your own cell,
            # because we already checked it in the horizontal line of sight
            grid_y = y + i
            if (x, grid_y) in self.ca_grid and i != 0:
                new_cell = self.ca_grid[x, grid_y]
                agnt_y = ((grid_y * self.cell_size) + int(self.cell_size / 2))
                if (agent_x, agnt_y) not in a_pos:
                    new_agent = False
                else:
                    new_agent = a_pos[agent_x, agnt_y]
                visible_cells.append((new_cell, new_agent))
        return visible_cells

    def get_neighborhood(self, a_pos, agent_x, agent_y):
        x = int(agent_x / self.cell_size)
        y = int(agent_y / self.cell_size)
        neighborhood = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                grid_x = x + i
                agnt_x = ((grid_x * self.cell_size) + int(self.cell_size / 2))
                grid_y = y + j
                agnt_y = ((grid_y * self.cell_size) + int(self.cell_size / 2))
                if (grid_x, grid_y) in self.ca_grid and not (grid_x == 0 and grid_y == 0):
                    a = self.ca_grid[grid_x, grid_y]
                    if (agnt_x, agnt_y) not in a_pos:
                        b = False
                    else:
                        b = a_pos[agnt_x, agnt_y]
                    neighborhood.append((a, b))
        return neighborhood

    def update_from_neighs(self):
        """
        Looping over all cells to gather all the neighbor information they need to update
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                if y - 1 > -1 and x - 1 > -1 and x + 1 < self.width and y + 1 < self.height:
                    #self.ca_grid[x, y].sense_neigh(self.ca_grid[(x - 1), (y - 1)])  # Top Left
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[x, (y - 1)])  # Top
                    #self.ca_grid[x, y].sense_neigh(self.ca_grid[(x + 1), (y - 1)])  # Top Right
                    #self.ca_grid[x, y].sense_neigh(self.ca_grid[(x - 1), (y + 1)])  # Bottom Left
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[x, (y + 1)])  # Bottom
                    #self.ca_grid[x, y].sense_neigh(self.ca_grid[(x + 1), (y + 1)])  # Bottom Right
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x - 1), y])  # Left
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x + 1), y])  # Right

    def get_plain_landscape(self):
        landscape = [[2 for _ in range(self.gc.dim_y)] for _ in range(self.gc.dim_x)]
        return landscape

    def get_procedural_landscape(self):
        landscape = [[0 for _ in range(self.gc.dim_y)] for _ in range(self.gc.dim_x)]
        # First step: plant some 'seeds' for hills
        num_hills = random.randint(5, 15)
        for _ in range(num_hills):
            rand_x = random.randint(0, self.gc.dim_x - 1)
            rand_y = random.randint(0, self.gc.dim_y - 1)
            landscape[rand_x][rand_y] = self.gc.MAX_SUGAR
        for _ in range(50):
            for j in range(1, self.gc.dim_y - 1):
                for i in range(1, self.gc.dim_x - 1):
                    c1 = landscape[i - 1][j]
                    c2 = landscape[i + 1][j]
                    c3 = landscape[i][j - 1]
                    c4 = landscape[i][j + 1]
                    choice = random.choice([c1, c2, c3, c4])
                    if 0 < choice and landscape[i][j] < self.gc.MAX_SUGAR:
                        landscape[i][j] = random.choice(range(1, choice + 1))
        return landscape

    def get_two_hill_landscape(self):
        a = two_hill_landscape
        a2 = copy.deepcopy(a)
        a3 = []
        for i in range(self.gc.dim_x):
            for j in range(self.gc.dim_y):
                try:
                    a2[i][j] = a[i][j]
                except IndexError:
                    a2[i][j] = 0
        for l in range(self.gc.dimx - 1, -1, -1):
            a3.append(a2[l])
        return a3

    def get_inverted_two_hill_landscape(self):
        a = two_hill_landscape
        a2 = copy.deepcopy(a)
        a3 = []
        for i in range(self.gc.dim_x):
            for j in range(self.gc.dim_y):
                try:
                    a2[j][i] = a[i][j]
                except IndexError:
                    a2[j][i] = 0
        for l in range(self.gc.dimx - 1, -1, -1):
            a3.append(a2[l])
        return a3


two_hill_landscape = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2],
[1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2],
[1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2],
[1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
[1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
[1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
[2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
[2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
[2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]