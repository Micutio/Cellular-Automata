__author__ = 'Michael Wagner'
__version__ = '2.0'


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
        self.pheromones = {"hive": 0, "food": 0}
        #self.neighbor_pheromones = {"hive": 0, "food": 0}
        #self.num_neighbors = 0
        self.food = food
        self.is_hive = is_hive
        self.num_neighbors = 0
        self.neighbor_pheromones = {"hive": 0, "food": 0}
        self.neighbor_max_pheromone = {"hive": 0, "food": 0}

    def sense_neighbor(self, neigh):
        self.num_neighbors += 1
        self.neighbor_pheromones["hive"] += neigh.pheromones["hive"]
        self.neighbor_pheromones["food"] += neigh.pheromones["food"]
        if neigh.pheromone["hive"] > self.neighbor_max_pheromone["hive"]:
            self.neighbor_max_pheromone["hive"] = neigh.pheromones["hive"]
        if neigh.pheromone["food"] > self.neighbor_max_pheromone["food"]:
            self.neighbor_max_pheromone["food"] = neigh.pheromones["food"]

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        #if self.num_neighbors > 0:
            #for i in range(len(self.pheromones)):
                #avg = self.neighbor_pheromones[i] / self.num_neighbors
                # This cells pheromone amount is greater than in the surrounding
                # We have a pheromone flux out this cell.
                #if self.pheromones[i] > avg:
                #    self.pheromones[i] -= (self.pheromones[i] - avg) * self.out_flux
                # This cells pheromone amount is lesser than in the surrounding
                # We have an influx of pheromone
                #else:
                #    self.pheromones[i] += (avg - self.pheromones[i]) * self.in_flux
        # Reset the control variables for the next round.
        #self.num_neighbors = 0
        #self.neighbor_pheromones = [0, 0]
        decrease = 0
        if self.pheromones["hive"] >= decrease:
            self.pheromones["hive"] -= decrease
        else:
            self.pheromones["hive"] = 0

        if self.pheromones["food"] >= decrease:
            self.pheromones["food"] -= decrease
        else:
            self.pheromones["food"] = 0