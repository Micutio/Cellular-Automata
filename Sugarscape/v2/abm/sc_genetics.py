__author__ = 'Michael Wagner'
__version__ = '1.0'

import random


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
        my_gen = max(dna[4][0], dna[4][1]) + 1
        self.generation = (dna[4][0], dna[4][1], my_gen)
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
        # TODO: Shift this map into GlobalConstants and automatically generate genome lengths from the given constants.
        self.att_map = {'meta_sugar': (0, 3),
                        'meta_spice': (3, 6),
                        'init_sugar': (6, 12),
                        'init_spice': (12, 18),
                        'vision': (18, 21),
                        'gender': (21, 22),
                        'fertility_1': (22, 28),
                        'fertility_2': (28, 34),
                        'dying_age': (34, 41)}

        self.map_genome_to_attributes()

    def map_genome_to_attributes(self):
        """
        Decodes the genome and creates the attribute of the individual.
        """
        # The meta and init attributes cannot become smaller than 1,
        # even though that is possible by the encoding. We have to avoid that.
        self.meta_sugar = max(int(self.choose_dominant_gene(self.get_genome_substring('meta_sugar')), 2), 1)
        self.meta_spice = max(int(self.choose_dominant_gene(self.get_genome_substring('meta_spice')), 2), 1)
        self.init_sugar = max(int(self.choose_dominant_gene(self.get_genome_substring('init_sugar')), 2), 1)
        self.init_spice = max(int(self.choose_dominant_gene(self.get_genome_substring('init_spice')), 2), 1)
        self.vision = int(self.choose_dominant_gene(self.get_genome_substring('vision')), 2)
        self.gender = int(random.choice(self.get_genome_substring('gender')), 2)
        self.dying_age = int(self.choose_dominant_gene(self.get_genome_substring('dying_age')), 2)
        f1 = int(self.choose_dominant_gene(self.get_genome_substring('fertility_1')), 2)
        f2 = int(self.choose_dominant_gene(self.get_genome_substring('fertility_2')), 2)
        self.fertility = (f1, f2)

    def get_genome_substring(self, key):
        """
        Retrieves the partitions of both genes.
        :param key: The key of the partition entries' location in the dictionary
        :return: Two sub-strings of the genomes
        """
        indices = self.att_map[key]
        start = indices[0]
        end = indices[1]
        return self.genomes[0][start: end], self.genomes[1][start: end]

    def choose_dominant_gene(self, strings):
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
        # Create a string out of the gene strings
        genome1 = "".join(map(str, genome1))
        genome2 = "".join(map(str, genome2))
        # Order the generation tuple for better overview: (mom, dad)
        if self.gender == 1:
            generation = (self.generation[2], mate_chromosome.generation[2])
        else:
            generation = (mate_chromosome.generation[2], self.generation[2])
        return [genome1, genome2, culture, immune_sys, generation]

    def create_gamete(self, genomes):
        """
        Creates and returns a gamete that consists of parts of
        both genomes in this chromosome.
        :return: Gamete in form of a single bitstring.
        """
        # 1) Generate a random number (gaussian distributed) of
        # random indices which are then used to split the genes at the respective points.
        genome_size = len(genomes[0])
        num_partitions = int(random.triangular(0, genome_size / 2, genome_size))
        partitions = random.sample(range(genome_size), num_partitions)
        partitions.sort()  # Now we have all our indices, and sorted.
        partitions.append(genome_size)  # Append the end of the string
        start = 0
        gamete = []
        for p in partitions:
            i = random.choice([0, 1])
            gamete.extend(genomes[i][start:p])
            start = p
        # 'gamete' is now a list of integers. Convert the ints to strings and join 'em all together.
        return gamete

    def mutate(self):
        """
        Has a chance of 0.5% to perform a random mutation in the dna,
        and a chance of 1% to flip a few bits in the cultural dna.
        :return:
        """
        # Flip bit in genome
        if random.random() < 0.005:
            length = len(self.genomes)
            index = random.randrange(length)
            l = list(self.genomes[0])
            l[index] = self.invert_bit(l[index])
            g1 = "".join(l)

            index = random.randrange(length)
            l = list(self.genomes[1])
            l[index] = self.invert_bit(l[index])
            g2 = "".join(l)
            self.genomes = (g1, g2)

        # Flip a bit in culture
        if random.random() < 0.01:
            length = len(self.culture)
            num_bits_changed = int(random.triangular(0, 1, length))
            index = random.sample(range(length), num_bits_changed)
            for i in index:
                self.culture[i] = 1 - self.culture[i]

    def invert_bit(self, bit):
        """
        Takes the bit as a string and inverts it.
        :param bit:
        :return: Inverted bit
        """
        if bit == "0":
            return "1"
        else:
            return "0"

    # This method makes sense only for Lamarckian Evolution!
    #def map_attributes_to_genome(self, attributes):
    #    return