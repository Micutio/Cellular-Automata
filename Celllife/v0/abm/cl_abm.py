#!/usr/bin/python
from v0.abm.cl_agent import BioCell

__author__ = 'Michael Wagner'
__version__ = '1.0'

# This is an ABM for a python implementation of Sugarscape.


import copy
import math
import random


class ABM:
    def __init__(self, visualizer, gc):
        """
        Initializes an abm with the given number of agents and returns it
        :return: An initialized ABM.
        """
        self.agent_dict = {}
        self.agent_list = []
        self.new_agents = []
        self.visualizer = visualizer
        self.gc = gc

    def cycle_system(self, ca):
        """
        Cycles through all agents and has them perceive and act in the world
        """
        # Have all agents perceive and act in a random order
        # While we're at it, look for dead agents to remove
        self.spawn_agent()
        for agent in self.agent_list:
            agent.perceive_and_act(ca, self, self.agent_dict)
            # In case the agent has updated it's position we change the position list accordingly.
            self.update_position(agent)
        self.agent_list = [agent for agent in self.agent_list if not agent.dead]
        if self.new_agents:
            self.agent_list.extend(self.new_agents)
            self.new_agents = []

    def spawn_agent(self):
        if not self.agent_dict:
            x = random.randint(0, self.gc.DIM_X)
            y = random.randint(0, self.gc.DIM_Y)
            x = (math.floor(x) * self.gc.CELL_SIZE) + int(self.gc.CELL_SIZE / 2)
            y = (math.floor(y) * self.gc.CELL_SIZE) + int(self.gc.CELL_SIZE / 2)
            dna = [random.randint(0, 1) for _ in range(64)]
            dna[0] = 0
            agent = BioCell(x, y, self.gc.CELL_SIZE, dna)
            self.add_agent(agent)
            #print("Cell created! %s" % agent.a_id)

    def add_agent(self, agent):
        """
        Adds an agent to be scheduled by the abm.
        """
        pos = (int(agent.x / self.gc.CELL_SIZE), int(agent.y / self.gc.CELL_SIZE))
        if pos in self.agent_dict:
            self.agent_dict[pos].append(agent)
        else:
            self.agent_dict[pos] = [agent]
        self.new_agents.append(agent)

    def draw_agents(self):
        """
        Iterates over all agents and draws them on the grid
        """
        for a_list in self.agent_dict.values():
            for agent in a_list:
                self.visualizer.draw_agent(agent)

    def get_agent_at_position(self, x, y):
        for (_, _), v in self.agent_dict.items():
            for agent in v:
                if agent.x == x and agent.y == y:
                    return agent

    def update_position(self, agent):
        x = int(agent.prev_x / self.gc.CELL_SIZE)
        y = int(agent.prev_y / self.gc.CELL_SIZE)
        if agent.dead:
            # Remove dead agent from agent list on position p
            #self.agent_dict[v.prev_x, v.prev_y].remove(v)
            self.remove_agent(agent, x, y)
            #print("Cell died! %s" % agent.a_id)
        elif agent.x != agent.prev_x or agent.y != agent.prev_y:
            # Also remove agent from former position
            self.remove_agent(agent)
            #self.agent_dict[v.prev_x, v.prev_y].remove(v)
            # ... and insert into new one
            self.add_agent(agent)

        # If there is no one else at the old position left, delete it from the dict
        if not self.agent_dict[x, y]:
            self.agent_dict.pop((x, y))

    def remove_agent(self, agent, x, y):
        a_index = -1
        for a in self.agent_dict[x, y]:
            delete = a.a_id == agent.a_id
            if delete:
                a_index = self.agent_dict[x, y].index(a)
        if a_index > -1:
            self.agent_dict[x, y].pop(a_index)