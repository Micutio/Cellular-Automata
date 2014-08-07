__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is an ABM for a python implementation of Sugarscape.

import random
import copy
from v2.abm.sc_agent import Agent
from v2.abm.sc_tribes import Tribes
from v2.sc_global_constants import GlobalConstants

GC = GlobalConstants()


class ABM:
    def __init__(self, num_agents, c_size, min_x, max_x, min_y, max_y, visualizer):
        """
        Initializes an abm with the given number of agents and returns it
        :return: An initialized ABM.
        """
        self.agent_dict = {}
        self.tribes = Tribes(GC.NUM_TRIBES)
        self.visualizer = visualizer
        total_wealth = 0
        a_id = 0
        c = c_size
        r = int(c_size / 2)
        positions = [((x * c) + r, (y * c) + r) for x in range(min_x, max_x) for y in range(min_y, max_y)]
        positions = random.sample(positions, num_agents)
        random.shuffle(positions)

        for p in positions:
            meta_sugar = random.randint(GC.MIN_METABOLISM, GC.MAX_METABOLISM)
            meta_spice = random.randint(GC.MIN_METABOLISM, GC.MAX_METABOLISM)
            vision = random.randint(1, GC.VISION)
            g = random.choice([0, 1])
            if g == 1:
                f = [GC.F_FERTILITY_START, random.randint(GC.F_FERTILITY_END[0], GC.F_FERTILITY_END[1])]
            else:
                f = [GC.M_FERTILITY_START, random.randint(GC.M_FERTILITY_END[0], GC.M_FERTILITY_END[1])]
            su = random.randint(GC.STARTING_SUGAR[0], GC.STARTING_SUGAR[1])
            sp = random.randint(GC.STARTING_SUGAR[0], GC.STARTING_SUGAR[1])
            d = random.randint(f[1], GC.MAX_AGENT_LIFE)
            c = [random.randint(0, GC.NUM_TRIBES - 1) for _ in range(11)]
            imm_sys = [random.getrandbits(1) for _ in range(50)]
            a = random.randint(0, int(GC.MAX_AGENT_LIFE / 2))
            gene_string = bin(meta_sugar) + bin(meta_spice) + bin(su) + bin(sp)
            gene_string += bin(vision) + bin(g) + bin(f[0]) + bin(f[1]) + bin(d)
            genome = (gene_string, gene_string, c, imm_sys)
            self.agent_dict[p[0], p[1]] = Agent(p[0], p[1], c_size, su, sp, genome, a, self.tribes)
            a_id += 1

            total_wealth += (su + sp)
        self.tribes.total_wealth = total_wealth

    def cycle_system(self, ca):
        """
        Cycles through all agents and has them perceive and act in the world
        """
        # Have all agents perceive and act in a random order
        # While we're at it, look for dead agents to remove
        temp_dict = copy.deepcopy(self.agent_dict)
        for (_, _), v in temp_dict.items():
            v.perceive_and_act(ca, self.agent_dict)
            # In case the agent has updated it's position we change the position list accordingly.
            self.update_position(v)

    def draw_agents(self):
        """
        Iterates over all agents and draws them on the grid
        """
        for (_, _), v in self.agent_dict.items():
            self.visualizer.draw_agent(v)

    def get_agent_at_position(self, x, y):
        for (_, _), v in self.agent_dict.items():
            if v.x == x and v.y == y:
                return v

    def update_position(self, v):
        if v.dead:
            v.on_death()
            self.agent_dict.pop((v.prev_x, v.prev_y))
        #elif v.x != v.prev_x or v.y != v.prev_y:
        else:
            self.agent_dict.pop((v.prev_x, v.prev_y))
            self.agent_dict[v.x, v.y] = v