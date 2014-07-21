__author__ = 'Michael Wagner'
__version__ = '2.0'

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


class AbstractAgent():
    """
    Interface for all agents in the system.
    """

    def __init__(self, x, y, size):
        """
        Initializer
        """
        self.x = x
        self.y = y
        self.size = size
        return

    def act(self, cells):
        """
        To be overwritten
        """
        return

    def draw(self, screen):
        """
        To be overwritten
        """
        return


class Agent(AbstractAgent):
    """
    Simple Agent class for a thermal creep variant
    """

    def __init__(self, x, y, size, team, min_density, strategy_walk, strategy_seed):
        """
        Initializer
        """
        super().__init__(x, y, size)
        self.team = team
        self.min_density = min_density
        self.strategy_walk = strategy_walk  # 0 - random, 1 - min-based, 2 - max-based
        self.strategy_seed = strategy_seed  # 0 - random, 1 - min-based, 2 - max-based

    def move(self, cells):
        """
        Lets the agent interact with the environment
        """
        # Step 1: move to a new cell, if possible
        if cells:
            possible_cells = [c for c in cells if c.temperature > 0]
            if len(possible_cells) > 0:
                if self.strategy_walk == 0:
                    cell = random.choice(possible_cells)
                elif self.strategy_walk == 1:
                    min_val = min(cells, key=attrgetter('temperature'))
                    c_list = [c for c in cells if c.temperature == min_val.temperature]
                    random.shuffle(c_list)
                    cell = random.choice(c_list)
                else:
                    max_val = max(cells, key=attrgetter('temperature'))
                    c_list = [c for c in cells if c.temperature == max_val.temperature]
                    random.shuffle(c_list)
                    cell = random.choice(c_list)
                self.x = (cell.x * self.size) + int(self.size / 2)
                self.y = (cell.y * self.size) + int(self.size / 2)

    def act(self, cells):
        if cells:
            if self.strategy_walk == 0:
                cell = random.choice(cells)
            elif self.strategy_walk == 1:
                min_val = min(cells, key=attrgetter('temperature'))
                c_list = [c for c in cells if c.temperature == min_val.temperature]
                random.shuffle(c_list)
                cell = random.choice(c_list)
            else:
                max_val = max(cells, key=attrgetter('temperature'))
                c_list = [c for c in cells if c.temperature == max_val.temperature]
                random.shuffle(c_list)
                cell = random.choice(c_list)
            cell.inc_temperature(self.team)

    def draw(self, surf):
        """
        Method for visualizing the agent
        """
        radius1 = int(self.size / 2)
        if self.team == 0:
            pygame.draw.circle(surf, (255, 0, 0), [self.x, self.y], radius1, 0)
        elif self.team == 1:
            pygame.draw.circle(surf, (255, 255, 0), [self.x, self.y], radius1, 0)
        elif self.team == 2:
            pygame.draw.circle(surf, (0, 255, 0), [self.x, self.y], radius1, 0)
        else:
            pygame.draw.circle(surf, (0, 0, 255), [self.x, self.y], radius1, 0)


class AgentBasedSystem:
    """
    Encapsulates all methods necessary to execute
    """
    def __init__(self, width, height, cell_size):
        """
        Initializer
        """
        self.agent_list = []
        self.width = width
        self.height = height
        self.cell_size = cell_size

    def add_agent(self, x, y, team, min_density, strategy_walk, strategy_seed):
        """
        Adding new agent to the system.
        """
        self.agent_list.append(Agent(x, y, self.cell_size, team, min_density, strategy_walk, strategy_seed))

    def cycle_agents(self, ca):
        for a in self.agent_list:
            cells = ca.get_cells_around(int(a.x / self.cell_size), int(a.y / self.cell_size))
            a.move(cells)
            cells = ca.get_cells_around(int(a.x / self.cell_size), int(a.y / self.cell_size))
            a.act(cells)

    def draw_agents(self, screen):
        for a in self.agent_list:
            a.draw(screen)

    def random_scenario(self, num_agents):
        loc = [(0, 0), (0, self.height), (self.width, 0), (self.width, self.height)]
        team = 0
        for l in loc:
            for _ in num_agents:
                self.add_agent(l[0], l[1], team, random.randint(0, 10), random.randint(0, 2), random.randint(0, 2))
            team += 1