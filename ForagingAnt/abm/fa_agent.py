__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import uuid
import math


class Agent:
    def __init__(self, x, y, c_size):
        self.a_id = uuid.uuid4().urn
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.size = c_size

    def perceive_and_act(self, ca, agent_list):
        return


class Hive(Agent):
    def __init__(self, x, y, c_size, abm, max_ants, max_pheromone):
        super().__init__(x, y, c_size)
        self.id = "hive"
        self.abm = abm
        self.max_ants = max_ants
        self.food = 0
        self.dead = False
        # Spawn all the ants.
        for i in range(self.max_ants):
            ant = Ant(self.x, self.y, self.size, max_pheromone)
            abm.add_agent(ant)

    def perceive_and_act(self, ca, agent_list):
        return


class Food(Agent):
    def __init__(self, x, y, c_size, amount):
        super().__init__(x, y, c_size)
        self.id = "food"
        self.food = amount
        self.dead = False

    def perceive_and_act(self, ca, agent_list):
        if self.food < 0:
            self.dead = True
        return


class Ant(Agent):
    def __init__(self, x, y, c_size, max_pheromone):
        """
        Initializes an agent
        """
        super().__init__(x, y, c_size)
        self.id = "ant"
        self.prev_x = x
        self.prev_y = y
        self.max_ph = max_pheromone
        self.food = 1
        self.has_food = False
        self.dead = False
        self.directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        self.current_dir = random.randint(0, 7)

    def perceive_and_act(self, ca, agent_positions):
        """
        Perceiving the environment and act according to the rules
        """
        self.prev_x = self.x
        self.prev_y = self.y
        neighborhood = ca.get_neighborhood(agent_positions, self.x, self.y)

        self.forage(neighborhood)

    def forage(self, neighborhood):
        if self.has_food:
            self.return_to_hive(neighborhood)
        else:
            self.find_food_source(neighborhood)

    def return_to_hive(self, neighborhood):
        cell = self.get_cell_with_pheromone("hive", neighborhood)
        if cell:
            x = int(self.x / self.size)
            y = int(self.y / self.size)
            this_cell = neighborhood[x, y]
            self.drop_pheromones("food", this_cell)
            self.move_to(cell[0])
            self.check_if_at_hive(cell[1])
        else:
            print('Ant Error: no valid hive bound cell found!')

    def find_food_source(self, neighborhood):
        cell = self.get_cell_with_pheromone("food", neighborhood)
        if cell:
            x = int(self.x / self.size)
            y = int(self.y / self.size)
            this_cell = neighborhood[x, y]
            self.drop_pheromones("hive", this_cell)
            self.move_to(cell[0])
            self.check_if_at_food(cell[1])
        else:
            print('Ant Error: no valid hive bound cell found!')

    def get_cell_with_pheromone(self, target_ph, neighborhood):
        result = None
        result_list = []
        backup_list = []
        best_cell = None
        max_ph = 0

        # Choose the possible directions the ants can currently look at.
        if self.current_dir == 7:
            possible_dirs = [6, 7, 0]
        elif self.current_dir == 0:
            possible_dirs = [7, 0, 1]
        else:
            possible_dirs = [self.current_dir -1, self.current_dir, self.current_dir + 1]

        for i in possible_dirs:
            d = self.directions[i]
            x = int(self.x / self.size) + d[0]
            y = int(self.y / self.size) + d[1]
            if (x, y) in neighborhood:
                cell = neighborhood[x, y]
                if cell[0].pheromones[target_ph] > 0 and (not cell[1] or len(cell[1]) < 10):
                    ph = cell[0].pheromones[target_ph]
                    if ph > max_ph:
                        best_cell = cell
                        max_ph = ph
                        self.current_dir = i
                    result_list.append((cell, ph, i))
                elif not cell[1] or len(cell[1]) < 10:
                    backup_list.append((cell, i))
        if result_list:
            if random.random() < 0.01:
                choice = weighted_choice(result_list)
                result = choice[0]
                self.current_dir = choice[1]
            else:
                result = best_cell
        elif backup_list:
            choice = random.choice(backup_list)
            result = choice[0]
            self.current_dir = choice[1]
        else:
            # print('Ant Error: no cells found to move to!')
            self.current_dir = get_opposite_direction(self.current_dir)
            return self.get_cell_with_pheromone(target_ph, neighborhood)
        return result

    def drop_pheromones(self, target_ph, cell):
        if cell[1]:
            for agent in cell[1]:
                # Check if one of the agents present on this cell is hive or food.
                if agent.id == target_ph:
                    cell[0].pheromones[target_ph] = self.max_ph
                    return

        max_ph = cell[0].last_neighbor_max_pheromone[target_ph]
        des = max_ph - 2
        d = des - cell[0].pheromones[target_ph]
        if d > 0:
            cell[0].pheromones[target_ph] += d
        return

    def move_to(self, target_c):
        # Save my current position...
        self.prev_x = self.x
        self.prev_y = self.y
        # ... and move to the new one.
        self.x = (target_c.x * self.size) + int(self.size / 2)
        self.y = (target_c.y * self.size) + int(self.size / 2)

    def check_if_at_hive(self, agents_at_cell):
        if agents_at_cell:
            for agent in agents_at_cell:
                if agent.id == "hive":
                    agent.food += self.food
                    self.has_food = False

    def check_if_at_food(self, agents_at_cell):
        if agents_at_cell:
            for agent in agents_at_cell:
                if agent.id == "food":
                    agent.food -= self.food
                    self.has_food = True


def weighted_choice(choices):
    total = sum(w for c, w, i in choices)
    r = random.uniform(0, total)
    up_to = 0
    for c, w, i in choices:
        if up_to + w > r:
            return c, i
        up_to += w
    assert False, "Shouldn't get here"

def get_opposite_direction(number):
    if number < 4:
        return number + 4
    else:
        return number - 1