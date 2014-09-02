__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import copy


class Chromosome:
    def __init__(self, dna):
        self.dna = dna
        self.core = None

    def get_genome_substring(self, key):
        raise NotImplementedError("Should have implemented this")


class ChromosomeMitosis(Chromosome):
    def __init__(self, dna):
        super().__init__(dna)
        self.att_map = {"type": (0, 1),
                        "eff1": (1, 8),
                        "eff2": (8, 15),
                        "eff3": (15, 22),
                        "eff4": (22, 29),
                        "eff5": (29, 36),
                        "eff6": (36, 43),
                        "mitosis_limit": (43, 50),
                        "dying_age": (50, 57),
                        "metabolism": (57, 63)}

        e1 = min(int(self.get_genome_substring("eff1"), 2) / 100, 1)
        e2 = min(int(self.get_genome_substring("eff2"), 2) / 100, 1)
        e3 = min(int(self.get_genome_substring("eff3"), 2) / 100, 1)
        e4 = min(int(self.get_genome_substring("eff4"), 2) / 100, 1)
        e5 = min(int(self.get_genome_substring("eff5"), 2) / 100, 1)
        e6 = min(int(self.get_genome_substring("eff6"), 2) / 100, 1)
        c_type = int(self.get_genome_substring("type"), 2)
        if c_type == 0:
            self.core = Chloroplast(e1, e2, e3, e4, e5, e6)
            self.type = "chloroplast"
        else:
            self.core = Mitochondrion(e1, e2, e3, e4, e5, e6)
            self.type = "mitochondrion"

        self.mitosis_limit = max(int(self.get_genome_substring("mitosis_limit"), 2), 1)
        self.dying_age = int(self.get_genome_substring("dying_age"), 2)
        self.metabolism = int(self.get_genome_substring("metabolism"), 2)

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
    def __init__(self, e1, e2, e3, e4, e5, e6):
        self.eff_co2 = e1
        self.eff_light = e2
        self.eff_o2 = e3
        self.eff_h2o_in = e4
        self.eff_ho2_out = e5
        self.eff_glucose = e6
        return

    def process(self, ca_cell):
        output = (self.eff_co2 * ca_cell.co2) + (self.eff_light * ca_cell.light) + (self.eff_h2o_in * ca_cell.h2o)
        total_out = (self.eff_ho2_out * 100) + (self.eff_o2 * 100)
        ratio_h2o = (self.eff_ho2_out * 100) / total_out
        ratio_o2 = (self.eff_o2 * 100) / total_out
        glucose_out = output * self.eff_glucose
        output -= glucose_out
        h2o_out = output * ratio_h2o
        o2_out = output * ratio_o2

        ca_cell.co2 -= (self.eff_co2 * ca_cell.co2)
        ca_cell.h2o -= (self.eff_h2o_in * ca_cell.h2o)
        ca_cell.h2o += h2o_out
        ca_cell.o2 += o2_out
        return glucose_out


class Mitochondrion:
    def __init__(self, e1, e2, e3, e4, e5, e6):
        self.eff_co2 = e1
        self.eff_atp = e2
        self.eff_o2 = e3
        self.eff_h2o_in = e4
        self.eff_h2o_out = e5
        self.eff_glucose = e6
        return

    def process(self, ca_cell):
        return ca_cell
