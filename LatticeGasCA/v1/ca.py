#!/usr/bin/python

__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is a python prototype for a complex automaton, which
# integrates a CA and ABM. The CA is supposed to simulate heat emission
# of an object passing through the CA grid.

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

#########################################################################
###                            CLASSES                                ###
#########################################################################


class ClassCell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """
    def __init__(self, x, y, cells):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.cells = cells
        self.incoming = [False, False, False, False]
        self.pop = self.cells.count(True)
        self.is_wall = False

    def sense_neigh(self, neighbor, pos_inc, pos_out):
        """
        positions: 0 = north, 1 = east, 2 = south, 3 = west
        """
        self.incoming[pos_inc] = neighbor.cells[pos_out]

    def regulate(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        for i in range(len(self.incoming)):
            self.cells[i] = self.incoming[i]
        #self.cells = self.incoming
        if not self.is_wall:
            if (self.cells[0] and self.cells[2]) != (self.cells[1] and self.cells[3]):
                self.cells = [not c for c in self.cells]
            else:
                self.cells[0], self.cells[2] = self.cells[2], self.cells[0]
                self.cells[1], self.cells[3] = self.cells[3], self.cells[1]

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
        self.pop = self.cells.count(True)
        col = self.calculate_color()
        pygame.draw.rect(surf, col, (self.x * self.w, self.y * self.h, self.w, self.h), 0)


#########################################################################
###                          GLOBAL METHODS                           ###
#########################################################################
# The following methods are used to manipulate the CA grid


def draw_cells(ca_grid, screen):
    for y in range(0, int(GRID_HEIGHT / 10)):
        for x in range(0, int(GRID_WIDTH / 10)):
            ca_grid[x, y].draw(screen)


def init_ca():
    """
    Initializes and returns the cellular automaton.
    The CA is a dictionary and not a list of lists
    :return: The initialized CA.
    """
    ca_grid = {}
    height = int(GRID_HEIGHT / 10)
    width = int(GRID_WIDTH / 10)
    for y in range(0, height):
        for x in range(0, width):
            ca_grid[x, y] = ClassCell(x, y, [False, False, False, False])
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                ca_grid[x, y].is_wall = True
    return ca_grid


def cycle_ca(ca_grid):
    ca_grid = update_from_neighs(ca_grid)
    ca_grid = update_states(ca_grid)
    return ca_grid


#########################################################################
###                    UPDATE FROM NEIGHBOR METHODS                   ###
#########################################################################


def update_from_neighs(ca_grid):
    """
    Looping over all cells to gather all the neighbor information they need to update
    """
    height = int(GRID_HEIGHT / 10)
    width = int(GRID_WIDTH / 10)
    for y in range(0, height):
        for x in range(0, width):
            for i in [(0, -1, 0, 2), (1, 0, 1, 3), (0, 1, 2, 0), (-1, 0, 3, 1)]:
                if (x + i[0], y + i[1]) in ca_grid.keys():
                    ca_grid[x, y].sense_neigh(ca_grid[x + i[0], y + i[1]], i[2], i[3])
    return ca_grid


#########################################################################
###                       UPDATE STATES METHODS                       ###
#########################################################################


def update_states(ca_grid):
    """
    After executing update_neighs this is the actual update of the cell itself
    """
    height = int(GRID_HEIGHT / 10)
    width = int(GRID_WIDTH / 10)
    for y in range(0, height):
        for x in range(0, width):
            ca_grid[x, y].regulate()
    return ca_grid