__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is an ABM for a python implementation of Sugarscape.

import random

from abm.sc_agent import Agent
from abm.sc_tribes import Tribes
from abm.sc_diseases import Bacteria, Virus


class ABM:
    def __init__(self, visualizer, gc):
        """
        Initializes an abm with the given number of agents and returns it
        :return: An initialized ABM.
        """
        self.agent_dict = {}
        self.agent_list = []
        self.tribes = Tribes(gc.NUM_TRIBES)
        self.visualizer = visualizer
        self.gc = gc
        total_wealth = 0
        c = gc.CELL_SIZE
        r = int(gc.CELL_SIZE / 2)
        # Create a list with possible spawn positions for every tribe, then pack them all into a list.
        position_list = []
        for b in gc.ABM_BOUNDS:
            positions = [((x * c) + r, (y * c) + r) for x in range(b[0], b[1]) for y in range(b[2], b[3])]
            random.shuffle(positions)
            position_list.append(positions)

        for _ in range(gc.NUM_AGENTS):
            meta_sugar = random.randint(gc.MIN_METABOLISM, gc.MAX_METABOLISM)
            meta_spice = random.randint(gc.MIN_METABOLISM, gc.MAX_METABOLISM)
            vision = random.randint(1, gc.VISION + 1)
            g = random.choice([0, 1])
            if g == 1:
                f = (gc.F_FERTILITY_START, random.randint(gc.F_FERTILITY_END[0], gc.F_FERTILITY_END[1]))
            else:
                f = (gc.M_FERTILITY_START, random.randint(gc.M_FERTILITY_END[0], gc.M_FERTILITY_END[1]))
            su = random.randint(gc.STARTING_SUGAR[0], gc.STARTING_SUGAR[1])
            sp = random.randint(gc.STARTING_SUGAR[0], gc.STARTING_SUGAR[1])
            d = random.randint(f[1], gc.MAX_AGENT_LIFE)
            c = [random.randint(0, gc.NUM_TRIBES - 1) for _ in range(11)]
            imm_sys = [random.getrandbits(gc.NUM_TRIBES - 1) for _ in range(gc.IMMUNE_SYSTEM_GENOME_LENGTH)]
            a = 0  # random.randint(0, int(gc.MAX_AGENT_LIFE / 2))
            gene_string = "{0:03b}".format(meta_sugar) + "{0:03b}".format(meta_spice)\
                          + "{0:06b}".format(su) + "{0:06b}".format(sp) \
                          + "{0:03b}".format(vision) + "{0:01b}".format(g)\
                          + "{0:06b}".format(f[0]) + "{0:06b}".format(f[1]) + "{0:07b}".format(d)
            # We use generation to keep track of how far an agent has walked down the evolutionary road.
            generation = (0, 0)
            genome = (gene_string, gene_string, c, imm_sys, generation)

            # Retrieve a spawn position from the position list belonging to its tribe.
            tribe_id = max(set(c), key=c.count)
            random.shuffle(position_list[tribe_id])
            p = position_list[tribe_id].pop()
            # Create the new agent and add to both, dictionary and list.
            new_agent = Agent(p[0], p[1], gc.CELL_SIZE, su, sp, genome, a, self.tribes)
            self.agent_dict[p[0], p[1]] = new_agent
            self.agent_list.append(new_agent)

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
        new_agents = []
        for a in self.agent_list:
            a.perceive_and_act(ca, self.agent_dict, new_agents)
            self.spawn_disease()
        self.agent_list.extend(new_agents)

    def draw_agents(self):
        """
        Iterates over all agents and draws them on the grid
        """
        draw = self.visualizer.draw_agent
        for v in self.agent_dict.values():
            draw(v)

    def spawn_disease(self):
        """
        Have a small chance of spawning a disease in a random agent.
        """
        if random.random() < 0.0001:
            # 50% chance of either, bacterial or viral infection
            dis_genome = [random.getrandbits(1) for _ in range(self.gc.DISEASE_GENOME_LENGTH)]

            # Choose a random agent as victim
            victim = random.choice(list(self.agent_dict.values()))
            if len(victim.diseases) == 0:
                if random.choice([0, 1]) == 0:
                    disease = Bacteria(dis_genome)
                    print(" > bacterial infection spawned: %s" % disease.genome_string)
                else:
                    disease = Virus(dis_genome)
                    print(" > viral infection spawned: %s" % disease.genome_string)
                victim.diseases[disease.genome_string] = disease