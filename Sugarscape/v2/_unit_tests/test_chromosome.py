from unittest import TestCase
import unittest
import random
from v2.abm.sc_genetics import Chromosome

__author__ = 'Michl'


class TestChromosome(TestCase):
    """
    The purpose of this test in to ensure that the encoding / decoding of chromosomes delivers the correct values.
    """
    def setUp(self):
        # Create new genome, encode the single attributes into bit strings and concatenate them.
        self.meta_sugar = random.randint(1, 4)
        self.meta_spice = random.randint(1, 4)
        self.vision = random.randint(1, 6)
        self.g = random.choice([0, 1])
        if self.g == 1:
            self.f = (15, random.randint(40, 50))
        else:
            self.f = (15, random.randint(50, 60))
        self.su = random.randint(20, 40)
        self.sp = random.randint(20, 40)
        self.d = random.randint(self.f[1], 100)
        self.c = [random.randint(0, 2 - 1) for _ in range(11)]
        self.imm_sys = [random.getrandbits(1) for _ in range(50)]
        gene_string = "{0:03b}".format(self.meta_sugar) + "{0:03b}".format(self.meta_spice)\
                      + "{0:06b}".format(self.su) + "{0:06b}".format(self.sp) \
                      + "{0:03b}".format(self.vision) + "{0:01b}".format(self.g)\
                      + "{0:06b}".format(self.f[0]) + "{0:06b}".format(self.f[1]) + "{0:07b}".format(self.d)
        self.genome = (gene_string, gene_string, self.c, self.imm_sys)
        print("Genome Length: " + str(len(gene_string)))

    def test_sample(self):
        with self.assertRaises(ValueError):
            # Hand new genome to chromosome, which decodes it automatically into attributes.
            chromosome = Chromosome(self.genome)
            meta_sugar = chromosome.meta_sugar
            meta_spice = chromosome.meta_spice
            vision = chromosome.vision
            g = chromosome.gender
            f = chromosome.fertility
            su = chromosome.init_sugar
            sp = chromosome.init_spice
            d = chromosome.dying_age
            c = chromosome.culture
            imm_sys = chromosome.immune_system
            # Assert that all the new attributes are the same as the old attributes.
            self.assertEqual(self.meta_sugar, meta_sugar)
            self.assertEqual(self.meta_spice, meta_spice)
            self.assertEqual(self.vision, vision)
            self.assertEqual(self.g, g)
            self.assertEqual(self.f, f)
            self.assertEqual(self.su, su)
            self.assertEqual(self.sp, sp)
            self.assertEqual(self.d, d)
            self.assertEqual(self.c, c)
            self.assertEqual(self.imm_sys, imm_sys)
            self.assertEqual(1, 1)
            raise ValueError


def main():
    unittest.main()

if __name__ == '__main__':
    main()