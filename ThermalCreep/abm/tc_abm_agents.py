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

    def __init__(self, x, y, size, team):
        """
        Initializer
        """
        self.x = x
        self.y = y
        self.size = size
        self.dead = False
        self.team = team
        return

    def act(self, cells):
        """
        To be overwritten
        """
        return

    def move(self, cells):
        """
        To be overwritten
        """
        return

    def draw(self, screen):
        """
        To be overwritten
        """
        return


class Creepling(AbstractAgent):
    """
    Simple Agent class for a thermal creep variant
    """

    def __init__(self, x, y, size, team, min_density, strategy_walk, strategy_seed, power):
        """
        Initializer
        """
        super().__init__(x, y, size, team)
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


class Hive(AbstractAgent):
    """
    Class for the creep-agents' headquarters.
    """

    def __init__(self, x, y, size, team):
        """
        Initializer
        """
        super().__init__(x, y, size, team)

    def act(self, cells):
        """
        To be overwritten
        """
        for c in cells:
            if c.team != self.team:
                self.dead = True
                break
        return

    def draw(self, surf):
        """
        Method for visualizing the agent
        """
        radius1 = int(self.size * 0.4)
        radius2 = int(self.size * 0.3)
        radius3 = int(self.size * 0.2)

        pygame.draw.circle(surf, (255, 255, 255), [self.x + self.size, self.y], radius2, 0)
        pygame.draw.circle(surf, (255, 255, 255), [self.x, self.y + self.size], radius2, 0)
        pygame.draw.circle(surf, (255, 255, 255), [self.x - self.size, self.y], radius2, 0)
        pygame.draw.circle(surf, (255, 255, 255), [self.x, self.y - self.size], radius2, 0)
        if self.team == 0:
            pygame.draw.circle(surf, (255, 0, 0), [self.x + self.size, self.y], radius3, 0)
            pygame.draw.circle(surf, (255, 0, 0), [self.x, self.y + self.size], radius3, 0)
            pygame.draw.circle(surf, (255, 0, 0), [self.x - self.size, self.y], radius3, 0)
            pygame.draw.circle(surf, (255, 0, 0), [self.x, self.y - self.size], radius3, 0)
        elif self.team == 1:
            pygame.draw.circle(surf, (255, 255, 0), [self.x + self.size, self.y], radius3, 0)
            pygame.draw.circle(surf, (255, 255, 0), [self.x, self.y + self.size], radius3, 0)
            pygame.draw.circle(surf, (255, 255, 0), [self.x - self.size, self.y], radius3, 0)
            pygame.draw.circle(surf, (255, 255, 0), [self.x, self.y - self.size], radius3, 0)
        elif self.team == 2:
            pygame.draw.circle(surf, (0, 255, 0), [self.x + self.size, self.y], radius3, 0)
            pygame.draw.circle(surf, (0, 255, 0), [self.x, self.y + self.size], radius3, 0)
            pygame.draw.circle(surf, (0, 255, 0), [self.x - self.size, self.y], radius3, 0)
            pygame.draw.circle(surf, (0, 255, 0), [self.x, self.y - self.size], radius3, 0)
        else:
            pygame.draw.circle(surf, (0, 0, 255), [self.x + self.size, self.y], radius3, 2)
            pygame.draw.circle(surf, (0, 0, 255), [self.x, self.y + self.size], radius3, 2)
            pygame.draw.circle(surf, (0, 0, 255), [self.x - self.size, self.y], radius3, 2)
            pygame.draw.circle(surf, (0, 0, 255), [self.x, self.y - self.size], radius3, 2)

        pygame.draw.line(surf, (0, 0, 0), [self.x, self.y], [self.x + self.size, self.y], 3)
        pygame.draw.line(surf, (0, 0, 0), [self.x, self.y], [self.x, self.y + self.size], 3)
        pygame.draw.line(surf, (0, 0, 0), [self.x, self.y], [self.x - self.size, self.y], 3)
        pygame.draw.line(surf, (0, 0, 0), [self.x, self.y], [self.x, self.y - self.size], 3)

        pygame.draw.circle(surf, (255, 255, 255), [self.x, self.y], radius1, 0)
        if self.team == 0:
            pygame.draw.circle(surf, (255, 0, 0), [self.x, self.y], radius2, 0)
        elif self.team == 1:
            pygame.draw.circle(surf, (255, 255, 0), [self.x, self.y], radius2, 0)
        elif self.team == 2:
            pygame.draw.circle(surf, (0, 255, 0), [self.x, self.y], radius2, 0)
        else:
            pygame.draw.circle(surf, (0, 0, 255), [self.x, self.y], radius2, 0)
