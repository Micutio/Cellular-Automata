__author__ = 'Michael Wagner'
__version__ = '1.0'

import copy
import random


class Disease:
    """
    Interface for the two classes virus and bacteria.
    """
    def __init__(self, genome, tag):
        # The modifiers indicate how much the metabolism of affected agents changes.
        self.genome = genome
        self.genome_string = "".join(map(str, genome))
        self.tag = tag

    def spread(self, agent):
        return

    def affect(self, agent):
        return


class Bacteria(Disease):
    """
    Bacteria are one kind of disease in the sugarscape, the other one being viruses.
    Bacteria increase the sugar metabolism of an agent, causing it to need more sugar
    to survive.
    """
    def __init__(self, genome):
        """
        Initializer. Bacteria have the fixed tag 'bacteria' in order to be identified by the system.
        """
        super().__init__(genome, "bacteria")

    def spread(self, agent):
        """
        It spreads to agents in the standard way: placing a copy into its disease list.
        """
        if not self.genome_string in agent.diseases:
            agent.diseases[self.genome_string] = copy.deepcopy(self)

    def affect(self, agent):
        """
        In this version of Sugarscape bacteria affect agents by raising their sugar consumption.
        """
        agent.meta_sugar += 2
        agent.meta_spice += 2


class Virus(Disease):
    """
    Viruses are one kind of disease in the sugarscape, the other one being bacteria.
    Viruses increase the spice metabolism of an agent, causing it to need more spice
    to survive.
    """
    def __init__(self, genome):
        """
        Initializer. Viruses have the fixed tag 'virus' in order to be identified by the system.
        """
        half = int(len(genome) / 2)
        virus_genome = genome[0: half]
        super().__init__(virus_genome, "virus")

    def spread(self, agent):
        """
        It spreads to agents in the standard way: placing a copy into its disease list.
        """
        if not self.genome_string in agent.diseases:
            genome_offspring = self.genome
            index = random.choice(range(0, len(self.genome)))
            genome_offspring[index] = 1 - genome_offspring[index]
            agent.diseases[self.genome_string] = copy.deepcopy(self)
            agent.diseases[self.genome_string].genome = genome_offspring

    def affect(self, agent):
        """
        In this version of Sugarscape viruses affect agents by raising their spice consumption.
        Additionally viruses inject a part of their dna into their hosts.
        Furthermore its own genome has a certain chance per tick to mutate.
        """
        agent.vision = max(agent.vision - 1, 0)
        # TODO: Inject part of own genome into agent instead of just temporarily changing an attribute
        # TODO: When genome injected into agent, give it the possibility to repair its genome, if the virus is defeated.