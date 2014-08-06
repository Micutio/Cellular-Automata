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
import random

#########################################################################
###                       Global Variables                            ###
#########################################################################

MAX_TEMPERATURE = 100

#########################################################################
###                            CLASSES                                ###
#########################################################################


class ClassCell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """
    def __init__(self, x, y, persist):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 10
        self.temperature = 0
        self.neighbor_count = 0
        self.persist = persist

    def inc_temperature(self):
        if self.temperature < MAX_TEMPERATURE:
            self.temperature += 1

    def sense_neigh(self, neighbor):
        if neighbor.temperature > 0:
            self.neighbor_count += 1

    def regulate(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        ratio = (self.neighbor_count / 8)
        if (self.temperature == 0 and random.random() < ratio / 10) or (self.temperature > 0 and not self.persist):
            self.temperature = ratio * 100

    @property
    def calculate_color_hsv(self):
        """
        Calculates the RGB values depending on the cell's current temperature.
        This method uses HSV ranges.
        :return:
        """
        h = (1 - (self.temperature / MAX_TEMPERATURE)) * 250
        red, green, blue = colorsys.hsv_to_rgb(h / 360, 1., 1.)
        return red * 255, green * 255, blue * 255

    def calculate_color(self):
        """
        Calculates the RGB values depending on the cell's current temperature.
        :return:
        """
        normalized_v = self.temperature / MAX_TEMPERATURE
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

    def draw(self, surf):
        #print("new color: (%i,%i,%i)" % (red, green, blue))
        col = self.calculate_color()
        pygame.draw.rect(surf, col, (self.x * self.w, self.y * self.h, self.w, self.h), 0)

        col = self.calculate_color()
        col2 = (col[0] * 0.6, col[1] * 0.6, col[2] * 0.6)
        lx = self.x * self.w
        ly = self.y * self.h
        thick = self.neighbor_count
        pygame.draw.line(surf, col2, [lx + 1, ly + 9], [lx + 9, ly + 9], thick)
        pygame.draw.line(surf, col2, [lx + 9, ly + 1], [lx + 9, ly + 9], thick)
        self.neighbor_count = 0


class CellularAutomaton:
    """
    Encapsulates all functions for a cellular automaton.
    """

    def __init__(self, g_width, g_height, c_size):
        """
        Initializes and returns the cellular automaton.
        The CA is a dictionary and not a list of lists
        :return: The initialized CA.
        """
        self.ca_grid = {}
        self.width = int(g_width / c_size)
        self.height = int(g_height / c_size)
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.ca_grid[x, y] = ClassCell(x, y, False)

    def cycle_ca(self):
        """
        Performs one simulation step
        """
        self.update_from_neighs()
        self.update_states()

    def update_from_neighs(self):
        """
        Looping over all cells to gather all the neighbor information they need to update
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                if y - 1 > -1 and x - 1 > -1 and x + 1 < self.width and y + 1 < self.height:
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x - 1), (y - 1)])  #Top Left
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[x, (y - 1)])  #Top
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x + 1), (y - 1)])  #Top Right
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x - 1), (y + 1)])  #Bottom Left
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[x, (y + 1)])  #Bottom
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x + 1), (y + 1)])  #Bottom Right
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x - 1), y])  #Left
                    self.ca_grid[x, y].sense_neigh(self.ca_grid[(x + 1), y])  #Right

    def update_states(self):
        """
        After executing update_neighs this is the actual update of the cell itself
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.ca_grid[x, y].regulate()

    def draw_cells(self, screen):
        for y in range(0, self.height):
            for x in range(0, int(self.width)):
                self.ca_grid[x, y].draw(screen)

    def get_cells_around(self, x, y):
        result = []
        moves = [(-1, 0), (1, 0), (0, 0), (0, -1), (0, 1)]
        for m in moves:
            if (x + m[0], y + m[1]) in self.ca_grid:
                result.append(self.ca_grid[x + m[0], y + m[1]])
        return result