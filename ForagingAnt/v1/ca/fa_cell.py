__author__ = 'Michael Wagner'
__version__ = '2.0'


class ClassCell:
    """
    This class models one cell of the CA, while the grid itself will be a dictionary of ClassCell instances.
    """

    def __init__(self, x, y, c_size, diffusion, evaporation, max_ph, food, is_hive):
        self.x = x
        self.y = y
        self.w = c_size
        self.h = c_size
        self.diffusion = diffusion
        self.evaporation = evaporation
        self.max_ph = max_ph
        self.pheromones = {"hive": 0, "food": 0}
        #self.neighbor_pheromones = {"hive": 0, "food": 0}
        #self.num_neighbors = 0
        self.food = food
        self.is_hive = is_hive
        self.num_neighbors = 0
        self.neighbor_pheromones = {"hive": 0, "food": 0}
        self.neighbor_max_pheromone = {"hive": 0, "food": 0}
        self.last_neighbor_max_pheromone = {"hive": 0, "food": 0}

    def sense_neighbor(self, neigh):
        self.num_neighbors += 1
        for ph in ["hive", "food"]:
            self.neighbor_pheromones[ph] += neigh.pheromones[ph]
            if neigh.pheromones[ph] > self.neighbor_max_pheromone[ph]:
                self.neighbor_max_pheromone[ph] = neigh.pheromones[ph]

    def update(self):
        """
        This method regulates the cell's temperature according to the temperature of its neighbors.
        """
        for ph in ["hive", "food"]:
            avg = self.neighbor_pheromones[ph] / self.num_neighbors
            self.pheromones[ph] = (1.0 - self.evaporation) * (self.pheromones[ph] + self.diffusion * (avg - self.pheromones[ph]))
            #if self.pheromones[ph] < 1:
            #    self.pheromones[ph] = 0

        self.num_neighbors = 0
        self.neighbor_pheromones = {"hive": 0, "food": 0}
        self.last_neighbor_max_pheromone = self.neighbor_max_pheromone
        self.neighbor_max_pheromone = {"hive": 0, "food": 0}