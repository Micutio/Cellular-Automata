#!/usr/bin/python

__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is an ABM for a python implementation of Sugarscape.

import random
import pygame
import math
import copy

#########################################################################
###                       Global Variables                            ###
#########################################################################

# Insert any global variable for the agents.
MIN_METABOLISM = 1
MAX_METABOLISM = 4
VISION = 6
M_FERTILITY_START = 15
F_FERTILITY_START = 15
M_FERTILITY_END = (50, 60)
F_FERTILITY_END = (40, 50)
MAX_AGENT_LIFE = 100
STARTING_SUGAR = (80, 120)

#########################################################################
###                            CLASSES                                ###
#########################################################################


class Agent:
    def __init__(self, g_id, x, y, s, m, v, g, f, d, c):
        """
        Initializes an agent
        """
        self.gene_id = g_id
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.init_sugar = s
        self.sugar = s
        self.metabolism = m
        self.vision = v
        self.gender = g
        self.fertility = f
        self.age = 1
        self.dying_age = d
        self.culture = c
        self.dead = False
        self.radius = 5

    def visible_cells(self, ca):
        return ca.get_all_cells_in_vision(self.x, self.y, self.vision)

    def draw(self, surf):
        """
        Method for visualizing the agent
        """
        if not self.dead:
            col = self.get_color()
            pygame.draw.circle(surf, col[0], [self.x, self.y], self.radius, 0)
            pygame.draw.circle(surf, col[1], [self.x, self.y], self.radius - 2, 0)
        else:
            pygame.draw.circle(surf, (0, 0, 0), [self.x, self.y], self.radius, 0)

    def get_color(self):
        # First color: the ring
        r0 = g0 = b0 = 0
        if self.is_fertile():
            ratio = 1 - (self.age / MAX_AGENT_LIFE)
            if self.gender == "m":
                b0 = 255 * ratio
            else:
                r0 = 255 * ratio
        elif self.age > self.fertility[1]:
            r0 = g0 = b0 = 80
        elif self.age < self.fertility[0]:
            r0 = g0 = 150
            b0 = 0
        if self.culture.count(0) > self.culture.count(1):
            r1 = g1 = b1 = 0
        else:
            r1 = g1 = b1 = 255
        return [(r0, g0, b0), (r1, g1, b1)]

    def is_fertile(self):
        return self.fertility[0] <= self.age <= self.fertility[1]

    def grow_older(self):
        self.age += 1
        if self.age >= self.dying_age:
            self.dead = True

    def perceive_and_act(self, ca, agent_positions):
        """
        Perceiving the environment and act according to the rules
        """
        self.grow_older()
        self.prev_x = self.x
        self.prev_y = self.y
        if not self.dead:
            vc = ca.get_visible_cells(agent_positions, self.x, self.y, self.vision)
            self.r1_select_best_cell(vc)
            #nb = ca.get_neighborhood(agent_positions, self.x, self.y)
            vc = ca.get_visible_cells(agent_positions, self.x, self.y, self.vision)
            self.r2_reproduce(vc, agent_positions)
            self.r3_culture(vc)

    def r1_select_best_cell(self, cells):
        grid_x = int(self.x / 10)
        grid_y = int(self.y / 10)

        if cells:
            search_starting_point = True
            result = []
            debug = []
            for c in cells:
                if not c[1] or (c[1] and c[1].x == self.x and c[1].y == self.y):
                    # First look for an unoccupied (or the own) cell to start with.
                    if search_starting_point:
                        result.append(c[0])
                        max_c = c[0]
                        search_starting_point = False
                    else:
                        # Then look whether we got higher sugar (clear list, take as new best)
                        # or it is closer and of same sugar as the best (clear list, take as new best)
                        # or identical to best (add to existing list)
                        dist1 = (abs(c[0].x - grid_x) + abs(c[0].y - grid_y))
                        dist2 = (abs(max_c.x - grid_x) + abs(max_c.y - grid_y))
                        if c[0].sugar > max_c.sugar or (c[0].sugar == max_c.sugar and dist1 < dist2):
                            result = [c[0]]
                            max_c = c[0]
                        elif c[0].sugar == max_c.sugar and dist1 == dist2:
                            result.append(c[0])

            # In this case we didn't find any good cell
            if search_starting_point or not result:
                print('This should be impossible to happen')
                for msg in debug:
                    print(msg)

            # Pick one of the best cells (if there are multiple)
            # and set it as new position for this agent
            random.shuffle(result)
            c = random.choice(result)
            self.prev_x = self.x
            self.prev_y = self.y
            self.x = (c.x * 10) + 5
            self.y = (c.y * 10) + 5
            # Additionally, try to eat from it
            self.eat_from_cell(c)

    def eat_from_cell(self, cell):
        self.sugar += cell.sugar
        cell.sugar = 0
        self.sugar -= self.metabolism
        if self.sugar <= 0:
            self.dead = True

    def r2_reproduce(self, neighbors, agent_positions):
        if self.is_fertile():
            free_cells = []
            mates = []
            for nb in neighbors:
                if nb[1]:
                    mates.append(nb[1])
                else:
                    free_cells.append(nb[0])
            if mates:
                m = random.choice(mates)
                both_wealthy = (self.sugar >= self.init_sugar and m.sugar >= m.init_sugar)
                if free_cells and m.is_fertile() and m.gender != self.gender and both_wealthy:
                    c = free_cells.pop()
                    n_id = self.gene_id + "|"
                    n_x = (c.x * 10) + 5
                    n_y = (c.y * 10) + 5
                    n_s = int(self.init_sugar / 2) + int(m.init_sugar / 2)
                    self.sugar -= int(self.init_sugar / 2)
                    m.sugar -= int(m.init_sugar / 2)
                    n_m = int((self.metabolism + m.metabolism) / 2)
                    n_v = random.choice([self.vision, m.vision])
                    n_g = random.choice([self.gender, m.gender])
                    if n_g == self.gender:
                        n_f = self.fertility
                    else:
                        n_f = m.fertility
                    d1 = self.dying_age
                    d2 = m.dying_age
                    n_d = random.randint(min(d1, d2), max(d1, d2))
                    n_c = []
                    for bit in range(len(self.culture)):
                        if self.culture[bit] == m.culture[bit]:
                            n_c.append(self.culture[bit])
                        else:
                            n_c.append(random.choice([self.culture[bit], m.culture[bit]]))
                    agent_positions[n_x, n_y] = Agent(n_id, n_x, n_y, n_s, n_m, n_v, n_g, n_f, n_d, n_c)

    def r3_culture(self, neighbors):
        for n in neighbors:
            if n[1]:
                index = random.choice(range(len(self.culture)))
                if n[1].culture[index] != self.culture[index]:
                    n[1].culture[index] = self.culture[index]

