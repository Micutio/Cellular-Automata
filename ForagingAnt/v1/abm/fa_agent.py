__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import uuid


class Agent:
    def __init__(self, x, y, c_size):
        self.a_id = uuid.uuid4()
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
        self.has_food = True
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
        # Get forward location with max hive_pheromone
        forward_positions = [self.current_dir - 1, self.current_dir, self.current_dir + 1]
        cell = self.get_best_cell_with_pheromone_in_direction("hive", forward_positions, neighborhood)

        # If we can't move forward (no suitable cells found in that direction) then try out other directions.
        if not cell:
            cell = self.get_best_cell_with_pheromone("hive", forward_positions, neighborhood)

        if cell:
            self.drop_pheromones("food", cell)
            self.move_to(cell[0])
            self.check_if_at_hive(cell[1])

    def find_food_source(self, neighborhood):
        # Get forward locations
        forward_positions = [self.current_dir - 1, self.current_dir, self.current_dir + 1]
        cell = self.get_best_cell_in_direction(forward_positions, neighborhood)

        # If we can't move forward (no suitable cells found in that direction) then try out other directions.
        if not cell:
            cell = self.get_best_cell(forward_positions, neighborhood)

        if cell:
            self.drop_pheromones("hive", cell)
            self.move_to(cell[0])
            self.check_if_at_hive(cell[1])

    def get_best_cell_with_pheromone_in_direction(self, target_ph, positions, neighborhood):
        max_ph = 0
        result = None
        result_list = []
        for p in positions:
            x = self.x + self.directions[p][0]
            y = self.y + self.directions[p][1]
            cell = neighborhood[x, y]
            if cell[0].pheromone[target_ph] > max_ph and len(cell[1]) < 10:
                result_list = [cell]
                max_ph = cell[0].pheromone[target_ph]
            elif cell[0].pheromone[target_ph] == max_ph and len(cell[1]) < 10:
                result_list.append(cell)
        if result_list:
            result = random.choice(result_list)
        return result

    def get_best_cell_with_pheromone(self, target_ph, positions, neighborhood):
        max_ph = 0
        result = None
        result_list = []
        pos_list = list(range(8))
        # Only look through the positions that are not in front of us.
        if positions:
            for p in positions:
                pos_list.remove(p)
        for p in pos_list:
            x = self.x + self.directions[p][0]
            y = self.y + self.directions[p][1]
            cell = neighborhood[x, y]
            if cell[0].pheromone[target_ph] > max_ph and len(cell[1]) < 10:
                result_list = [cell]
                max_ph = cell[0].pheromone[target_ph]
            elif cell[0].pheromone[target_ph] == max_ph and len(cell[1]) < 10:
                result_list.append((cell, p))
        if result_list:
            best = random.choice(result_list)
            # In case we got a result, change our current direction.
            self.current_dir = best[1]
            result = best[0]
        return result

    def get_best_cell_in_direction(self, positions, neighborhood):
        result = None
        result_list = []
        for p in positions:
            x = self.x + self.directions[p][0]
            y = self.y + self.directions[p][1]
            cell = neighborhood[x, y]
            if len(cell[1]) < 10:
                result_list.append(cell)
        if result_list:
            result = random.choice(result_list)
        return result

    def get_best_cell(self, positions, neighborhood):
        result = None
        result_list = []
        pos_list = list(range(8))
        # Only look through the positions that are not in front of us.
        if positions:
            for p in positions:
                pos_list.remove(p)
        for p in pos_list:
            x = self.x + self.directions[p][0]
            y = self.y + self.directions[p][1]
            cell = neighborhood[x, y]
            if len(cell[1]) < 10:
                result_list.append((cell, p))
        if result_list:
            best = random.choice(result_list)
            # In case we got a result, change our current direction.
            self.current_dir = best[1]
            result = best[0]
        return result

    def drop_pheromones(self, target_ph, cell):
        if cell[1]:
            for agent in cell[1]:
                if agent.id == target_ph:
                    cell[0].pheromones[target_ph] = self.max_ph
                else:
                    max_ph = cell[0].neighbor_max_pheromone[target_ph]
                    des = max_ph - 2
                    d = des - cell[0].pheromones[target_ph]
                    if d > 0:
                        cell[0].pheromones[target_ph] = d

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