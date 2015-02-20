"""
This module contains the class for a CA with hexagonal cells in pointy top layout.
"""

__author__ = 'Michael Wagner'

from ca.cab_cell import CellHex

import math


class CAHex:
    '''
    For reference go to "http://www.redblobgames.com/grids/hexagons/"
    Hex CA parameters:
    - even-r horizontal layout
    - cube coordinates for algorithms
    - axial coordinates for storage
    '''
    def __init__(self, gc, visualizer, proto_cell=None):
        """
        Initializes and returns the cellular automaton.
        The CA is a dictionary and not a list of lists
        :return: The initialized CA.
        """
        self.ca_grid = {}
        self.gc = gc
        self.grid_height = gc.GRID_HEIGHT
        self.grid_width = gc.GRID_WIDTH
        self.height = int(self.grid_height / gc.CELL_SIZE)
        self.width = int(self.grid_width / gc.CELL_SIZE)
        self.cell_size = gc.CELL_SIZE
        self.visualizer = visualizer
        self.use_borders = gc.USE_CA_BORDERS
        self.proto_cell = None

        if proto_cell is None:
            for j in range(0, self.height):
                for i in range(0, self.width):
                    # self.ca_grid[i, j] = CellHex(i, j, gc.CELL_SIZE, gc)
                    q = i-math.floor(j/2)
                    self.ca_grid[q, j] = CellHex(q, j, gc.CELL_SIZE, gc)
                    # print('x={0}, y={1}'.format(q, j))
                    if self.gc.USE_CA_BORDERS and (i == 0 or j == 0 or i == (self.width - 1) or j == (self.height - 1)):
                        self.ca_grid[q, j].is_border = True                    
        else:
            self.proto_cell = proto_cell
            for j in range(0, self.height):
                for i in range(0, self.width):
                    # self.ca_grid[i, j] = proto_cell.clone(i, j, gc.CELL_SIZE)
                    q = i-math.floor(j/2)
                    self.ca_grid[q, j] = proto_cell.clone(q, j, gc.CELL_SIZE)
                    # print('x={0}, y={1}'.format(q, j))
                    if self.gc.USE_CA_BORDERS and (i == 0 or j == 0 or i == (self.width - 1) or j == (self.height - 1)):
                        self.ca_grid[q, j].is_border = True

        for cell in list(self.ca_grid.values()):
            self.set_neighborhood(cell)

    def set_neighborhood(self, cell):
        cx, cy, cz = cell.get_cube()
        for d in self.gc.HEX_DIRECTIONS:
            x = cx + d[0]
            y = cy + d[1]
            if (x, y) in self.ca_grid:
                cell.neighbors.append(self.ca_grid[x, y])


    def draw_cells(self):
        """
        Simply iterating over all cells and calling their draw() method.
        """
        draw = self.visualizer.draw_cell
        for cell in self.ca_grid.values():
            draw(cell)

    def cycle_automaton(self):
        """
        This method updates the cellular automaton
        """
        self.update_cells_from_neighborhood()
        self.update_cells_state()

    def update_cells_from_neighborhood(self):
        for cell in self.ca_grid.values():
            cell.sense_neighborhood()

    def update_cells_state(self):
        """
        After executing update_neighs this is the actual update of the cell itself
        """
        for cell in self.ca_grid.values():
            cell.update()

    def get_agent_neighborhood(self, a_pos, agent_x, agent_y):
        """
        Creates a dictionary {'position': (cell, [agents on that cell])}
        for the calling agent to get an overview over its immediate surrounding.
        """
        x = int(agent_x / self.cell_size)
        y = int(agent_y / self.cell_size)
        neighborhood = {}
        for i in range(-1, 2):
            for j in range(-1, 2):
                grid_x = x + i
                grid_y = y + j
                if (grid_x, grid_y) in self.ca_grid and not (grid_x == 0 and grid_y == 0):
                    a = self.ca_grid[grid_x, grid_y]
                    if (grid_x, grid_y) not in a_pos:
                        b = False
                    else:
                        b = a_pos[grid_x, grid_y]
                    neighborhood[grid_x, grid_y] = (a, b)
        return neighborhood