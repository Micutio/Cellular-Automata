__author__ = 'Michael Wagner'

import random

from cab_agent import Agent


class CellLifeSpawner(Agent):
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)

    def clone(self, x, y):
        return CellLifeSpawner(x, y, self.gc)

    def perceive_and_act(self, ca, abm):
        if len(abm.agent_locations) == 1:
            new_x = random.randint(0, self.gc.DIM_X)
            new_y = random.randint(0, self.gc.DIM_Y)
            _agent = CellAgent(new_x, new_y, self.gc)
            abm.add_agent(_agent)
            abm.agent_list.append(_agent)
            print("added agent")
        pass


class AbstractChromosome:
    def __init__(self, dna):
        self.dna = dna
        self.core = None  # Will be either a chloroplast (plant) or a mitochondrion (animal).

    def get_genome_substring(self, key):
        raise NotImplementedError("Should have implemented this")


class MitosisChromosome(AbstractChromosome):
    def __init__(self, dna):
        super().__init__(dna)
        self.att_map = {"type": (0, 1),  # Decides whether the core is gonna be a chloroplast or mitochondrion.
                        "efficiency": (1, 8),
                        "mitosis_limit": (8, 15),  # How much is needed to procreate.
                        "dying_age": (15, 22),
                        "metabolism": (22, 28)}  # How much is needed every tick to stay alive.

        self.eff = min(int(self.get_genome_substring("efficiency"), 2) / 100, 1)
        c_type = int(self.get_genome_substring("type"), 2)
        self.metabolism = int(self.get_genome_substring("metabolism"), 2)
        if c_type == 0:
            #self.core = Chloroplast(eff, metabolism)
            self.type = "chloroplast"
        else:
            #self.core = Mitochondrion(eff, metabolism)
            self.type = "mitochondrion"

        self.mitosis_limit = max(int(self.get_genome_substring("mitosis_limit"), 2), 1)
        self.dying_age = int(self.get_genome_substring("dying_age"), 2)


class CellAgent(Agent):
    def __init__(self, x, y, gc, chromosome):
        super().__init__(x, y, gc)
        self.chromosome = chromosome

    def clone(self, x, y):
        return CellAgent(x, y, self.gc, self.chromosome)

    def perceive_and_act(self, ca, abm):
        self.chromosome.act(self, ca, abm)