#!/usr/bin/python
from v1.abm.fa_agent import Agent

__author__ = 'Michael Wagner'
__version__ = '1.0'

# This is an ABM for a python implementation of Sugarscape.

import random
import copy


class ABM:
    def __init__(self, visualizer, gc):
        """
        Initializes an abm with the given number of agents and returns it
        :return: An initialized ABM.
        """
        self.agent_dict = {}
        self.visualizer = visualizer
        self.gc = gc

        c = gc.CELL_SIZE
        r = int(gc.CELL_SIZE / 2)
        # Create a list with possible spawn positions for every tribe, then pack them all into a list.
        position_list = []
        for b in gc.ABM_BOUNDS:
            positions = [((x * c) + r, (y * c) + r) for x in range(b[0], b[1]) for y in range(b[2], b[3])]
            random.shuffle(positions)
            position_list.append(positions)

        for _ in range(gc.NUM_AGENTS):
            p = random.choice(position_list[0])
            self.agent_dict[p[0], p[1]] = Agent(p[0], p[1], gc.CELL_SIZE, gc.VISION, gc.MAX_PHEROMONE)

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
            self.agent_dict.pop((v.prev_x, v.prev_y))
        #elif v.x != v.prev_x or v.y != v.prev_y:
        else:
            self.agent_dict.pop((v.prev_x, v.prev_y))
            self.agent_dict[v.x, v.y] = v
