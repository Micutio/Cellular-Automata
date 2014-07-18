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
        self.male_per_gen = []
        self.female_per_gen = []
        self.cult_white = []
        self.cult_black = []
        self.total_sugar = []
        self.total_spice = []
        self.production_sugar = []
        self.production_spice = []
        self.trade_sugar = []
        self.trade_spice = []

    def update_records(self):
        """
        Should be called every tick. This saves important data that is
        to be displayed by the information key.
        """
        self.pop_per_gen.append(len(self.abm.agent_dict))
        males = 0
        females = 0
        black_cults = 0
        white_cults = 0
        prod_sugar = 0
        prod_spice = 0
        tr_sugar = 0
        tr_spice = 0

        for k, v in self.abm.agent_dict.items():
            # count gender
            if v.gender == "m":
                males += 1
            else:
                females += 1
            # count culture
            if v.culture.count(0) > v.culture.count(1):
                black_cults += 1
            else:
                white_cults += 1
            # count production
            prod_sugar += v.sugar_gathered
            prod_spice += v.spice_gathered
            # count trade
            tr_sugar += v.sugar_traded
            tr_spice += v.spice_traded

        self.male_per_gen.append(males)
        self.female_per_gen.append(females)
        self.cult_black.append(black_cults)
        self.cult_white.append(white_cults)
        self.production_sugar.append(prod_sugar)
        self.production_spice.append(prod_spice)
        self.trade_sugar.append(tr_sugar)
        self.trade_spice.append(tr_spice)

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
        generations = len(self.pop_per_gen)
        gen_line = range(generations)
        pop_graph = plt.subplot(2, 1, 1)
        pop_graph.plot(gen_line, self.pop_per_gen, color="#505050", linewidth=1)
        pop_graph.plot(gen_line, self.male_per_gen, color="#0000FF", linewidth=1)
        pop_graph.plot(gen_line, self.female_per_gen, color="#FF0090", linewidth=1)
        pop_graph.plot(gen_line, self.cult_black, ":", color="#606060", linewidth=1)
        pop_graph.plot(gen_line, self.cult_white, "--", color="#BBBBBB", linewidth=1)
        plt.ylabel("population")
        pop_graph.grid()
        #pop_graph.legend(("total pop", "male pop", "female pop", "white culture", "black culture"), loc=7)

        resource_graph = plt.subplot(2, 1, 2)
        resource_graph.plot(gen_line, self.total_sugar, color="#90FF90", linewidth=1)
        resource_graph.plot(gen_line, self.total_spice, color="#FF9090", linewidth=1)
        resource_graph.plot(gen_line, self.production_sugar, ":", color="#00AA00", linewidth=2)
        resource_graph.plot(gen_line, self.trade_sugar, "--", color="#00AA00", linewidth=2)
        resource_graph.plot(gen_line, self.production_spice, ":", color="#AA0000", linewidth=2)
        resource_graph.plot(gen_line, self.trade_spice, "--", color="#AA0000", linewidth=2)
        plt.ylabel("resources")
        resource_graph.grid()
        #resource_graph.legend(("total sugar", "total spice"), loc=7)

        plt.title("Sugarscape Information")
        plt.show()