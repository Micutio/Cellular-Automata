__author__ = 'Michael Wagner'
__version__ = '1.0'

import uuid
import random
from abm.cl_genetics import ChromosomeMitosis


class Agent:
    """
    Interface for all agent classes in this system.
    """
    def __init__(self, x, y, c_size, dna):
        self.a_id = uuid.uuid4().urn
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.size = c_size
        self.chromosome = ChromosomeMitosis(dna)
        self.type = self.chromosome.type
        self.dead = False

    def perceive_and_act(self, ca, abm, agent_list):
        raise NotImplementedError("Should have implemented this")


class BioCell(Agent):
    def __init__(self, x, y, c_size, dna):
        super().__init__(x, y, c_size, dna)
        self.chromosome = ChromosomeMitosis(dna)
        self.age = 0
        self.energy = 1

    def perceive_and_act(self, ca, abm, agent_list):
        self.prev_x = self.x
        self.prev_y = self.y
        neighborhood = ca.get_neighborhood(agent_list, self.x, self.y)

        self.produce(neighborhood)
        self.procreate(neighborhood, abm)

        if self.age >= self.chromosome.dying_age or self.energy <= 0:
            self.dead = True
        self.age += 1

    def produce(self, neighborhood):
        x = int(self.x / self.size)
        y = int(self.y / self.size)

        if (x, y) in neighborhood:
            cell = neighborhood[x, y]
            if cell[0].co2 == 0 or cell[0].h2o == 0 or cell[0].light == 0:
                self.dead = True
            else:
                output = self.chromosome.core.process(cell[0])
                self.energy += output
                return

    def procreate(self, neighborhood, abm):
        if self.energy > self.chromosome.mitosis_limit:
            free_cells = []
            for (_, _), cell in neighborhood.items():
                if not cell[1]:
                    free_cells.append(cell[0])

            if free_cells:
                cell = random.choice(free_cells)
                x = (cell.x * self.size) + int(self.size / 2)
                y = (cell.y * self.size) + int(self.size / 2)
                child = BioCell(x, y, self.size, self.chromosome.get_dna())
                abm.add_agent(child)
                self.energy -= self.chromosome.mitosis_limit