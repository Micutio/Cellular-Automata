__author__ = 'Michael Wagner'
__version__ = '1.0'


class Disease:
    """
    Interface for the two classes virus and bacteria.
    """
    def __init__(self, genome, sugar_meta_modifier, spice_meta_modifier, color):
        # The modifiers indicate how much the metabolism of affected agents changes.
        self.genome = genome
        self.genome_string = "".join(map(str, genome))
        self.su_mod = sugar_meta_modifier
        self.sp_mod = spice_meta_modifier
        # The color is used in the disease map mode.
        self.color = color

    def affect(self, agent):
        return

    def spread(self, agent):
        return