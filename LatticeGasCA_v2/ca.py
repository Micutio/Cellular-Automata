__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is a python prototype for a lattice gas automaton.
# Version 2 uses the Margolus neighborhood, which is a lot more accurate than
# the simple model.
# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"

import colorsys
#import math
#import time

import pygame

#########################################################################
###                       Global Variables                            ###
#########################################################################

# The Grid of the CA
#Cells = {}
# Dimensions of the grid
GRID_WIDTH = 500
GRID_HEIGHT = 500
MAX_POP = 4
RULE_LIST = [(0, 0, 0, 0),
             (1, 0, 0, 0),
             (0, 1, 0, 0),
             (1, 1, 0, 0),
             (0, 0, 1, 0),
             (1, 0, 1, 0),
             (0, 1, 1, 0),
             (1, 1, 1, 0),
             (0, 0, 0, 1),
             (1, 0, 0, 1),
             (0, 1, 0, 1),
             (1, 1, 0, 1),
             (0, 0, 1, 1),
             (1, 0, 1, 1),
             (0, 1, 1, 1),
             (1, 1, 1, 1)]

#########################################################################
###                            CLASSES                                ###
#########################################################################


class ClassCell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """
    def __init__(self, x, y, is_wall):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.pop = 0
        self.is_wall = is_wall

    def calculate_color(self):
        if self.is_wall:
            r = g = 255
            b = 0
        else:
            ratio = self.pop / MAX_POP
            r = 255 * ratio
            g = b = 0
        return r, g, b

    def draw(self, surf):
        #print("new color: (%i,%i,%i)" % (red, green, blue))
        #self.pop = self.cells.count(True)
        col = self.calculate_color()
        pygame.draw.rect(surf, col, (self.x * self.w, self.y * self.h, self.w, self.h), 0)


#########################################################################
###                          GLOBAL METHODS                           ###
#########################################################################
# The following methods are used to manipulate the CA grid

class LGCA:
    def __init__(self, rule_def):
        """
        Initializes and returns the cellular automaton.
        The CA is a dictionary and not a list of lists
        :return: The initialized CA.
        """
        self.ca_grid = {}
        self.switch = True
        self.rules = setup_rules(rule_def)
        height = int(GRID_HEIGHT / 10)
        width = int(GRID_WIDTH / 10)
        for y in range(0, height):
            for x in range(0, width):
                self.ca_grid[x, y] = ClassCell(x, y, False)
                #if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                #ca_grid[x, y].is_wall = True

    def create_walls(self):
        height = int(GRID_HEIGHT / 10)
        width = int(GRID_WIDTH / 10)
        for y in range(0, height):
            for x in range(0, width):
                if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                    self.ca_grid[x, y].is_wall = True
                    self.ca_grid[x, y].pop = 1

    def draw_cells(self, screen):
        for y in range(0, int(GRID_HEIGHT / 10)):
            for x in range(0, int(GRID_WIDTH / 10)):
                self.ca_grid[x, y].draw(screen)

    def cycle(self):
        #self.update_from_neighs(ca_grid)
        self.update_states()

    #########################################################################
    ###                    UPDATE FROM NEIGHBOR METHODS                   ###
    #########################################################################

    def update_from_neighs(self):
        """
        Looping over all cells to gather all the neighbor information they need to update
        """
        height = int(GRID_HEIGHT / 10)
        width = int(GRID_WIDTH / 10)
        for y in range(0, height):
            for x in range(0, width):
                for i in [(0, -1, 0, 2), (1, 0, 1, 3), (0, 1, 2, 0), (-1, 0, 3, 1)]:
                    if (x + i[0], y + i[1]) in self.ca_grid.keys():
                        self.ca_grid[x, y].sense_neigh(self.ca_grid[x + i[0], y + i[1]], i[2], i[3])

                    #########################################################################
                    ###                       UPDATE STATES METHODS                       ###
                    #########################################################################

    def update_states(self):
        """
        After executing update_neighs this is the actual update of the cell itself
        """
        height = int(GRID_HEIGHT / 10)
        width = int(GRID_WIDTH / 10)
        cells = [(0, 0), (1, 0), (0, 1), (1, 1)]
        if self.switch:
            i = 0
            j = 0
        else:
            i = -1
            j = -1
        self.switch = not self.switch
        for y in range(i, height, 2):
            for x in range(j, width, 2):
                if (x + cells[0][0], y + cells[0][1]) in self.ca_grid.keys():
                    c0 = self.ca_grid[x + cells[0][0], y + cells[0][1]].pop
                else:
                    c0 = 0
                if (x + cells[1][0], y + cells[1][1]) in self.ca_grid.keys():
                    c1 = self.ca_grid[x + cells[1][0], y + cells[1][1]].pop
                else:
                    c1 = 0
                if (x + cells[2][0], y + cells[2][1]) in self.ca_grid.keys():
                    c2 = self.ca_grid[x + cells[2][0], y + cells[2][1]].pop
                else:
                    c2 = 0
                if (x + cells[3][0], y + cells[3][1]) in self.ca_grid.keys():
                    c3 = self.ca_grid[x + cells[3][0], y + cells[3][1]].pop
                else:
                    c3 = 0
                new_pop = self.rules[c0, c1, c2, c3]
                if (x + cells[0][0], y + cells[0][1]) in self.ca_grid.keys() and not self.ca_grid[x + cells[0][0], y + cells[0][1]].is_wall:
                    self.ca_grid[x + cells[0][0], y + cells[0][1]].pop = new_pop[0]
                if (x + cells[1][0], y + cells[1][1]) in self.ca_grid.keys() and not self.ca_grid[x + cells[1][0], y + cells[1][1]].is_wall:
                    self.ca_grid[x + cells[1][0], y + cells[1][1]].pop = new_pop[1]
                if (x + cells[2][0], y + cells[2][1]) in self.ca_grid.keys() and not self.ca_grid[x + cells[2][0], y + cells[2][1]].is_wall:
                    self.ca_grid[x + cells[2][0], y + cells[2][1]].pop = new_pop[2]
                if (x + cells[3][0], y + cells[3][1]) in self.ca_grid.keys() and not self.ca_grid[x + cells[3][0], y + cells[3][1]].is_wall:
                    self.ca_grid[x + cells[3][0], y + cells[3][1]].pop = new_pop[3]
        return self.ca_grid


def setup_rules(rule_def):
    rule_set = {}
    for i in range(len(rule_def)):
        rule_set[RULE_LIST[i]] = RULE_LIST[rule_def[i]]
    return rule_set