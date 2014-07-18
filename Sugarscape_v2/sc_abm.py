__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is an ABM for a python implementation of Sugarscape.

import random
import pygame
import copy
import math

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
STARTING_SUGAR = (40, 80)

#########################################################################
###                            CLASSES                                ###
#########################################################################


class Agent:
    def __init__(self, g_id, x, y, c_size, su, sp, m_su, m_sp, v, g, f, d, c):
        """
        Initializes an agent
        """
        self.gene_id = g_id
        self.x = x
        self.y = y
        self.size = c_size
        self.prev_x = x
        self.prev_y = y
        self.init_sugar = su
        self.init_spice = sp
        self.sugar = su
        self.spice = sp
        self.metab_sugar = m_su
        self.metab_spice = m_sp
        self.vision = v
        self.gender = g
        self.fertility = f
        self.age = 1
        self.dying_age = d
        self.dead = False
        self.culture = c
        self.sugar_gathered = 0
        self.spice_gathered = 0
        self.sugar_traded = 0
        self.spice_traded = 0

    def visible_cells(self, ca):
        return ca.get_all_cells_in_vision(self.x, self.y, self.vision)

    def draw(self, surf):
        """
        Method for visualizing the agent
        """
        radius = int(self.size / 2)
        if not self.dead:
            col = self.get_color()
            pygame.draw.circle(surf, col[0], [self.x, self.y], radius, 0)
            pygame.draw.circle(surf, col[1], [self.x, self.y], radius - 2, 0)
        else:
            pygame.draw.circle(surf, (0, 0, 0), [self.x, self.y], radius, 0)

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

    def welfare(self, su, sp):
        """
        Relates the time the agent will die of lack of sugar with
        the time the agent will die of lack of spice.
        :param su:
        :param sp:
        :return:
        """
        metab_total = self.metab_sugar + self.metab_spice
        w1 = math.pow((self.sugar + su), (self.metab_sugar / metab_total))
        w2 = math.pow((self.spice + sp), (self.metab_spice / metab_total))
        return w1 * w2

    def mrs(self, su, sp):
        rate_sugar = (self.sugar + su) / self.metab_sugar
        rate_spice = (self.spice + sp) / self.metab_spice
        if rate_sugar > 0:
            return rate_spice / rate_sugar
        else:
            return 0

    def perceive_and_act(self, ca, agent_positions):
        """
        Perceiving the environment and act according to the rules
        """
        self.grow_older()
        self.prev_x = self.x
        self.prev_y = self.y
        self.sugar_gathered = 0
        self.spice_gathered = 0
        self.sugar_traded = 0
        self.spice_traded = 0
        if not self.dead:
            vc = ca.get_visible_cells(agent_positions, self.x, self.y, self.vision)
            self.r1_select_best_cell(vc)
            #nb = ca.get_neighborhood(agent_positions, self.x, self.y)
            vc = ca.get_visible_cells(agent_positions, self.x, self.y, self.vision)
            self.r2_reproduce(vc, agent_positions)
            self.r3_culture(vc)
            self.r4_trading(vc)

    def r1_select_best_cell(self, cells):
        grid_x = int(self.x / self.size)
        grid_y = int(self.y / self.size)
        if cells:
            search_starting_point = True
            result = []
            debug = []
            for c in cells:
                # First look for an unoccupied (or the own) cell to start with.
                if not c[1] or (c[1] and c[1].x == self.x and c[1].y == self.y):
                    if search_starting_point:
                        result.append(c[0])
                        max_w = self.welfare(c[0].sugar, c[0].spice)
                        max_dist = (abs(c[0].x - grid_x) + abs(c[0].y - grid_y))
                        search_starting_point = False
                    else:
                        # Then look whether we got higher sugar (clear list, take as new best)
                        # or it is closer and of same sugar as the best (clear list, take as new best)
                        # or identical to best (add to existing list)
                        dist = (abs(c[0].x - grid_x) + abs(c[0].y - grid_y))
                        welfare = self.welfare(c[0].sugar, c[0].spice)
                        if welfare >= max_w and dist < max_dist:
                            result = [c[0]]
                            max_w = welfare
                        elif welfare == max_w and dist == max_dist:
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
            self.x = (c.x * self.size) + int(self.size / 2)
            self.y = (c.y * self.size) + int(self.size / 2)
            # Additionally, try to eat from it
            self.eat_from_cell(c)

    def eat_from_cell(self, cell):
        self.sugar += cell.sugar
        self.spice += cell.spice
        self.sugar_gathered += cell.sugar
        self.spice_gathered += cell.spice
        cell.sugar = 0
        cell.spice = 0
        self.sugar -= self.metab_sugar
        self.spice -= self.metab_spice
        if self.sugar <= 0 or self.spice <= 0:
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
                both_wealthy1 = (self.sugar >= self.init_sugar and m.sugar >= m.init_sugar)
                both_wealthy2 = (self.spice >= self.init_spice and m.spice >= m.init_spice)
                if free_cells and m.is_fertile() and m.gender != self.gender and both_wealthy1 and both_wealthy2:
                    c = free_cells.pop()
                    n_id = self.gene_id + "|"
                    n_x = (c.x * self.size) + int(self.size / 2)
                    n_y = (c.y * self.size) + int(self.size / 2)
                    n_s = self.size
                    n_su = int(self.init_sugar / 2) + int(m.init_sugar / 2)
                    n_sp = int(self.init_spice / 2) + int(m.init_spice / 2)
                    self.sugar -= int(self.init_sugar / 2)
                    self.spice -= int(self.init_spice / 2)
                    m.sugar -= int(m.init_sugar / 2)
                    m.spice -= int(m.init_spice / 2)
                    n_m_su = int((self.metab_sugar + m.metab_spice) / 2)
                    n_m_sp = int((self.metab_sugar + m.metab_spice) / 2)
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
                    agent_positions[n_x, n_y] = Agent(n_id, n_x, n_y, n_s, n_su, n_sp, n_m_su, n_m_sp, n_v, n_g, n_f, n_d, n_c)

    def r3_culture(self, neighbors):
        for n in neighbors:
            if n[1]:
                index = random.choice(range(len(self.culture)))
                if n[1].culture[index] != self.culture[index]:
                    n[1].culture[index] = self.culture[index]

    def r4_trading(self, neighbors):
        for n in neighbors:
            if n[1] and not self.dead and not n[1].dead:
                w1 = self.mrs(0, 0)
                w2 = n[1].mrs(0, 0)
                if w1 < w2:
                    p = math.sqrt(w1 * w2)
                    # trade 1 unit of sugar for p units of spice, obey the constraints
                    if 1 <= p < n[1].spice and self.sugar > 1 and n[1].spice > p and self.mrs(-1, p) < n[1].mrs(1, -p):
                        self.sugar -= 1
                        self.spice += p
                        n[1].sugar += 1
                        n[1].spice -= p
                        self.sugar_traded += 1
                        self.spice_traded += p
                    elif 0 < p < 1 and self.sugar > int(1 / p) and n[1].spice > 1 and self.mrs(- int(1 / p), 1) < n[1].mrs(int(1 / p), -1):
                        self.sugar -= int(1 / p)
                        self.spice += 1
                        n[1].sugar += int(1 / p)
                        n[1].spice -= 1
                        self.sugar_traded += int(1 / p)
                        self.spice_traded += 1
                if w1 > w2:
                    p = math.sqrt(w1 * w2)
                    # trade 1 unit of sugar for p units of spice, obey the constraints
                    if 1 <= p < self.spice and n[1].sugar > 1 and self.spice > p and self.mrs(-1, p) < n[1].mrs(1, -p):
                        n[1].sugar -= 1
                        n[1].spice += p
                        self.sugar += 1
                        self.spice -= p
                        self.sugar_traded += 1
                        self.spice_traded += p
                    elif p < 1 and n[1].sugar > int(1 / p) and self.spice > 1 and n[1].mrs(- int(1 / p), 1) < self.mrs(int(1 / p), -1):
                        n[1].sugar -= int(1 / p)
                        n[1].spice += 1
                        self.sugar += int(1 / p)
                        self.spice -= 1
                        self.sugar_traded += int(1 / p)
                        self.spice_traded += 1


