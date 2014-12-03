"""
Celllife module for genetics functions.
"""

__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import copy


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