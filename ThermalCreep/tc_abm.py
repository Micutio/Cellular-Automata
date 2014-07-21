__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import random
from operator import attrgetter

#########################################################################
###                       Global Variables                            ###
#########################################################################

# Insert any global variable for the agents.

#########################################################################
###                            CLASSES                                ###
#########################################################################


class Agent():
    """
    Simple Agent class for a thermal creep variant
    """
    def __init__(self, x, y, size, rand_act):
        """
        Initializer
        """
        self.x = x
        self.y = y
        self.size = size
        self.rand_act = rand_act

    def move(self, cells):
        """
        Lets the agent interact with the environment
        """
        # Step 1: move to a new cell, if possible
        if cells:
            possible_cells = [c for c in cells if c.temperature > 0]
            if len(possible_cells) > 0:
                if self.rand_act:
                    cell = random.choice(possible_cells)
                else:
                    min_val = min(cells, key=attrgetter('temperature'))
                    c_list = [c for c in cells if c.temperature == min_val.temperature]
                    random.shuffle(c_list)
                    cell = random.choice(c_list)
                self.x = (cell.x * self.size) + int(self.size / 2)
                self.y = (cell.y * self.size) + int(self.size / 2)

    def act(self, cells):
        if cells:
            if self.rand_act:
                cell = random.choice(cells)
                cell.inc_temperature()
            else:
                min_val = min(cells, key=attrgetter('temperature'))
                c_list = [c for c in cells if c.temperature == min_val.temperature]
                random.shuffle(c_list)
                cell = random.choice(c_list)
                cell.inc_temperature()

    def draw(self, surf):
        """
        Method for visualizing the agent
        """
        if self.rand_act:
            pygame.draw.circle(surf, (255, 255, 255), [self.x, self.y], int(self.size / 2), 0)
        else:
            pygame.draw.circle(surf, (0, 0, 0), [self.x, self.y], int(self.size / 2), 0)


class AgentBasedSystem:
    """
    Encapsulates all methods necessary to execute
    """
    def __init__(self, cell_size):
        """
        Initializer
        """
        self.agent_list = []
        self.cell_size = cell_size

    def add_agent(self, x, y, act_rand):
        """
        Adding new agent to the system.
        """
        self.agent_list.append(Agent(x, y, self.cell_size, act_rand))

    def cycle_agents(self, ca):
        for a in self.agent_list:
            cells = ca.get_cells_around(int(a.x / self.cell_size), int(a.y / self.cell_size))
            a.move(cells)
            cells = ca.get_cells_around(int(a.x / self.cell_size), int(a.y / self.cell_size))
            a.act(cells)

    def draw_agents(self, screen):
        for a in self.agent_list:
            a.draw(screen)