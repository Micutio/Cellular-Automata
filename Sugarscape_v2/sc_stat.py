__author__ = 'Michael Wagner'
__version__ = '1.0'

import numpy
import matplotlib.pyplot as plt
#########################################################################
###                       Global Variables                            ###
#########################################################################

#########################################################################
###                            CLASSES                                ###
#########################################################################


class Statistics:
    """
    This class records and outputs statistics about the sugarscape.
    """

    def __init__(self, abm, ca):
        """
        Initializes the Statistics class.
        """
        self.abm = abm
        self.ca = ca
        # Variables to record
        self.pop_per_gen = []
        self.total_sugar = []
        self.total_spice = []

    def update_records(self):
        """
        Should be called every tick. This saves important data that is
        to be displayed by the information key.
        """
        self.pop_per_gen.append(len(self.abm.agent_dict))
        sugar = 0
        spice = 0
        for k, v in self.ca.ca_grid.items():
            sugar += v.sugar
            spice += v.spice
        self.total_sugar.append(sugar)
        self.total_spice.append(spice)

    def plot(self):
        """
        Plots all available data in figures.
        """
        ax = plt.subplot(111)
        len_pop = len(self.pop_per_gen)
        len_sugar = len(self.total_sugar)
        len_spice = len(self.total_spice)
        ax.plot(range(len_pop), self.pop_per_gen, color="#0000FF", linewidth=2)
        ax.plot(range(len_sugar), self.total_sugar, color="#00FF00", linewidth=1)
        ax.plot(range(len_spice), self.total_spice, color="#FF0000", linewidth=1)
        ax.grid()

        plt.legend(("population", "total sugar", "total spice"), loc=7)
        plt.title("Sugarscape Information")
        plt.show()