class ABM:
    def __init__(self, num_agents, min_x, max_x, min_y, max_y):
        """
        Initializes an abm with the given number of agents and returns it
        :return: An initialized ABM.
        """
        self.agent_dict = {}
        a_id = 0
        positions = [((x * 10) + 5, (y * 10) + 5) for x in range(min_x, max_x) for y in range(min_y, max_y)]
        positions = random.sample(positions, num_agents)
        random.shuffle(positions)
        for p in positions:
            metabolism = random.randint(MIN_METABOLISM, MAX_METABOLISM)
            vision = random.randint(1, VISION)
            g = random.choice(["f", "m"])
            if g == "f":
                f = [F_FERTILITY_START, random.randint(F_FERTILITY_END[0], F_FERTILITY_END[1])]
            else:
                f = [M_FERTILITY_START, random.randint(M_FERTILITY_END[0], M_FERTILITY_END[1])]
            s = random.randint(STARTING_SUGAR[0], STARTING_SUGAR[1])
            d = random.randint(f[1], MAX_AGENT_LIFE)
            c = [random.getrandbits(1) for _ in range(11)]
            self.agent_dict[p[0], p[1]] = Agent(str(a_id), p[0], p[1], s, metabolism, vision, g, f, d, c)
            a_id += 1

    def cycle_system(self, ca):
        """
        Cycles through all agents and has them perceive and act in the world
        """
        # Have all agents perceive and act in a random order
        # While we're at it, look for dead agents to remove
        temp_dict = copy.deepcopy(self.agent_dict)
        for (_, _), v in temp_dict.items():
            v.perceive_and_act(ca, self.agent_dict)
            # In case the agent has updated it's position we change the position list accordingly.
            self.update_position(v)

    def draw_agents(self, surf):
        """
        Iterates over all agents and draws them on the grid
        """
        for (_, _), v in self.agent_dict.items():
            v.draw(surf)

    def get_agent_at_position(self, x, y):
        for (_, _), v in self.agent_dict.items():
            if v.x == x and v.y == y:
                return v

    def update_position(self, v):
        if v.dead:
            self.agent_dict.pop((v.prev_x, v.prev_y))
        #elif v.x != v.prev_x or v.y != v.prev_y:
        else:
            self.agent_dict.pop((v.prev_x, v.prev_y))
            self.agent_dict[v.x, v.y] = v


#########################################################################
###                          GLOBAL METHODS                           ###
#########################################################################
