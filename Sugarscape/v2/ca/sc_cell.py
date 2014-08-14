__author__ = 'Michael Wagner'
__version__ = '1.0'


class ClassCell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """

    def __init__(self, x, y, c_size, sugar, spice, growth, period, pollution_coefficients, max_pollution):
        """
        Standard initializer.
        """
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
        self.tribe_id = -1
        self.visits = 0
        self.pollution = 0
        self.num_neighs = 0
        self.neigh_pollution = 0.0
        self.pc = pollution_coefficients
        self.max_p = max_pollution

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

        if self.num_neighs > 0:
            self.pollution = min((self.neigh_pollution / self.num_neighs), self.max_p)
            self.num_neighs = 0
            self.neigh_pollution = 0

    def sense_neigh(self, neighbor):
        self.num_neighs += 1
        self.neigh_pollution += neighbor.pollution

    def pollute(self, production, metabolism):
        self.pollution += (self.pc[0] * production) + (self.pc[1] * metabolism)