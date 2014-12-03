"""
Cell life module for genetics functions. For now we only concern us with one cell life forms.
"""

__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import copy


class Chromosome:
    def __init__(self, dna):
        self.dna = dna


class Chloroplast(Chromosome):
    """
    Simple One-Cell life form.
    """
    def __init__(self, dna):
        super().__init__(dna)


class Mitochondrion(Chromosome):
    """
    Simple One-Cell life form.
    """
    def __init__(self, dna):
        super().__init__(dna)


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


def choose_dominant_gene(strings):
    """
    Takes two gene strings and returns the dominant one,
    or random if both are dominant/ recessive
    :param strings: Two sub-genes of the chromosome
    :return: The more dominant/ luckier string of both.
    """
    # How do we determine dominance?
    # For now just by looking whether there is an even number of 'ones' in it.
    dominant0 = strings[0].count('1') % 2 == 0
    dominant1 = strings[1].count('1') % 2 == 0
    if (dominant0 and dominant1) or (not (dominant0 or dominant1)):
        return random.choice([strings[0], strings[1]])
    elif dominant1:
        return strings[0]
    else:
        return strings[1]