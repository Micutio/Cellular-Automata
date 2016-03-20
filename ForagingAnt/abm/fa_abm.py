#!/usr/bin/python
from abm.fa_agent import Ant

__author__ = 'Michael Wagner'
__version__ = '1.0'

# This is an ABM for a python implementation of Sugarscape.


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

    def cycle_system(self, ca):
        """
        Cycles through all agents and has them perceive and act in the world
        """
        # Have all agents perceive and act in a random order
        # While we're at it, look for dead agents to remove
        temp_dict = copy.deepcopy(self.agent_dict)
        for (_, _), v in temp_dict.items():
            if v:
                for agent in v:
                    agent.perceive_and_act(ca, self.agent_dict)
                    # In case the agent has updated it's position we change the position list accordingly.
                    self.update_position(agent)

    def add_agent(self, agent):
        """
        Adds an agent to be scheduled by the abm.
        """
        pos = (int(agent.x / self.gc.CELL_SIZE), int(agent.y / self.gc.CELL_SIZE))
        if pos in self.agent_dict:
            self.agent_dict[pos].append(agent)
        else:
            self.agent_dict[pos] = [agent]

    def draw_agents(self):
        """
        Iterates over all agents and draws them on the grid
        """
        for (_, _), v in self.agent_dict.items():
            for agent in v:
                self.visualizer.draw_agent(agent)

    def get_agent_at_position(self, x, y):
        for (_, _), v in self.agent_dict.items():
            for agent in v:
                if agent.x == x and agent.y == y:
                    return agent

    def update_position(self, v):
        x = int(v.prev_x / self.gc.CELL_SIZE)
        y = int(v.prev_y / self.gc.CELL_SIZE)
        if v.dead:
            # Remove dead agent from agent list on position p
            #self.agent_dict[v.prev_x, v.prev_y].remove(v)
            self.remove_agent(v)
        else:
            # Also remove agent from former position
            self.remove_agent(v)
            #self.agent_dict[v.prev_x, v.prev_y].remove(v)
            # ... and insert into new one
            self.add_agent(v)

        # If there is no one else at the old position left, delete it from the dict
        if not self.agent_dict[x, y]:
            self.agent_dict.pop((x, y))

    def remove_agent(self, agent):
        x = int(agent.prev_x / self.gc.CELL_SIZE)
        y = int(agent.prev_y / self.gc.CELL_SIZE)
        a_index = -1
        for a in self.agent_dict[x, y]:
            delete = a.a_id == agent.a_id
            if delete:
                a_index = self.agent_dict[x, y].index(a)
        if a_index > -1:
            self.agent_dict[x, y].pop(a_index)