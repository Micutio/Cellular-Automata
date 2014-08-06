__author__ = 'Michael Wagner'
__version__ = '1.0'

import random


# TODO: Complete implementation
class Chromosome:
    """
    This class handles all biological aspects of an agent.
    """

    def __init__(self, genomes):
        """
        Standard initializer.
        :return:
        """
        self.genomes = genomes
        self.culture = None
        self.immune_system = None
        self.attributes = None
        self.meta_sugar = None
        self.meta_spice = None
        self.init_sugar = None
        self.init_spice = None
        self.vision = None
        self.gender = None
        self.fertility = None
        self.dying_age = None
        # Read dictionary entries as:
        # ----> {attribute: (start index, end index)}
        self.att_map = {'meta_sugar': (0, 2),
                        'meta_spice': (2, 4),
                        'init_sugar': (4, 10),
                        'init_spice': (10, 16),
                        'vision': (16, 19),
                        'gender': (19, 20),
                        'fertility_1': (20, 22),
                        'fertility_2': (22, 24),
                        'dying_age': (24, 31)}

        self.map_genome_to_attributes()

    def map_genome_to_attributes(self):
        """
        Decodes the genome and creates the attribute of the individual.
        :return:
        """
        # TODO: Improve genetics!
        # TODO: How often do we have to build the chromosome from the genome?
        gene = random.choice(self.genomes)
        self.meta_sugar = int(gene[self.att_map['meta_sugar'][0]: self.att_map['meta_sugar'][1]], 2)
        self.meta_spice = int(gene[self.att_map['meta_spice'][0]: self.att_map['meta_spice'][1]], 2)
        self.init_sugar = int(gene[self.att_map['init_sugar'][0]: self.att_map['init_sugar'][1]], 2)
        self.init_spice = int(gene[self.att_map['init_spice'][0]: self.att_map['init_spice'][1]], 2)
        self.vision = int(gene[self.att_map['vision'][0]: self.att_map['vision'][1]], 2)
        self.gender = int(gene[self.att_map['gender'][0]: self.att_map['gender'][1]], 2)
        self.dying_age = int(gene[self.att_map['dying_age'][0]: self.att_map['dying_age'][1]], 2)
        f1 = int(gene[self.att_map['fertility_1'][0]: self.att_map['fertility_1'][1]], 2)
        f2 = int(gene[self.att_map['fertility_2'][0]: self.att_map['fertility_2'][1]], 2)
        self.fertility = (f1, f2)

        return

    def merge_with(self, mate_genomes):
        """
        Takes the chromosome from the mate and performs the fertilization.
        :param mate_genomes:
        :return: The child's chromosome.
        """
        # TODO: Finish this!
        return

    # This method makes sense only for Lamarckian Evolution!
    def map_attributes_to_genome(self, attributes):
        return