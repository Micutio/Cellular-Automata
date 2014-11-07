__author__ = 'Michael Wagner'

import random

from cab_agent import Agent


class CellLifeAgent(Agent):
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)

    def clone(self, x, y):
        return CellLifeAgent(x, y, self.gc)

    def perceive_and_act(self, ca, abm):
        possible_cells = [cell for cell in ca.ca_grid.values() if
                          not (cell.x, cell.y) in abm.agent_locations
                          and abs(cell.x - self.x) < 2 and abs(cell.y - self.y) < 2]
        if possible_cells:
            new_cell = random.choice(possible_cells)
            abm.remove_agent(self)
            self.x = new_cell.x
            self.y = new_cell.y
            abm.add_agent(self)
        pass


class CellLifeSpawner(Agent):
    def __init__(self, x, y, gc):
        super().__init__(x, y, gc)

    def clone(self, x, y):
        return CellLifeSpawner(x, y, self.gc)

    def perceive_and_act(self, ca, abm):
        if len(abm.agent_locations) == 1:
            new_x = random.randint(0, self.gc.DIM_X)
            new_y = random.randint(0, self.gc.DIM_Y)
            _agent = CellLifeAgent(new_x, new_y, self.gc)
            abm.add_agent(_agent)
            abm.agent_list.append(_agent)
            print("added agent")
        pass