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
                self.ca_grid[i, j] = ClassCell(i, j, gc.CELL_SIZE, gc.DIFFUSION, gc.EVAPORATION, gc.MAX_PHEROMONE, 0,
                                               False)

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
        self.update_from_neighbors()
        self.update_borders_from_neighs()
        self.update_states()

    def update_states(self):
        """
        After executing update_neighs this is the actual update of the cell itself
        """
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.ca_grid[x, y].update()

    def get_neighborhood(self, a_pos, agent_x, agent_y):
        """
        Creates a dictionary {'position': (cell, [agents on that cell])} for the agent
        to get an overview over its immediate surrounding.
        """
        x = int(agent_x / self.cell_size)
        y = int(agent_y / self.cell_size)
        neighborhood = {}
        for i in range(-1, 2):
            for j in range(-1, 2):
                grid_x = x + i
                # agnt_x = ((grid_x * self.cell_size) + int(self.cell_size / 2))
                grid_y = y + j
                # agnt_y = ((grid_y * self.cell_size) + int(self.cell_size / 2))
                if (grid_x, grid_y) in self.ca_grid and not (grid_x == 0 and grid_y == 0):
                    a = self.ca_grid[grid_x, grid_y]
                    # if (agnt_x, agnt_y) not in a_pos:
                    if (grid_x, grid_y) not in a_pos:
                        b = False
                    else:
                        # b = a_pos[agnt_x, agnt_y]
                        b = a_pos[grid_x, grid_y]
                    neighborhood[grid_x, grid_y] = (a, b)
        return neighborhood

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

    def update_borders_from_neighs(self):
        """
        Going through all border-regions of the automaton to update them
        """
        for y in range(0, self.height):
            if y - 1 > -1 and y + 1 < self.height:
                # leftmost column
                self.ca_grid[0, y].sense_neighbor(self.ca_grid[0, (y - 1)])  # Top
                self.ca_grid[0, y].sense_neighbor(self.ca_grid[1, (y - 1)])  # Top Right
                self.ca_grid[0, y].sense_neighbor(self.ca_grid[0, (y + 1)])  # Bottom
                self.ca_grid[0, y].sense_neighbor(self.ca_grid[1, (y + 1)])  # Bottom Right
                self.ca_grid[0, y].sense_neighbor(self.ca_grid[1, y])  # Right
    
                # rightmost column
                self.ca_grid[(self.width - 1), y].sense_neighbor(self.ca_grid[(self.width - 2), (y - 1)])  # Top Left
                self.ca_grid[(self.width - 1), y].sense_neighbor(self.ca_grid[(self.width - 1), (y - 1)])  # Top
                self.ca_grid[(self.width - 1), y].sense_neighbor(self.ca_grid[(self.width - 2), (y + 1)])  # Bottom Left
                self.ca_grid[(self.width - 1), y].sense_neighbor(self.ca_grid[(self.width - 1), (y + 1)])  # Bottom
                self.ca_grid[(self.width - 1), y].sense_neighbor(self.ca_grid[(self.width - 2), y])  # Left
    
        for x in range(0, self.width):
            if x - 1 > -1 and x + 1 < self.width:
                # top row
                self.ca_grid[x, 0].sense_neighbor(self.ca_grid[(x - 1), 1])  # Bottom Left
                self.ca_grid[x, 0].sense_neighbor(self.ca_grid[x, 1])  # Bottom
                self.ca_grid[x, 0].sense_neighbor(self.ca_grid[(x + 1), 1])  # Bottom Right
                self.ca_grid[x, 0].sense_neighbor(self.ca_grid[(x - 1), 0])  # Left
                self.ca_grid[x, 0].sense_neighbor(self.ca_grid[(x + 1), 0])  # Right
                # bottom row
                self.ca_grid[x, (self.height - 1)].sense_neighbor(self.ca_grid[(x - 1), (self.height - 2)])  # Top Left
                self.ca_grid[x, (self.height - 1)].sense_neighbor(self.ca_grid[x, (self.height - 2)])  # Top
                self.ca_grid[x, (self.height - 1)].sense_neighbor(self.ca_grid[(x + 1), (self.height - 2)])  # Top Right
                self.ca_grid[x, (self.height - 1)].sense_neighbor(self.ca_grid[(x - 1), (self.height - 1)])  # Left
                self.ca_grid[x, (self.height - 1)].sense_neighbor(self.ca_grid[(x + 1), (self.height - 1)])  # Right
    
        # top left corner
        self.ca_grid[0, 0].sense_neighbor(self.ca_grid[0, 1])  # Bottom
        self.ca_grid[0, 0].sense_neighbor(self.ca_grid[1, 1])  # Bottom Right
        self.ca_grid[0, 0].sense_neighbor(self.ca_grid[1, 0])  # Right
    
        # top right corner
        self.ca_grid[(self.width - 1), 0].sense_neighbor(self.ca_grid[(self.width - 2), 1])  # Bottom Left
        self.ca_grid[(self.width - 1), 0].sense_neighbor(self.ca_grid[(self.width - 1), 1])  # Bottom
        self.ca_grid[(self.width - 1), 0].sense_neighbor(self.ca_grid[(self.width - 2), 0])  # Left
    
        # bottom left corner
        self.ca_grid[0, (self.height - 1)].sense_neighbor(self.ca_grid[0, (self.height - 2)])  # Top
        self.ca_grid[0, (self.height - 1)].sense_neighbor(self.ca_grid[1, (self.height - 2)])  # Top Right
        self.ca_grid[0, (self.height - 1)].sense_neighbor(self.ca_grid[1, (self.height - 1)])  # Right
    
        # bottom right corner
        # Top Left
        self.ca_grid[(self.width - 1), (self.height - 1)].sense_neighbor(self.ca_grid[(self.width - 2), (self.height - 2)])
        # Top
        self.ca_grid[(self.width - 1), (self.height - 1)].sense_neighbor(self.ca_grid[(self.width - 1), (self.height - 2)])
        #Left
        self.ca_grid[(self.width - 1), (self.height - 1)].sense_neighbor(self.ca_grid[(self.width - 2), (self.height - 1)])