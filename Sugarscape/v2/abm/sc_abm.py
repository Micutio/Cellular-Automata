__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is an ABM for a python implementation of Sugarscape.

import random
import copy
from v2.abm.sc_agent import Agent
from v2.abm.sc_tribes import Tribes


class ABM:
    def __init__(self, visualizer, gc):
        """
        Initializes an abm with the given number of agents and returns it
        :return: An initialized ABM.
        """
        self.agent_dict = {}
        self.tribes = Tribes(gc.NUM_TRIBES)
        self.visualizer = visualizer
        total_wealth = 0
        c = gc.CELL_SIZE
        r = int(gc.CELL_SIZE / 2)
        positions = [((x * c) + r, (y * c) + r)
                     for x in range(gc.ABM_BOUNDS[0], gc.ABM_BOUNDS[1])
                     for y in range(gc.ABM_BOUNDS[2], gc.ABM_BOUNDS[3])]
        positions = random.sample(positions, gc.NUM_AGENTS)
        random.shuffle(positions)

        for p in positions:
            meta_sugar = random.randint(gc.MIN_METABOLISM, gc.MAX_METABOLISM)
            meta_spice = random.randint(gc.MIN_METABOLISM, gc.MAX_METABOLISM)
            vision = random.randint(1, gc.VISION)
            g = random.choice([0, 1])
            if g == 1:
                f = (gc.F_FERTILITY_START, random.randint(gc.F_FERTILITY_END[0], gc.F_FERTILITY_END[1]))
            else:
                f = (gc.M_FERTILITY_START, random.randint(gc.M_FERTILITY_END[0], gc.M_FERTILITY_END[1]))
            su = random.randint(gc.STARTING_SUGAR[0], gc.STARTING_SUGAR[1])
            sp = random.randint(gc.STARTING_SUGAR[0], gc.STARTING_SUGAR[1])
            d = random.randint(f[1], gc.MAX_AGENT_LIFE)
            c = [random.randint(0, gc.NUM_TRIBES - 1) for _ in range(11)]
            imm_sys = [random.getrandbits(1) for _ in range(10)]
            a = 0  # random.randint(0, int(gc.MAX_AGENT_LIFE / 2))
            gene_string = "{0:03b}".format(meta_sugar) + "{0:03b}".format(meta_spice)\
                          + "{0:06b}".format(su) + "{0:06b}".format(sp) \
                          + "{0:03b}".format(vision) + "{0:01b}".format(g)\
                          + "{0:06b}".format(f[0]) + "{0:06b}".format(f[1]) + "{0:07b}".format(d)
            # We use generation to keep track of how far an agent has walked down the evolutionary road.
            generation = (0, 0)
            genome = (gene_string, gene_string, c, imm_sys, generation)
            self.agent_dict[p[0], p[1]] = Agent(p[0], p[1], gc.CELL_SIZE, su, sp, genome, a, self.tribes)

            # Update the tribal information
            tribal_id = max(set(c), key=c.count)
            self.tribes.tribal_wealth[tribal_id] += su + sp

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
        else:
            self.agent_dict.pop((v.prev_x, v.prev_y))
            self.agent_dict[v.x, v.y] = v