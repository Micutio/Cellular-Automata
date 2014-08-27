__author__ = 'Michael Wagner'
__version__ = '2.0'

import math


class ClassCell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """

    def __init__(self, x, y, c_size, in_flux, out_flux, food, is_hive):
        self.x = x
        self.y = y
        self.w = c_size
        self.h = c_size
        self.in_flux = in_flux
        self.out_flux = out_flux
        self.pheromones = [0, 0]
        self.neighbor_pheromones = [0, 0]
        self.num_neighbors = 0
        self.food = food
        self.is_hive = is_hive

    def sense_neighbor(self, neigh):
        self.num_neighbors += 1
        for i in range(len(neigh)):
            self.neighbor_pheromones[i] += neigh.pheromones[i]

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        if self.num_neighbors > 0:
            for i in range(len(self.pheromones)):
                avg = self.pheromones[i] / self.num_neighbors
                # This cells pheromone amount is greater than in the surrounding
                # We have a pheromone flux out this cell.
                if self.pheromones[i] > avg:
                    self.pheromones[i] = math.floor(self.out_flux * (self.pheromones[i] - avg))
                # This cells pheromone amount is lesser than in the surrounding
                # We have an influx of pheromone
                else:
                    self.pheromones[i] = math.floor(self.in_flux * (avg - self.pheromones[i]))
        # Reset the control variables for the next round.
        self.num_neighbors = 0
        self.neighbor_pheromones = [0, 0]