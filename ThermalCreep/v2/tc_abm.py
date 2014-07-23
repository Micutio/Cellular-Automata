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
        self.dead = False
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

    def __init__(self, x, y, size, team, min_density, strategy_walk, strategy_seed, power):
        """
        Initializer
        """
        super().__init__(x, y, size)
        self.team = team
        self.min_density = min_density
        self.strategy_walk = strategy_walk  # 0 - random, 1 - min-based
        self.strategy_seed = strategy_seed  # 0 - random, 1 - min-based
        self.score = 0
        self.power = power

    def move(self, cells):
        """
        Lets the agent interact with the environment
        """
        possible_cells = [c for c in cells if self.team == c.team and c.temperature >= self.min_density]
        if possible_cells:
            if self.strategy_walk == 0:
                random.shuffle(possible_cells)
                cell = random.choice(possible_cells)
            else:  # self.strategy_walk == 1:
                min_val = min(possible_cells, key=attrgetter('temperature'))
                c_list = [c for c in possible_cells if c.temperature == min_val.temperature]
                random.shuffle(c_list)
                cell = random.choice(c_list)

            self.x = (cell.x * self.size) + int(self.size / 2)
            self.y = (cell.y * self.size) + int(self.size / 2)
        else:
            self.dead = True

    def act(self, cells):
        possible_cells = [c for c in cells if self.team == c.team]
        if possible_cells:
            if self.strategy_walk == 0:
                random.shuffle(cells)
                cell = random.choice(cells)
            else:
                min_val = min(possible_cells, key=attrgetter('temperature'))
                c_list = [c for c in possible_cells if c.temperature == min_val.temperature]
                c_list.extend([c for c in cells if self.team != c.team])
                random.shuffle(c_list)
                cell = random.choice(c_list)
            self.score += cell.inc_temperature(self.team, self.power)
        else:
            self.dead = True

    def draw(self, surf):
        """
        Method for visualizing the agent
        """
        radius1 = int(self.size / 2)
        radius2 = int(radius1 * 0.6)
        pygame.draw.circle(surf, (255, 255, 255), [self.x, self.y], radius1, 0)
        if self.team == 0:
            pygame.draw.circle(surf, (255, 0, 0), [self.x, self.y], radius2, 0)
        elif self.team == 1:
            pygame.draw.circle(surf, (255, 255, 0), [self.x, self.y], radius2, 0)
        elif self.team == 2:
            pygame.draw.circle(surf, (0, 255, 0), [self.x, self.y], radius2, 0)
        else:
            pygame.draw.circle(surf, (0, 0, 255), [self.x, self.y], radius2, 0)


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

    def add_agent(self, x, y, team, min_density, strategy_walk, strategy_seed, power):
        """
        Adding new agent to the system.
        """
        self.agent_list.append(Agent(x, y, self.cell_size, team, min_density, strategy_walk, strategy_seed, power))

    def cycle_agents(self, ca):
        for a in self.agent_list:
            if not a.dead:
                cells = ca.get_cells_around(int(a.x / self.cell_size), int(a.y / self.cell_size))
                a.move(cells)
                cells = ca.get_cells_around(int(a.x / self.cell_size), int(a.y / self.cell_size))
                a.act(cells)

    def draw_agents(self, screen):
        for a in self.agent_list:
            if not a.dead:
                a.draw(screen)

    def random_scenario(self, num_agents, min_density, power, ca):
        loc = [(5, 5), (5, self.height - 5), (self.width - 5, 5), (self.width - 5, self.height - 5)]
        team = 0
        for l in loc:
            for _ in range(num_agents):
                walk = random.randint(0, 1)
                seed = random.randint(0, 1)
                self.add_agent(l[0], l[1], team, min_density, walk, seed, power)
            ca_x = int(l[0] / self.cell_size)
            ca_y = int(l[1] / self.cell_size)
            ca.ca_grid[ca_x, ca_y].team = team
            ca.ca_grid[ca_x, ca_y].temperature = min_density
            team += 1