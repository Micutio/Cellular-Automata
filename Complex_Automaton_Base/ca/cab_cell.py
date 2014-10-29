"""
This module contains all classes associated with the CA cells.
"""

__author__ = 'Michael Wagner'


class CACell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """
    def __init__(self, x, y, c_size, gc):
        self.x = x
        self.y = y
        self.w = c_size
        self.h = c_size
        self.gc = gc

    def sense_neighborhood(self, neighborhood):
        raise NotImplementedError("Method needs to be implemented")

    def update(self):
        raise NotImplementedError("Method needs to be implemented")

    def clone(self, x, y, c_size):
        return CACell(x, y, c_size, self.gc)