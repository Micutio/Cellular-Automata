from v2.abm.tc_abm_agents import Creepling, Hive

__author__ = 'Michael Wagner'
__version__ = '2.0'

import random

#########################################################################
###                       Global Variables                            ###
#########################################################################

# Insert any global variable for the agents.

#########################################################################
###                            CLASSES                                ###
#########################################################################


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
        self.agent_list.append(Creepling(x, y, self.cell_size, team, min_density, strategy_walk, strategy_seed, power))

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
        a = int(self.cell_size / 2)
        loc = [(a, a), (a, self.height - a), (self.width - a, a), (self.width - a, self.height - a)]
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

    def hive_scenario(self, num_agents, min_density, power, ca):
        w = int(self.width / 10)
        h = int(self.height / 10)
        a = int(self.cell_size / 2)
        loc = [(w + a, h + a), (w + a, self.height - h - a), (self.width - w - a, h + a), (self.width - w - a, self.height - h - a)]
        team = 0
        for l in loc:
            for _ in range(num_agents):
                walk = random.randint(0, 1)
                seed = random.randint(0, 1)
                self.add_agent(l[0], l[1], team, min_density, walk, seed, power)
            self.agent_list.append(Hive(l[0], l[1], self.cell_size, team))
            ca_x = int(l[0] / self.cell_size)
            ca_y = int(l[1] / self.cell_size)
            ca.ca_grid[ca_x, ca_y].team = team
            ca.ca_grid[ca_x, ca_y].temperature = min_density
            ca.ca_grid[ca_x + 1, ca_y].temperature = min_density * 2
            ca.ca_grid[ca_x, ca_y + 1].temperature = min_density * 2
            ca.ca_grid[ca_x - 1, ca_y].temperature = min_density * 2
            ca.ca_grid[ca_x, ca_y - 1].temperature = min_density * 2
            ca.ca_grid[ca_x + 1, ca_y].team = team
            ca.ca_grid[ca_x, ca_y + 1].team = team
            ca.ca_grid[ca_x - 1, ca_y].team = team
            ca.ca_grid[ca_x, ca_y - 1].team = team
            team += 1