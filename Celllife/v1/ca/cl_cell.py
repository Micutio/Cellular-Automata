__author__ = 'Michael Wagner'


from cab_cell import CACell


class CellLifeCell(CACell):
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """

    def __init__(self, x, y, c_size, gc):
        super().__init__(x, y, c_size, gc)
        self.diffusion = gc.DIFFUSION
        self.evaporation = gc.EVAPORATION
        self.o2 = 0.0
        self.co2 = 0.0
        self.new_o2 = 0
        self.new_co2 = 0
        self.is_persistent = False
        #self.neighbor_values = {"o2": 0, "co2": 0, "h2o": 0, "glucose": 0}

    def sense_neighborhood(self, neighbors):
        neigh_o2 = 0.0
        neigh_co2 = 0.0
        num_neighbors = 0
        if not self.is_persistent:
            for n in neighbors:
                if not n.is_persistent:
                    num_neighbors += 1
                    neigh_o2 += n.o2
                    neigh_co2 += n.co2

            if num_neighbors > 0:
                avg_o2 = neigh_o2 / num_neighbors
                avg_co2 = neigh_co2 / num_neighbors
                self.new_o2 = (1.0 - (self.evaporation * 10)) * (self.o2 + (self.diffusion * 10) * (avg_o2 - self.o2))
                self.new_co2 = (1.0 - self.evaporation * 10) * (self.co2 + (self.diffusion * 10) * (avg_co2 - self.co2))

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        self.o2 = self.new_o2
        self.co2 = self.new_co2