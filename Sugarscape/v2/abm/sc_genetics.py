__author__ = 'Michael Wagner'
__version__ = '1.0'

import numpy.random as npr


# TODO: Implement proper immune system.
class Chromosome:
    """
    This class handles all biological aspects of an agent.
    """

    def __init__(self, dna):
        """
        Standard initializer.
        :return:
        """
        self.genomes = dna[0:2]
        self.culture = dna[2]
        self.immune_system = dna[3]
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
                        'fertility_1': (20, 24),
                        'fertility_2': (24, 28),
                        'dying_age': (28, 35)}

        self.map_genome_to_attributes()

    def map_genome_to_attributes(self):
        """
        Decodes the genome and creates the attribute of the individual.
        """
        # The meta and init attributes cannot become smaller than 1
        self.meta_sugar = max(int(self.choose_dominant(self.get_sub_genes('meta_sugar')), 2), 1)
        self.meta_spice = max(int(self.choose_dominant(self.get_sub_genes('meta_spice')), 2), 1)
        self.init_sugar = max(int(self.choose_dominant(self.get_sub_genes('init_sugar')), 2), 1)
        self.init_spice = max(int(self.choose_dominant(self.get_sub_genes('init_spice')), 2), 1)
        self.vision = int(self.choose_dominant(self.get_sub_genes('vision')), 2)
        self.gender = int(self.choose_dominant(self.get_sub_genes('gender')), 2)
        self.dying_age = int(self.choose_dominant(self.get_sub_genes('dying_age')), 2)
        f1 = int(self.choose_dominant(self.get_sub_genes('fertility_1')), 2)
        f2 = int(self.choose_dominant(self.get_sub_genes('fertility_2')), 2)
        self.fertility = (f1, f2)

    def get_sub_genes(self, key):
        """
        Retrieves the partitions of both genes.
        :param key: The key of the partition entries' location in the dictionary
        :return: Two sub-strings of the genomes
        """
        indices = self.att_map[key]
        start = indices[0]
        end = indices[1]
        return self.genomes[0][start: end], self.genomes[1][start: end]

    def choose_dominant(self, strings):
        """
        Takes two gene strings and returns the dominant one,
        or random if both are dominant/ recessive
        :param strings: Two sub-genes of the chromosome
        :return: The more dominant/ luckier string of both.
        """
        # How do we distinguish dominance?
        # For now just by looking whether there is an even number of 'ones' in it.
        dominant0 = strings[0].count('1') % 2 == 0
        dominant1 = strings[1].count('1') % 2 == 0
        if (dominant0 and dominant1) or (not (dominant0 or dominant1)):
            return npr.choice([strings[0], strings[1]])
        elif dominant1:
            return strings[0]
        else:
            return strings[1]

    def merge_with(self, mate_chromosome):
        """
        Takes the chromosome from the mate, performs
        all necessary crossovers and returns the resulting DNA
        :param mate_chromosome:
        :return: The child's chromosome.
        """
        # Concept: divide genome in partions of varying length.
        # Exchange those parts between mother and father gametes?
        genome1 = self.create_gamete(self.genomes)
        genome2 = self.create_gamete(mate_chromosome.genomes)
        culture = self.create_gamete((self.culture, mate_chromosome.culture))
        immune_sys = self.create_gamete((self.immune_system, mate_chromosome.immune_system))
        return [genome1, genome2, culture, immune_sys]

    def create_gamete(self, genomes):
        """
        Creates and returns a gamete that consists of parts of
        both genomes in this chromosome.
        :return: Gamete in form of a single bitstring.
        """
        # 1) Generate a random number (gaussian distributed) of
        # random indices which are then used to split the genes at the respective points.
        genome_size = len(genomes[0]) - 1
        num_partitions = npr.triangular(0, genome_size / 2, genome_size)
        partitions = npr.sample(range(genome_size), num_partitions)
        partitions.append(-1)  # Append the end of the string
        partitions.sort()  # Now we have all our indices, and sorted.
        start = 0
        gamete = []
        for p in partitions:
            i = npr.choice([0, 1])
            gamete.append(genomes[i][start:p])
            start = p
        return gamete

    def mutate(self):
        """
        Has a chance of 1% to perform a random mutation in the dna.
        :return:
        """
        if npr.random() < 0.01:
            # Flip bit in genome
            length = len(self.genomes)
            index = npr.randint(length)
            l = list(self.genomes[0])
            l[index] = self.invert_bit(l[index])
            g1 = "".join(l)

            index = npr.randint(length)
            l = list(self.genomes[1])
            l[index] = self.invert_bit(l[index])
            g2 = "".join(l)

            self.genomes = (g1, g2)

    def invert_bit(self, bit):
        """
        Takes the bit as a string and inverts it.
        :param bit:
        :return: Inverted bit
        """
        if bit == '0':
            return '1'
        else:
            return '0'

    # This method makes sense only for Lamarckian Evolution!
    #def map_attributes_to_genome(self, attributes):
    #    return