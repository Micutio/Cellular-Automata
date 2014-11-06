__author__ = 'Michael Wagner'

from cab_agent import Agent


class CellLifeAgent(Agent):
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)

    def clone(self, x, y):
        return CellLifeAgent(x, y, self.gc)

    def perceive_and_act(self, ca, agent_list, agent_locations):
        pass