class ABM:
    def __init__(self, num_agents, c_size, min_x, max_x, min_y, max_y):
        """
        Initializes an abm with the given number of agents and returns it
        :return: An initialized ABM.
        """
        self.agent_dict = {}
        a_id = 0
        c = c_size
        r = int(c_size / 2)
        positions = [((x * c) + r, (y * c) + r) for x in range(min_x, max_x) for y in range(min_y, max_y)]
        positions = random.sample(positions, num_agents)
        random.shuffle(positions)
        for p in positions:
            metab_sugar = random.randint(MIN_METABOLISM, MAX_METABOLISM)
            metab_spice = random.randint(MIN_METABOLISM, MAX_METABOLISM)
            vision = random.randint(1, VISION)
            g = random.choice(["f", "m"])
            if g == "f":
                f = [F_FERTILITY_START, random.randint(F_FERTILITY_END[0], F_FERTILITY_END[1])]
            else:
                f = [M_FERTILITY_START, random.randint(M_FERTILITY_END[0], M_FERTILITY_END[1])]
            su = random.randint(STARTING_SUGAR[0], STARTING_SUGAR[1])
            sp = random.randint(STARTING_SUGAR[0], STARTING_SUGAR[1])
            d = random.randint(f[1], MAX_AGENT_LIFE)
            c = [random.getrandbits(1) for _ in range(11)]
            self.agent_dict[p[0], p[1]] = Agent(str(a_id), p[0], p[1], c_size, su, sp, metab_sugar, metab_spice, vision, g, f, d, c)
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
