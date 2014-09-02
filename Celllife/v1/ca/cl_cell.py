__author__ = 'Michael Wagner'
__version__ = '2.0'


class ClassCell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """

    def __init__(self, x, y, c_size, diffusion, evaporation):
        self.x = x
        self.y = y
        self.w = c_size
        self.h = c_size
        self.diffusion = diffusion
        self.evaporation = evaporation
        self.num_neighbors = 0
        self.co2 = 1
        self.light = 1
        self.h2o = 1
        self.o2 = 0
        self.glucose = 0
        self.neighbors_o2 = 0
        self.neighbors_co2 = 0
        self.neighbors_h2o = 0
        self.neighbors_glucose = 0
        self.is_persistent = False
        #self.neighbor_values = {"o2": 0, "co2": 0, "h2o": 0, "glucose": 0}

    def sense_neighbor(self, neigh):
        if not self.is_persistent:
            self.num_neighbors += 1
            self.neighbors_o2 += neigh.o2
            self.neighbors_co2 += neigh.o2
            self.neighbors_h2o += neigh.h2o
            self.neighbors_glucose += neigh.glucose

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        if not self.is_persistent:
            avg_o2 = self.neighbors_o2 / self.num_neighbors
            self.o2 = (1.0 - (self.evaporation * 10)) * (self.o2 + (self.diffusion * 10) * (avg_o2 - self.o2))
            avg_co2 = self.neighbors_co2 / self.num_neighbors
            self.co2 = (1.0 - self.evaporation) * (self.co2 + self.diffusion * (avg_co2 - self.co2))
            avg_h2o = self.neighbors_h2o / self.num_neighbors
            self.h2o = (1.0 - (self.evaporation * 5)) * (self.h2o + (self.diffusion * 5) * (avg_h2o - self.h2o))
            avg_glucose = self.neighbors_glucose / self.num_neighbors
            self.glucose = (1.0 - self.evaporation) * (self.glucose + self.diffusion * (avg_glucose - self.glucose))

            self.num_neighbors = 0
            self.neighbors_o2 = 0
            self.neighbors_co2 = 0
            self.neighbors_h2o = 0
            self.neighbors_glucose = 0

        self.co2 = 1
        self.h2o = 1