from v1.ca.fa_cell import ClassCell

__author__ = 'Michael Wagner'
__version__ = '2.0'


class CA:
    def __init__(self, visualizer, gc):
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

        for j in range(0, self.height):
            for i in range(0, self.width):
                self.ca_grid[i, j] = ClassCell(i, j, gc.CELL_SIZE, gc.IN_FLUX, gc.OUT_FLUX, 0, False)

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
        # self.update_from_neighbors()
        self.update_states()

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

    def highlight_cell(self, screen, x, y):
        cx = int(x / 10)
        cy = int(y / 10)
        self.ca_grid[cx, cy].highlight(screen)

    def update_from_neighbors(self):
        """
        Looping over all cells to gather all the neighbor information they need to update
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                if y - 1 > -1 and x - 1 > -1 and x + 1 < self.width and y + 1 < self.height:
                    self.ca_grid[x, y].sense_neighbor(self.ca_grid[(x - 1), (y - 1)])  # Top Left
                    self.ca_grid[x, y].sense_neighbor(self.ca_grid[x, (y - 1)])  # Top
                    self.ca_grid[x, y].sense_neighbor(self.ca_grid[(x + 1), (y - 1)])  # Top Right
                    self.ca_grid[x, y].sense_neighbor(self.ca_grid[(x - 1), (y + 1)])  # Bottom Left
                    self.ca_grid[x, y].sense_neighbor(self.ca_grid[x, (y + 1)])  # Bottom
                    self.ca_grid[x, y].sense_neighbor(self.ca_grid[(x + 1), (y + 1)])  # Bottom Right
                    self.ca_grid[x, y].sense_neighbor(self.ca_grid[(x - 1), y])  # Left
                    self.ca_grid[x, y].sense_neighbor(self.ca_grid[(x + 1), y])  # Right