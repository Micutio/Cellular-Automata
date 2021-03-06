__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is a CA for a python implementation of Sugarscape.

# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"

from numpy import *

import colorsys
import random
import pygame
import copy

#########################################################################
###                       Global Variables                            ###
#########################################################################

# The Grid of the CA
# Cells = {}
# Dimensions of the grid
MAX_SUGAR = 4
GROWTH_PER_TICK = 1
GROWTH_PERIOD = 1
TOROIDAL = False

#########################################################################
###                            CLASSES                                ###
#########################################################################


class ClassCell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """

    def __init__(self, x, y, c_size, sugar, spice, growth, period):
        self.x = x
        self.y = y
        self.w = c_size
        self.h = c_size
        self.sugar = sugar
        self.spice = spice
        self.max_sugar = sugar
        self.max_spice = spice
        self.growth = growth
        self.sugar_period = period
        self.spice_period = period
        self.sugar_period_counter = 0
        self.spice_period_counter = 0

    @property
    def get_sugar(self):
        return self.sugar

    #def sense_neigh(self, neighbor):
    #    self.sugar = self.get_sugar()

    def update(self):
        """
        This method updates the sugar/spice amount per cell.
        """
        if self.sugar_period_counter >= self.sugar_period and self.sugar < self.max_sugar:
            self.sugar_period_counter = 0
            self.sugar += self.growth
        else:
            self.sugar_period_counter += 1

        if self.spice_period_counter >= self.spice_period and self.spice < self.max_spice:
            self.spice_period_counter = 0
            self.spice += self.growth
        else:
            self.spice_period_counter += 1

    def draw(self, surf):
        #print("new color: (%i,%i,%i)" % (red, green, blue))
        col = self.calculate_color()
        col2 = (col[0] * 0.9, col[1] * 0.9, col[2] * 0.9)
        pygame.draw.rect(surf, col, (self.x * self.w, self.y * self.h, self.w, self.h), 0)
        lx = self.x * self.w
        ly = self.y * self.h
        pygame.draw.line(surf, col2, [lx + 1, ly + self.w - 1], [lx + self.h - 1, ly + self.w - 1], int(self.w * 0.2))
        pygame.draw.line(surf, col2, [lx + self.h - 1, ly + 1], [lx + self.h - 1, ly + self.w - 1], int(self.w * 0.2))

    def calculate_color(self):
        if self.max_sugar == 0:
            normalized_su = 0
        else:
            normalized_su = self.sugar / MAX_SUGAR
        if self.max_spice == 0:
            normalized_sp = 0
        else:
            normalized_sp = self.spice / MAX_SUGAR

        green = 200 * normalized_su
        red = 150 * normalized_sp
        blue = 0
        return red, green, blue

    def highlight(self, surf):
        col = (255, 255, 255)
        pygame.draw.rect(surf, col, (self.x * self.w, self.y * self.h, self.w, self.h), 0)


class CA:
    def __init__(self, init_mode, grid_height, grid_width, cell_size):
        """
        Initializes and returns the cellular automaton.
        The CA is a dictionary and not a list of lists
        :return: The initialized CA.
        """
        self.ca_grid = {}
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.height = int(self.grid_height / cell_size)
        self.width = int(self.grid_width / cell_size)
        self.cell_size = cell_size
        self.season_count = 0
        self.season = 1

        if init_mode == 1:
            for i in range(0, self.height):
                for j in range(0, self.width):
                    self.ca_grid[i, j] = ClassCell(i, j, cell_size, random.randint(0, MAX_SUGAR), random.randint(0, MAX_SUGAR), GROWTH_PER_TICK, self.season)
        elif init_mode == 2:
            landscape_sugar = get_procedural_landscape()
            landscape_spice = get_procedural_landscape()
            for i in range(0, self.height):
                for j in range(0, self.width):
                    self.ca_grid[i, j] = ClassCell(i, j, cell_size, landscape_sugar[i][j], landscape_spice[i][j], GROWTH_PER_TICK, self.season)
        elif init_mode == 3:
            sugar_dist = get_two_hill_landscape()
            spice_dist = get_inverted_two_hill_landscape()
            for i in range(0, self.height):
                for j in range(0, self.width):
                    self.ca_grid[i, j] = ClassCell(i, j, cell_size, sugar_dist[i][j], spice_dist[j][i], GROWTH_PER_TICK, self.season)

    def draw_cells(self, screen):
        """
        Simply iterating over all cells and calling their draw() method.
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.ca_grid[x, y].draw(screen)

    def cycle_automaton(self):
        """
        This method updates the cellular automaton
        """
        # self.ca_grid = update_from_neighs(ca_grid)
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
        Here we use the von-Neuman neighborhood
        """
        x = int(agent_x / self.cell_size)
        y = int(agent_y / self.cell_size)
        visible_cells = []
        for i in range(-v, v + 1):
            # 1. go through horizontal line of sight
            grid_x = x + i
            agnt_x = ((grid_x * self.cell_size) + int(self.cell_size / 2))
            if (grid_x, y) in self.ca_grid:
                a = self.ca_grid[grid_x, y]
                if (agnt_x, agent_y) not in a_pos:
                    b = False
                else:
                    b = a_pos[agnt_x, agent_y]
                visible_cells.append((a, b))
            # 2. go through vertical line of sight
            grid_y = y + i
            agnt_y = ((grid_y * self.cell_size) + int(self.cell_size / 2))
            if (x, grid_y) in self.ca_grid:
                a = self.ca_grid[x, grid_y]
                if (agent_x, agnt_y) not in a_pos:
                    b = False
                else:
                    b = a_pos[agent_x, agnt_y]
                visible_cells.append((a, b))
        random.shuffle(visible_cells)
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

    def highlight_cell(self, screen, x, y):
        cx = int(x / self.cell_size)
        cy = int(y / self.cell_size)
        self.ca_grid[cx, cy].highlight(screen)

    def update_from_neighs(self):
        """
        Looping over all cells to gather all the neighbor information they need to update
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                if y - 1 > -1 and x - 1 > -1 and x + 1 < self.width and y + 1 < self.height:
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x - 1), (y - 1)])  # Top Left
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[x, (y - 1)])  # Top
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x + 1), (y - 1)])  # Top Right
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x - 1), (y + 1)])  # Bottom Left
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[x, (y + 1)])  # Bottom
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x + 1), (y + 1)])  # Bottom Right
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x - 1), y])  # Left
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x + 1), y])  # Right


