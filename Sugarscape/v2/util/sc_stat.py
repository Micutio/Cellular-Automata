__author__ = 'Michael Wagner'
__version__ = '1.0'

import matplotlib.pyplot as plt
plt.xkcd()


class Statistics:
    """
    This class records and outputs statistics about the sugarscape.
    """

    def __init__(self, abm, ca, gc):
        """r
        Initializes the Statistics class.
        """
        self.abm = abm
        self.ca = ca
        # Variables to record
        self.pop_per_gen = []
        self.male_per_gen = []
        self.female_per_gen = []
        self.gc = gc
        self.tribes = [[] for _ in range(self.gc.NUM_TRIBES)]
        self.total_sugar = []
        self.total_spice = []
        self.production_sugar = []
        self.production_spice = []
        self.trade_sugar = []
        self.trade_spice = []
        self.sugar_price = []
        self.spice_price = []

    def update_records(self):
        """
        Should be called every tick. This saves important data that is
        to be displayed by the information key.
        """
        self.pop_per_gen.append(len(self.abm.agent_dict))
        males = 0
        females = 0
        tribes = [0 for _ in range(self.gc.NUM_TRIBES)]
        prod_sugar = 0
        prod_spice = 0
        tr_sugar = 0
        tr_spice = 0
        sugar_pr = 0
        spice_pr = 0
        price_count = 0

        for k, v in self.abm.agent_dict.items():
            # count gender
            if v.gender == 0:
                males += 1
            else:
                females += 1
            # count culture
            tribes[v.tribe_id] += 1
            # count production
            prod_sugar += v.sugar_gathered
            prod_spice += v.spice_gathered
            # count trade
            tr_sugar += v.sugar_traded
            tr_spice += v.spice_traded
            # count market prices
            sugar_pr += v.sugar_price
            spice_pr += v.spice_price
            price_count += 1

        if price_count > 0:
            sugar_pr /= price_count
            spice_pr /= price_count

        self.male_per_gen.append(males)
        self.female_per_gen.append(females)
        self.production_sugar.append(prod_sugar)
        self.production_spice.append(prod_spice)
        self.trade_sugar.append(tr_sugar)
        self.trade_spice.append(tr_spice)
        self.sugar_price.append(sugar_pr)
        self.spice_price.append(spice_pr)

        for i in range(self.gc.NUM_TRIBES):
            self.tribes[i].append(tribes[i])

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
        pop_graph = plt.subplot(2, 2, 1)
        pop_graph.plot(gen_line, self.pop_per_gen, color="#505050", linewidth=1)
        pop_graph.plot(gen_line, self.male_per_gen, color="#0000FF", linewidth=1)
        pop_graph.plot(gen_line, self.female_per_gen, color="#FF0090", linewidth=1)
        for i in range(self.gc.NUM_TRIBES):
            rgb = self.gc.TRIBE_COLORS[i]
            color = '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
            pop_graph.plot(gen_line, self.tribes[i], "-", color=color, linewidth=1)
        plt.ylabel("population and tribes")
        #pop_graph.grid()  # deactivate if using xkcd()
        #pop_graph.legend(("total pop", "male pop", "female pop", "tribes"), loc=7)

        resource_graph = plt.subplot(2, 2, 2)
        resource_graph.plot(gen_line, self.total_sugar, color="#90FF90", linewidth=1)
        resource_graph.plot(gen_line, self.total_spice, color="#FF9090", linewidth=1)
        plt.ylabel("resources")
        #resource_graph.grid()  # deactivate if using xkcd()
        #resource_graph.legend(("total sugar", "total spice"), loc=7)

        production_graph = plt.subplot(2, 2, 3)
        production_graph.plot(gen_line, self.production_sugar, ":", color="#00AA00", linewidth=1)
        production_graph.plot(gen_line, self.trade_sugar, "--", color="#00AA00", linewidth=1)
        production_graph.plot(gen_line, self.production_spice, ":", color="#AA0000", linewidth=1)
        production_graph.plot(gen_line, self.trade_spice, "--", color="#AA0000", linewidth=1)
        plt.ylabel("production (dotted) and trade (dashed)")
        #production_graph.grid()  # deactivate if using xkcd()

        market_graph = plt.subplot(2, 2, 4)
        market_graph.plot(gen_line, self.sugar_price, color="#00FF00", linewidth=1)
        market_graph.plot(gen_line, self.spice_price, color="#FF0000", linewidth=1)
        plt.ylabel("market prices")
        #market_graph.grid()  # deactivate if using xkcd()

        plt.title("Sugarscape Information")
        plt.show()