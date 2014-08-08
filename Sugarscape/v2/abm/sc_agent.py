__author__ = 'Michael Wagner'
__version__ = '1.0'

import random
import math
import sys
from v2.abm.sc_genetics import Chromosome


# TODO: Add diseases!
class Agent:
    def __init__(self, x, y, c_size, su, sp, genomes, a, tribe):
        """
        Initializes an agent
        """
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.size = c_size
        self.sugar = su
        self.spice = sp
        self.chromosome = Chromosome(genomes)
        self.init_sugar = self.chromosome.init_sugar
        self.init_spice = self.chromosome.init_spice
        self.meta_sugar = self.chromosome.meta_sugar
        self.meta_spice = self.chromosome.meta_spice
        self.vision = self.chromosome.vision
        self.gender = self.chromosome.gender
        self.fertility = self.chromosome.fertility
        self.dying_age = self.chromosome.dying_age
        self.culture = self.chromosome.culture
        self.age = a
        self.dead = False
        self.sugar_gathered = 0
        self.spice_gathered = 0
        self.sugar_traded = 0
        self.spice_traded = 0
        self.sugar_price = 0
        self.spice_price = 0
        self.children = []
        self.tribe_id = max(set(self.culture), key=self.culture.count)
        self.tribe = tribe

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
        :param su: amount of sugar that can be gained during this move.
        :param sp: amount of spice that can be gained during this move.
        :return: welfare value, important to calculate prices in the trading rule.
        """
        meta_total = self.meta_sugar + self.meta_spice
        w1 = math.pow((self.sugar + su), (self.meta_sugar / meta_total))
        w2 = math.pow((self.spice + sp), (self.meta_spice / meta_total))
        return w1 * w2

    def mrs(self, su, sp):
        """
        Second important trading tool, after welfare. MRS is used to calculate sugar and spice prices on the market.
        :param su:
        :param sp:
        :return:
        """
        rate_sugar = (self.sugar + su) / self.meta_sugar
        rate_spice = (self.spice + sp) / self.meta_spice
        if rate_sugar > 0:
            return rate_spice / rate_sugar
        else:
            return sys.maxsize

    def r1_select_best_cell(self, cells):
        """
        Agent selects the best cell to move to, according to: its resources, occupier and tribal alignment.
        :param cells: A list of all cells+occupiers in my range of sight.
        """
        grid_x = int(self.x / self.size)
        grid_y = int(self.y / self.size)
        available_cells = []
        # At first filter out all cells we can possibly move to.
        while len(cells) > 0:
            c = cells.pop()
            # Case 1: Cell is occupied.
            if c[1]:
                # Case 1a: Cell is my own.
                if c[1].x == self.x and c[1].y == self.y:
                    # Remove me from the (cell, agent) tuple. I don't want to kill myself.
                    available_cells.append((c[0], None))
                # Case 1b: Cell has an opponent who is poorer than me.
                elif c[1].tribe_id != self.tribe_id and c[1].gender == self.gender and\
                        (c[1].sugar + c[1].spice) < (self.sugar + self.spice):
                    available_cells.append(c)
            # Case 2: Cell is not occupied
            else:
                # Case 2a: Cell belongs to no one.
                if c[0].tribe_id == -1:
                    available_cells.append(c)
                # Case 2b: Cell belongs to my tribe.
                elif c[0].tribe_id == self.tribe_id:
                    available_cells.append(c)
                # Case 2c: Cell belongs to opposing tribe.
                elif self.tribe.can_conquer(c[0].tribe_id):
                    available_cells.append(c)

        # Secondly, find the field with highest reward. That basically means: maximize the welfare function!
        best_cells = []
        while len(available_cells) > 0:
            c = available_cells.pop()
            # Retrieve resources of possible occupants.
            occupant_sugar = 0
            occupant_spice = 0
            if c[1]:
                occupant_sugar = c[1].sugar
                occupant_spice = c[1].spice

            # Case: haven't found any cell so far.
            if not best_cells:
                best_cells = [c]
                max_w = self.welfare(c[0].sugar + occupant_sugar, c[0].spice + occupant_spice)
                max_dist = (abs(c[0].x - grid_x) + abs(c[0].y - grid_y))
            else:
                dist = (abs(c[0].x - grid_x) + abs(c[0].y - grid_y))
                welfare = self.welfare(c[0].sugar + occupant_sugar, c[0].spice + occupant_spice)
                if welfare > max_w:
                    best_cells = [c]
                    max_w = welfare
                elif welfare == max_w and dist < max_dist:
                    best_cells = [c]
                elif welfare == max_w and dist == max_dist:
                    best_cells.append(c)

        # Finally, pick one of the best cells (if there are multiple)
        # and set it as new position for this agent
        c = random.choice(best_cells)
        # Claim cell for our tribe, if we can afford it.
        if self.tribe.can_defend(self.tribe_id):
            self.tribe.tribal_area[self.tribe_id] += 1
            self.tribe.tribal_area[c[0].tribe_id] -= 1
            c[0].tribe_id = self.tribe_id

        # Save my current position...
        self.prev_x = self.x
        self.prev_y = self.y
        # ... and move to the new one.
        self.x = (c[0].x * self.size) + int(self.size / 2)
        self.y = (c[0].y * self.size) + int(self.size / 2)
        # Increase the cell's visit counter. This is only important for
        # the heat map visualization option.
        c[0].visits += 1
        # Additionally, try to eat from it and kill possible occupants.
        self.eat_from_cell(c)

    def eat_from_cell(self, cell):
        """
        Take all resources from cell, then claim it, if possible.
        Furthermore metabolise and update tribal statistics.
        :param cell: A tuple of cell and possible occupant
        """
        old_wealth = self.sugar + self.spice
        occupant_sugar = 0
        occupant_spice = 0
        # If there happens to be an occupant, kill him/her.
        if cell[1]:
            occupant_sugar = cell[1].sugar
            occupant_spice = cell[1].spice
            cell[1].sugar = 0
            cell[1].spice = 0
            cell[1].dead = True
        # Grab all the resources from the cell.
        self.sugar += cell[0].sugar + occupant_sugar
        self.spice += cell[0].spice + occupant_spice
        self.sugar_gathered += cell[0].sugar + occupant_sugar
        self.spice_gathered += cell[0].spice + occupant_spice
        cell[0].sugar = 0
        cell[0].spice = 0
        # Metabolise resources.
        self.sugar -= self.meta_sugar
        self.spice -= self.meta_spice
        new_wealth = self.sugar + self.spice
        # Update wealth count of my tribe.
        self.tribe.tribal_wealth[self.tribe_id] += (old_wealth - new_wealth)
        if self.sugar <= 0 or self.spice <= 0:
            self.dead = True

    def r2_reproduce(self, neighbors, agent_positions):
        """
        Look out for possible mates and procreate!
        :param neighbors: All neighbors around the agents' cell and their occupants.
        :param agent_positions: Dictionary of all agent positions. Use this to place possible children.
        """
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
                # All criteria is fulfilled to procreate!
                if free_cells and m.is_fertile() and m.gender != self.gender and both_wealthy1 and both_wealthy2:
                    print("Creating offspring...")
                    # Take one free cell to place Junior there.
                    c = random.choice(free_cells)
                    n_x = (c.x * self.size) + int(self.size / 2)
                    n_y = (c.y * self.size) + int(self.size / 2)
                    n_s = self.size
                    # Give him / her initial resources
                    n_su = int(self.init_sugar / 2) + int(m.init_sugar / 2)
                    n_sp = int(self.init_spice / 2) + int(m.init_spice / 2)
                    self.sugar -= int(self.init_sugar / 2)
                    self.spice -= int(self.init_spice / 2)
                    m.sugar -= int(m.init_sugar / 2)
                    m.spice -= int(m.init_spice / 2)
                    # Fuse mommy's and daddy's chromosomes to create Juniors attributes.
                    # This is the actual creation of the baby. Behold the wonders of nature!
                    n_chromosome = self.chromosome.merge_with(m.chromosome)
                    child = Agent(n_x, n_y, n_s, n_su, n_sp, n_chromosome, 0, self.tribe)
                    # Give the parents a reference to their newborn so they can,
                    # inherit their wealth to it before their inevitable demise.
                    self.children.append(child)
                    m.children.append(child)
                    # Update the abm that it has to schedule a new agent.
                    agent_positions[n_x, n_y] = child

    def r3_culture(self, neighbors):
        """
        Attempt to convert neighboring agents towards my culture.
        """
        for n in neighbors:
            if n[1] and n[1].tribe_id != self.tribe_id:
                index = 0
                while n[1].culture[index] == self.tribe_id:
                    index = random.choice(range(len(self.culture)))
                n[1].culture[index] = self.tribe_id
                old_id = n[1].tribe_id
                n[1].tribe_id = max(set(self.culture), key=self.culture.count)
                # In case the neighbor has been won over to my tribe,
                # shift its wealth over.
                if old_id != n[1].tribe_id:
                    wealth = n[1].sugar + n[1].spice
                    n[1].tribe.tribal_wealth[old_id] -= wealth
                    n[1].tribe.tribal_wealth[n[1].tribe_id] += wealth

    def r4_trading(self, neighbors):
        """
        Trade with neighboring agents if possible.
        """
        sugar_count = 0
        spice_count = 0
        self.sugar_price = 0
        self.spice_price = 0
        for n in neighbors:
            if n[1] and not self.dead and not n[1].dead:
                w1 = self.mrs(0, 0)
                w2 = n[1].mrs(0, 0)
                if w1 < w2:
                    p = math.sqrt(w1 * w2)
                    # trade 1 unit of sugar for p units of spice, obey the constraints
                    if 1 <= p < n[1].spice and self.sugar > 1 and n[1].spice > p \
                            and self.mrs(-1, p) < n[1].mrs(1, -p):
                        self.sugar -= 1
                        self.spice += p
                        n[1].sugar += 1
                        n[1].spice -= p
                        self.sugar_traded += 1
                        self.spice_traded += p
                    elif 0 < p < 1 and self.sugar > int(1 / p) and n[1].spice > 1 \
                            and self.mrs(- int(1 / p), 1) < n[1].mrs(int(1 / p), -1):
                        self.sugar -= int(1 / p)
                        self.spice += 1
                        n[1].sugar += int(1 / p)
                        n[1].spice -= 1
                        self.sugar_traded += int(1 / p)
                        self.spice_traded += 1
                    #self.sugar_price += 1 / p
                    self.spice_price += 1
                    spice_count += 1

                if w1 > w2:
                    p = math.sqrt(w1 * w2)
                    # trade 1 unit of sugar for p units of spice, obey the constraints
                    if 1 <= p < self.spice and n[1].sugar > 1 and self.spice > p \
                            and self.mrs(-1, p) < n[1].mrs(1, -p):
                        n[1].sugar -= 1
                        n[1].spice += p
                        self.sugar += 1
                        self.spice -= p
                        self.sugar_traded += 1
                        self.spice_traded += p
                    elif p < 1 and n[1].sugar > int(1 / p) and self.spice > 1 \
                            and n[1].mrs(- int(1 / p), 1) < self.mrs(int(1 / p), -1):
                        n[1].sugar -= int(1 / p)
                        n[1].spice += 1
                        self.sugar += int(1 / p)
                        self.spice -= 1
                        self.sugar_traded += int(1 / p)
                        self.spice_traded += 1
                    self.sugar_price += p
                    sugar_count += 1
                    #self.spice_price += 1 / p
        if sugar_count > 0:
            self.sugar_price /= sugar_count
        if spice_count > 0:
            self.spice_price /= spice_count

    def on_death(self):
        """
        As the name suggests, this method is to be executed upon the agent's death.
        """
        # Inherit my wealth to all my kids
        if self.children:
            num_kids = len(self.children)
            for c in self.children:
                c.sugar += math.floor(self.sugar / num_kids)
                c.spice += math.floor(self.spice / num_kids)

        # Update tribe's information
        self.tribe.tribal_wealth[self.tribe_id] -= (self.sugar + self.spice)
        self.sugar = 0
        self.spice = 0

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
            nb = ca.get_neighborhood(agent_positions, self.x, self.y)
            #vc = ca.get_visible_cells(agent_positions, self.x, self.y, self.vision)
            self.r2_reproduce(nb, agent_positions)
            self.r3_culture(nb)  # vc
            self.r4_trading(nb)  # vc
            self.chromosome.mutate()