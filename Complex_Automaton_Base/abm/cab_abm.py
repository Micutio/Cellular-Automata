"""
This module contains all classes associated with the agent based system,
except for the agent classes themselves.
"""

__author__ = 'Michael Wagner'


class ABM:
    def __init__(self, visualizer, gc):
        """
        Initializes an abm with the given number of agents and returns it.
        :param visualizer: Necessary for graphical output of the agents.
        :param gc: Global Constants, Parameters for the ABM.
        :return: An initialized ABM.
        """
        self.agent_locations = {}
        self.agent_list = []
        self.visualizer = visualizer
        self.gc = gc

    def cycle_system(self, ca):
        """
        Cycles through all agents and has them perceive and act in the world
        """
        # Have all agents perceive and act in a random order
        # While we're at it, look for dead agents to remove
        for a in self.agent_list:
            a.perceive_and_act(ca, self.agent_locations, self.agent_list)
        self.agent_list = [agent for agent in self.agent_list if not agent.dead]

    def add_agent(self, agent):
        """
        Adds an agent to be scheduled by the abm.
        """
        pos = (int(agent.x / self.gc.CELL_SIZE), int(agent.y / self.gc.CELL_SIZE))
        if pos in self.agent_locations:
            self.agent_locations[pos].append(agent)
        else:
            self.agent_locations[pos] = [agent]

    def draw_agents(self):
        """
        Iterates over all agents and hands them over to the visualizer.
        """
        draw = self.visualizer.draw_agent
        for a in self.agent_list:
            draw(a)

    def remove_agent(self, agent):
        x = int(agent.prev_x / self.gc.CELL_SIZE)
        y = int(agent.prev_y / self.gc.CELL_SIZE)
        a_index = -1
        for a in self.agent_locations[x, y]:
            if a.a_id == agent.a_id:
                a_index = self.agent_locations[x, y].index(a)
                break
        if a_index != -1:
            self.agent_locations[x, y].pop(a_index)