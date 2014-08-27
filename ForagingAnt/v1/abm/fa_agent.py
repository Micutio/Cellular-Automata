__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import math
import copy


# TODO: Add diseases!
class Agent:
    def __init__(self, x, y, c_size, vision, max_pheromone):
        """
        Initializes an agent
        """
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.size = c_size
        self.vision = vision
        # State 0 = want home
        # State 1 = looking for food
        self.state = 1
        self.storage = 1
        self.max_pheromone = max_pheromone
        self.dead = False

    def move_and_act(self, cells):
        """
        Agent selects the best cell to move to, according to: its resources, occupier and tribal alignment.
        :param cells: A list of all cells+occupiers in my range of sight.
        """
        available_cells = []
        # At first filter out all cells we can not move to.
        while len(cells) > 0:
            c = cells.pop()
            # Only look at free cells
            if not c[1]:
                available_cells.append(c)

        # Secondly, find the field with highest reward. That basically means: maximize the welfare function!
        best_cells = []
        while len(available_cells) > 0:
            c = available_cells.pop()
            if not c[1]:
                # If we were on our way home and found it, stop right away and deliver the foraged food.
                if c[0].is_hive and self.state == 0:
                    best_cells = [c[0]]
                    break
                # If we found food (except in a hive near us) and we are looking for it,
                # accept only more cells that also have food
                if c[0].food > 0 and (not c[0].is_hive) and self.state == 1:
                    best_cells = [c[0]]
                    max_pheromone = self.max_pheromone + 1
                elif c[0].pheromones[self.state] > max_pheromone:
                    best_cells = [c[0]]
                    max_pheromone = c[0].pheromones[self.state]
                elif c[0].pheromones[self.state] == max_pheromone:
                    best_cells.append(c[0])

        # Pick a random cell from the best ones we found.
        c = random.choice(best_cells)
        # Leave pheromone on the cell
        if c.pheromones[1 - self.state] < self.max_pheromone:
            c.pheromones[1 - self.state] += 1
        # Save my current position...
        self.prev_x = self.x
        self.prev_y = self.y
        # ... and move to the new one.
        self.x = (c.x * self.size) + int(self.size / 2)
        self.y = (c.y * self.size) + int(self.size / 2)

        # If the new cell has food, then take some
        self.eat(c)
        self.store_in_hive(c)

    def eat(self, cell):
        if cell.food > 0 and not cell.is_hive:
            cell.food -= self.storage
            self.state = 0
            # In case we took more food than was on the cell
            if cell.food < 0:
                cell.food = 0

    def store_in_hive(self, cell):
        if cell.is_hive:
            cell.food += self.storage
            self.state = 1

    def perceive_and_act(self, ca, agent_positions):
        """
        Perceiving the environment and act according to the rules
        """
        vc = ca.get_visible_cells(agent_positions, self.x, self.y, self.vision)
        self.move_and_act(vc)