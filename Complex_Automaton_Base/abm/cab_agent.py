"""
This module contains all classes associated with the agents of the system.
"""

__author__ = 'Michael Wagner'

import uuid


class Agent:
    """
    Parent class for all agents.
    Every subclass has to implement the perceive_and_act() method.
    """
    def __init__(self, x, y, gc):
        self.a_id = uuid.uuid4().urn
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.size = gc.CELL_SIZE
        self.gc = gc
        self.dead = False

    def clone(self, x, y):
        return Agent(x, y, self.gc)

    def perceive_and_act(self, ca, abm):
        raise NotImplementedError("Method needs to be implemented")