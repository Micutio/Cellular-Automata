__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import copy


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

    def get_genome_substring(self, key):
        """
        Retrieves the partitions of both genes.
        :param key: The key of the partition entries' location in the dictionary
        :return: Two sub-strings of the genomes
        """
        indices = self.att_map[key]
        start = indices[0]
        end = indices[1]
        result = map(str, self.dna[start: end])
        result = "".join(result)
        #return self.dna[start: end]
        return result

    def get_dna(self):
        bit = random.choice(range(len(self.dna)))
        self.dna[bit] = 1 - self.dna[bit]
        # TODO: Remove the following line to enable mitochondria to spawn.
        self.dna[0] = 0
        return copy.deepcopy(self.dna)


class Chloroplast:
    def __init__(self, eff, meta):
        self.efficiency = eff
        self.metabolism = meta
        return

    def process(self, cell):
        production = (self.efficiency * cell.co2)
        glucose_out = production - self.metabolism

        cell.co2 = 0
        return glucose_out


class Mitochondrion:
    def __init__(self, eff, meta):
        self.efficiency = eff
        self.metabolism = meta
        return

    def process(self, cell):
        production = (self.efficiency * cell.o2)
        atp_out = production - self.metabolism

        cell.co2 = 0
        return atp_out

