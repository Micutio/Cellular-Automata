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
    This class records and outputs statistics about the creeps.
    """

    def __init__(self, abm, ca):
        """
        Initializes the Statistics class.
        """
        self.abm = abm
        self.ca = ca
        self.pops = [[], [], [], []]
        self.creep_area = [[], [], [], []]
        self.creep_mass = [[], [], [], []]

    def update_records(self):
        """
        Should be called every tick. This saves important data that is
        to be displayed by the information key.
        """
        pop = [0, 0, 0, 0]
        for a in self.abm.agent_list:
            if not a.dead:
                pop[a.team] += 1
        for i in range(4):
            self.pops[i].append(pop[i])

        mass = [0, 0, 0, 0]
        area = [0, 0, 0, 0]
        for _, v in self.ca.ca_grid.items():
            if v.team != -1:
                mass[v.team] += v.temperature
                area[v.team] += 1
        for i in range(4):
            self.creep_area[i].append(area[i])
            self.creep_mass[i].append(mass[i])

    def print_pop(self):
        print("-------pop-info---------------------------------------------------------")
        for a in self.abm.agent_list:
            if a.dead:
                doa = " (dead)"
            else:
                doa = " "
            print("team " + str(a.team) + ", move: " + str(a.strategy_walk) + ", seed: "
                  + str(a.strategy_seed) + ", score: " + str(a.score) + doa)
        print("------------------------------------------------------------------------")

    def plot(self):
        """
        Plots all available data in figures.
        """
        self.print_pop()

        generations = len(self.pops[0])
        gen_line = range(generations)
        pop_graph = plt.subplot(2, 1, 1)
        #pop_graph.plot(gen_line, self.pops[0], color="#FF0000", linewidth=1)
        #pop_graph.plot(gen_line, self.pops[1], color="#FFFF00", linewidth=1)i
        #pop_graph.plot(gen_line, self.pops[2], color="#00FF00", linewidth=1)
        #pop_graph.plot(gen_line, self.pops[3], color="#0000FF", linewidth=1)
        pop_graph.plot(gen_line, self.creep_area[0], color="#FF0000", linewidth=1)
        pop_graph.plot(gen_line, self.creep_area[1], color="#FFFF00", linewidth=1)
        pop_graph.plot(gen_line, self.creep_area[2], color="#00FF00", linewidth=1)
        pop_graph.plot(gen_line, self.creep_area[3], color="#0000FF", linewidth=1)
        plt.ylabel("creep area")
        pop_graph.grid()
        #pop_graph.legend(("total pop", "male pop", "female pop", "white culture", "black culture"), loc=7)

        resource_graph = plt.subplot(2, 1, 2)
        resource_graph.plot(gen_line, self.creep_mass[0], color="#900000", linewidth=1)
        resource_graph.plot(gen_line, self.creep_mass[1], color="#909000", linewidth=1)
        resource_graph.plot(gen_line, self.creep_mass[2], color="#009000", linewidth=1)
        resource_graph.plot(gen_line, self.creep_mass[3], color="#000090", linewidth=1)
        plt.ylabel("creep mass")
        resource_graph.grid()
        #resource_graph.legend(("total sugar", "total spice"), loc=7)

        #plt.title("Sugarscape Information")
        plt.show()