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
                    self.ca_grid[i-math.floor(j/2), j] = CellHex(i-math.floor(j/2), j, gc.CELL_SIZE, gc)
                    # print('x={0}, y={1}'.format(i-math.floor(j/2), j))
        else:
            self.proto_cell = proto_cell
            for j in range(0, self.height):
                for i in range(0, self.width):
                    # self.ca_grid[i, j] = proto_cell.clone(i, j, gc.CELL_SIZE)
                    self.ca_grid[i-math.floor(j/2), j] = proto_cell.clone(i-math.floor(j/2), j, gc.CELL_SIZE)
                    # print('x={0}, y={1}'.format(i-math.floor(j/2), j))

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

    def init_von_neumann(self):
        """
        Looping over all cells to gather the neighbor information they need to update.
        This method uses Von-Neumann-Neighborhood (except for borders which are dealt
        with by borders_von_neumann)
        This method is used for initializing neighbor references in the cells
        """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                neighbors = [self.ca_grid[x, (y - 1)],
                             self.ca_grid[x, (y + 1)],
                             self.ca_grid[(x - 1), y],
                             self.ca_grid[(x + 1), y]]
                self.ca_grid[x, y].set_neighbors(neighbors)

    def init_von_neumann_borders(self):
        """
        Going through all border-regions of the automaton to update them.
        This method is used for initializing neighbor references in the cells
        """
        w = self.width
        h = self.height
        for y in range(1, self.height - 1):
            neighbors_vn = [self.ca_grid[0, (y - 1)], self.ca_grid[0, (y + 1)], self.ca_grid[1, y]]
            self.ca_grid[0, y].set_neighbors(neighbors_vn)

            neighbors_vn = [self.ca_grid[(w - 1), (y - 1)], self.ca_grid[(w - 1), (y + 1)], self.ca_grid[(w - 2), y]]
            self.ca_grid[(w - 1), y].set_neighbors(neighbors_vn)

        for x in range(1, self.width - 1):
            neighbors_vn = [self.ca_grid[x, 1], self.ca_grid[(x - 1), 0], self.ca_grid[(x + 1), 0]]
            self.ca_grid[x, 0].set_neighbors(neighbors_vn)

            neighbors_vn = [self.ca_grid[x, (h - 2)], self.ca_grid[(x - 1), (h - 1)], self.ca_grid[(x + 1), (h - 1)]]
            self.ca_grid[x, (h - 1)].set_neighbors(neighbors_vn)

        # top left corner
        neighbors_vn = [self.ca_grid[0, 1], self.ca_grid[1, 0]]
        self.ca_grid[0, 0].set_neighbors(neighbors_vn)

        # top right corner
        neighbors_vn = [self.ca_grid[(w - 1), 1], self.ca_grid[(w - 2), 0]]
        self.ca_grid[(w - 1), 0].set_neighbors(neighbors_vn)

        # bottom left corner
        neighbors_vn = [self.ca_grid[0, (h - 2)], self.ca_grid[1, (h - 1)]]
        self.ca_grid[0, (h - 1)].set_neighbors(neighbors_vn)

        # bottom right corner
        neighbors_vn = [self.ca_grid[(w - 1), (h - 2)], self.ca_grid[(w - 2), (h - 1)]]
        self.ca_grid[(w - 1), (h - 1)].set_neighbors(neighbors_vn)

    def init_moore(self):
        """
        Looping over all cells to gather the neighbor information they need to update.
        This method uses Moore_neighborhood.  (except for borders which are dealt
        with by borders_moore)
        This method is used for initializing neighbor references in the cells

        """
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                neighbors = [self.ca_grid[x, (y - 1)],
                             self.ca_grid[x, (y + 1)],
                             self.ca_grid[(x - 1), y],
                             self.ca_grid[(x + 1), y],
                             self.ca_grid[(x - 1), (y - 1)],  # Top Left
                             self.ca_grid[(x + 1), (y - 1)],  # Top Right
                             self.ca_grid[(x - 1), (y + 1)],  # Bottom Left
                             self.ca_grid[(x + 1), (y + 1)]]  # Bottom Right
                self.ca_grid[x, y].set_neighbors(neighbors)

    def init_moore_borders(self):
        """
        Going through all border-regions of the automaton to update them.
        This method is used for initializing neighbor references in the cells

        """
        w = self.width
        h = self.height
        for y in range(1, self.height - 1):
            neighbors_mo = [self.ca_grid[0, (y - 1)], self.ca_grid[0, (y + 1)], self.ca_grid[1, y],
                            self.ca_grid[1, (y - 1)], self.ca_grid[1, (y + 1)]]
            self.ca_grid[0, y].set_neighbors(neighbors_mo)

            neighbors_mo = [self.ca_grid[(w - 1), (y - 1)], self.ca_grid[(w - 1), (y + 1)], self.ca_grid[(w - 2), y],
                            self.ca_grid[(w - 2), (y - 1)], self.ca_grid[(w - 2), (y + 1)]]
            self.ca_grid[(w - 1), y].set_neighbors(neighbors_mo)

        for x in range(1, self.width - 1):
            neighbors_mo = [self.ca_grid[x, 1], self.ca_grid[(x - 1), 0], self.ca_grid[(x + 1), 0],
                            self.ca_grid[(x - 1), 1], self.ca_grid[(x + 1), 1]]
            self.ca_grid[x, 0].set_neighbors(neighbors_mo)

            neighbors_mo = [self.ca_grid[x, (h - 2)], self.ca_grid[(x - 1), (h - 1)], self.ca_grid[(x + 1), (h - 1)],
                            self.ca_grid[(x - 1), (h - 2)], self.ca_grid[(x + 1), (h - 2)]]
            self.ca_grid[x, (h - 1)].set_neighbors(neighbors_mo)

        # top left corner
        neighbors_mo = [self.ca_grid[0, 1], self.ca_grid[1, 0], self.ca_grid[1, 1]]
        self.ca_grid[0, 0].set_neighbors(neighbors_mo)

        # top right corner
        neighbors_mo = [self.ca_grid[(w - 1), 1], self.ca_grid[(w - 2), 0], self.ca_grid[(w - 2), 1]]
        self.ca_grid[(w - 1), 0].set_neighbors(neighbors_mo)

        # bottom left corner
        neighbors_mo = [self.ca_grid[0, (h - 2)], self.ca_grid[1, (h - 1)], self.ca_grid[1, (h - 2)]]
        self.ca_grid[0, (h - 1)].set_neighbors(neighbors_mo)

        # bottom right corner
        neighbors_mo = [self.ca_grid[(w - 1), (h - 2)], self.ca_grid[(w - 2), (h - 1)], self.ca_grid[(w - 2), (h - 2)]]
        self.ca_grid[(w - 1), (h - 1)].set_neighbors(neighbors_mo)

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