#########################################################################
###                           OTHER METHODS                           ###
#########################################################################


def calculate_color_hsv(sugar, max_sugar):
    """
    Calculates the RGB values depending on the cell's current temperature.
    This method uses HSV ranges.
    :return:
    """
    if max_sugar == 0:
        normalized_v = 0
    else:
        normalized_v = sugar / max_sugar
    h = (1 - normalized_v) * 250
    red, green, blue = colorsys.hsv_to_rgb(h / 360, 1., 1.)
    return red * 255, green * 255, blue * 255


def calculate_color_simple(sugar, max_sugar):
    """
    Calculates the RGB values depending on the cell's current temperature.
    :return:
    """
    if max_sugar == 0:
        normalized_v = 0
    else:
        normalized_v = sugar / max_sugar
    red = 0
    green = 0
    blue = 0
    if 0 <= normalized_v <= 1 / 8:
        red = 0
        green = 0
        blue = 4 * normalized_v + 0.5
    elif 1 / 8 < normalized_v <= 3 / 8:
        red = 0
        green = 4 * normalized_v - 0.5
        blue = 1
    elif 3 / 8 < normalized_v <= 5 / 8:
        red = 4 * normalized_v - 1.5
        green = 1
        blue = -4 * normalized_v + 2.5
    elif 5 / 8 < normalized_v <= 7 / 8:
        red = 1
        green = -4 * normalized_v + 3.5
        blue = 0
    elif 7 / 8 < normalized_v <= 1:
        red = -4 * normalized_v + 4.5
        green = 0
        blue = 0
    else:
        pass

    return red * 255, green * 255, blue * 255


def get_procedural_landscape():
    landscape = [[0 for _ in range(50)] for _ in range(50)]
    # First step: plant some 'seeds' for hills
    num_hills = random.randint(5, 15)
    for _ in range(num_hills):
        rand_x = random.randint(0, 49)
        rand_y = random.randint(0, 49)
        landscape[rand_x][rand_y] = MAX_SUGAR
    for _ in range(50):
        for i in range(1, 49):
            for j in range(1, 49):
                c1 = landscape[i - 1][j]
                c2 = landscape[i + 1][j]
                c3 = landscape[i][j - 1]
                c4 = landscape[i][j + 1]
                choice = random.choice([c1, c2, c3, c4])
                if 0 < choice and landscape[i][j] < MAX_SUGAR:
                    landscape[i][j] = random.choice(range(1, choice + 1))
    return landscape


def get_inverted_two_hill_landscape():
    a = get_two_hill_landscape()
    a2 = copy.deepcopy(a)
    a3 = []
    for i in range(50):
        for j in range(50):
            a2[j][i] = a[i][j]
    for l in range(49, -1, -1):
        a3.append(a2[l])
    return a3


def get_two_hill_landscape():
    return [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2],
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