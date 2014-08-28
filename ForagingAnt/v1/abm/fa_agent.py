__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import math
import copy


# TODO: Add diseases!
class Agent:
    def __init__(self, x, y, c_size, vision, max_pheromone, max_dist):
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
        self.state = "food"
        self.not_state = "hive"
        self.storage = 1
        self.max_ph = max_pheromone
        self.dead = False
        self.hive_pos = None
        self.food_pos = None
        self.max_dist = max_dist

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
        best_hive_cells = []
        best_food_cells = []
        best_t_pheromone_cells = []
        best_nt_pheromone_cells = []
        max_t_ph = 0
        min_nt_ph = self.max_ph

        while len(available_cells) > 0:
            c = available_cells.pop()
            if not c[1]:
                # If we were on our way home and found it, stop right away and deliver the foraged food.
                if c[0].is_hive and self.state == "hive":
                    best_hive_cells.append(c[0])
                # If we found food (except in a hive near us) and we are looking for it,
                # accept only more cells that also have food
                elif c[0].food > 0 and (not c[0].is_hive) and self.state == "food":
                    best_food_cells.append(c[0])
                # If there is no food or hive, look at the cells pheromone.
                # If our target pheromone is available, take the cell with the highest amount
                elif c[0].pheromones[self.state] > 0:
                    if c[0].pheromones[self.state] > max_t_ph:
                        best_t_pheromone_cells = [c[0]]
                        max_t_ph = c[0].pheromones[self.state]
                    elif c[0].pheromones[self.state] == max_t_ph:
                        best_t_pheromone_cells.append(c[0])
                # If our target pheromone is not available, take the one with the least amount of pheromone
                elif c[0].pheromones[self.not_state] >= 0:
                    if c[0].pheromones[self.not_state] < min_nt_ph:
                        best_nt_pheromone_cells = [c[0]]
                        min_nt_ph = c[0].pheromones[self.not_state]
                    elif c[0].pheromones[self.not_state] == min_nt_ph:
                        best_nt_pheromone_cells.append(c[0])

        # Pick a random cell from the best ones we found.
        # Case 1: Agent is on the way back and found a hive cell.
        if self.state == "hive" and best_hive_cells:
            target_c = random.choice(best_hive_cells)
            self.move_to(target_c)
            self.store_in_hive(target_c)
            self.state = "food"
            self.not_state = "hive"
        # Case 2: Agent is looking for food and found some.
        elif self.state == "food" and best_food_cells:
            target_c = random.choice(best_food_cells)
            self.move_to(target_c)
            self.eat_from(target_c)
            self.state = "hive"
            self.not_state = "food"
        # Case 3: Agent found cells with target pheromones.
        elif best_t_pheromone_cells:
            target_c = random.choice(best_t_pheromone_cells)
            self.move_to(target_c)
        # Case 4: Agent found only cells with non target pheromones
        elif best_nt_pheromone_cells:
            target_c = random.choice(best_nt_pheromone_cells)
            self.move_to(target_c)

    def move_to(self, target_c):
        grid_x = int(self.x / self.size)
        grid_y = int(self.y / self.size)
        emitted_ph = 0

        if self.state == "food" and self.hive_pos:
            dist_to_hive = (abs(self.hive_pos[0] - grid_x) + abs(self.hive_pos[1] - grid_y))
            emitted_ph = ((self.max_dist - dist_to_hive) / self.max_dist) * self.max_ph
        elif self.food_pos:
            dist_to_food = (abs(self.food_pos[0] - grid_x) + abs(self.food_pos[1] - grid_y))
            emitted_ph = ((self.max_dist - dist_to_food) / self.max_dist) * self.max_ph

        target_c.pheromones[self.not_state] = int(emitted_ph)
        # Save my current position...
        self.prev_x = self.x
        self.prev_y = self.y
        # ... and move to the new one.
        self.x = (target_c.x * self.size) + int(self.size / 2)
        self.y = (target_c.y * self.size) + int(self.size / 2)

    def eat_from(self, target_c):
        if target_c.food > 0 and not target_c.is_hive:
            target_c.food -= self.storage
            self.food_pos = (target_c.x, target_c.y)
            # In case we took more food than was on the cell
            if target_c.food < 0:
                target_c.food = 0

    def store_in_hive(self, cell):
        if cell.is_hive:
            cell.food += self.storage

    def perceive_and_act(self, ca, agent_positions):
        """
        Perceiving the environment and act according to the rules
        """
        self.prev_x = self.x
        self.prev_y = self.y
        vc = ca.get_visible_cells(agent_positions, self.x, self.y, self.vision)
        self.move_and_act(vc)