__author__ = 'Michael Wagner'
__version__ = '2.0'

import random
import math
import copy
from abm.sc_genetics import Chromosome


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
        self.diseases = {}
        self.immune_system = ["".join(map(str, self.chromosome.immune_system))]

    def is_fertile(self):
        return self.fertility[0] <= self.age <= self.fertility[1]

    def check_status(self, agent_positions):
        """
        Check whether I'm still healthy and stuff
        """
        # Check my resources and age.
        if not self.dead and (self.sugar <= 0 or self.spice <= 0 or self.age == self.dying_age):
            self.die(agent_positions)
        self.age += 1

    def welfare(self, su, sp):
        """
        Welfare function a.k.a. Cobb-Douglas form.
        Relates the time the agent will die of lack of sugar with
        the time the agent will die of lack of spice.
        :param su: potential sugar gain of cell in question.
        :param sp: potential spice gain of cell in question.
        :return: welfare value, important to calculate prices in the trading rule.
        """
        meta_total = self.meta_sugar + self.meta_spice
        w1 = math.pow((self.sugar + su), (self.meta_sugar / meta_total))
        w2 = math.pow((self.spice + sp), (self.meta_spice / meta_total))
        return w1 * w2

    def mrs(self, su, sp):
        """
        Marginal Rate of Substitution.
        Second important trading tool after welfare.
        MRS is used to calculate sugar and spice prices between two agents.
        :param su:
        :param sp:
        :return:
        """
        rate_sugar = (self.sugar + su) / self.meta_sugar
        rate_spice = (self.spice + sp) / self.meta_spice
        return rate_spice / rate_sugar

    def r1_select_best_cell(self, cells, agent_positions):
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
                    available_cells.append((c[0], False))
                # Case 1b: Cell has an opponent who is poorer than me and the same gender and we're both adults
                # Then I am allowed to kill the agent and take its cell
                elif (c[1].tribe_id != self.tribe_id) and (c[1].sugar + c[1].spice) < (self.sugar + self.spice)\
                        and c[1].gender == self.gender and c[1].fertility[0] < c[1].age < c[1].fertility[1]\
                        and self.fertility[0] < self.age < self.fertility[1]:
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
        max_dist = 0
        while len(available_cells) > 0:
            c = available_cells.pop()
            # Retrieve resources of possible neighbors occupying those cells.
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
                    max_dist = dist
                elif welfare == max_w and dist < max_dist:
                    best_cells = [c]
                    max_dist = dist
                elif welfare == max_w and dist == max_dist:
                    best_cells.append(c)

        # Finally, pick one of the best cells (if there are multiple)
        # and set it as new position for this agent
        c = random.choice(best_cells)
        # Claim cell for our tribe, if we can afford it.
        if c[0].tribe_id != self.tribe_id and self.tribe.can_defend(self.tribe_id):
            self.tribe.tribal_area[self.tribe_id] += 1
            self.tribe.tribal_area[c[0].tribe_id] -= 1
            c[0].tribe_id = self.tribe_id

        # Additionally, try to eat from it and kill possible occupants.
        self.eat_from_cell(c, agent_positions)

        # In case I don't stay on my cell: move
        if (c[0].x != self.x or c[0].y != self.y) and not self.dead:
            # Save my current position...
            self.prev_x = self.x
            self.prev_y = self.y
            # ... and move to the new one.
            self.x = (c[0].x * self.size) + int(self.size / 2)
            self.y = (c[0].y * self.size) + int(self.size / 2)
            # Also do not forget to update the agent position dictionary
            del(agent_positions[self.prev_x, self.prev_y])
            agent_positions[self.x, self.y] = self
        # Increase the cell's visit counter. This is only important for
        # the heat map visualization option.
        c[0].visits += 1

    def eat_from_cell(self, cell, agent_positions):
        """
        Take all resources from cell, then claim it, if possible.
        Furthermore metabolise and update tribal statistics.
        :param cell: A tuple of cell and possible occupant
        """
        old_wealth = self.sugar + self.spice
        occupant_sugar = 0
        occupant_spice = 0
        # If there happens to be an occupant, kill him/her.
        if cell[1] and (cell[1].x != self.x or cell[1].y != self.y):
            occupant_sugar = cell[1].sugar
            occupant_spice = cell[1].spice
            cell[1].sugar = 0
            cell[1].spice = 0
            cell[1].die(agent_positions)
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
            self.die(agent_positions)

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
                    return child

    def r3_culture(self, neighbors):
        """
        Attempt to convert neighboring agents towards my culture.
        """
        for n in neighbors:
            if n[1] and n[1].tribe_id != self.tribe_id:
                old_id = n[1].tribe_id
                genes_to_flip = [n[1].culture.index(g) for g in n[1].culture if g != self.tribe_id]
                if genes_to_flip:
                    index = random.choice(genes_to_flip)
                    n[1].chromosome.culture[index] = self.tribe_id
                    n[1].culture = n[1].chromosome.culture
                    n[1].tribe_id = max(set(n[1].culture), key=n[1].culture.count)
                else:
                    n[1].tribe_id = self.tribe_id
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
        trade_count = 0
        self.sugar_price = 0
        self.spice_price = 0
        for n in neighbors:
            if n[1] and not n[1].dead and not self.dead and n[1].sugar > 0 and n[1].spice > 0:
                m1_now = self.mrs(0, 0)
                m2_now = n[1].mrs(0, 0)
                mrs_diff = m1_now - m2_now
                while mrs_diff != 0:
                    # Calculate welfare.
                    w1_now = self.welfare(0, 0)
                    w2_now = n[1].welfare(0, 0)
                    # Set directions of traded resources
                    if mrs_diff < 0:
                        sugar_flow = -1
                        spice_flow = 1
                        direction = False
                    else:  # m1 < m2
                        sugar_flow = 1
                        spice_flow = -1
                        direction = True
                    # Calculate exchange price p as geometric mean.
                    price = math.sqrt(m1_now * m2_now)
                    if price > 1:  # Trade p units of spice for 1 sugar.
                        my_sugar_delta = int(sugar_flow * 1)
                        my_spice_delta = int(spice_flow * int(price))
                        neigh_sugar_delta = int(my_sugar_delta * -1)
                        neigh_spice_delta = int(my_spice_delta * -1)
                    else:  # p < 1, Trade 1/p units of sugar for 1 spice.
                        my_sugar_delta = int(sugar_flow * int(1 / price))
                        my_spice_delta = int(spice_flow * 1)
                        neigh_sugar_delta = int(my_sugar_delta * -1)
                        neigh_spice_delta = int(my_spice_delta * -1)
                    # Trade only if welfare of both agents increases.
                    # Trade only if neither agent loses resources.
                    my_trade_valid = self.sugar + my_sugar_delta > 0 and self.spice + my_spice_delta > 0
                    neigh_trade_valid = n[1].sugar + neigh_sugar_delta > 0 and n[1].spice + neigh_spice_delta > 0
                    if my_trade_valid and neigh_trade_valid:
                        w1_expected = self.welfare(my_sugar_delta, my_spice_delta)
                        w2_expected = n[1].welfare(neigh_sugar_delta, neigh_spice_delta)
                        if w1_expected > w1_now and w2_expected > w2_now:
                            # Trade only if mrs values of agents are not flipping.
                            # (If mrs flips, they would infinitely trade their goods back and forth.)
                            m1_expected = self.mrs(my_sugar_delta, my_spice_delta)
                            m2_expected = n[1].mrs(neigh_sugar_delta, neigh_spice_delta)
                            mrs_diff = m1_expected - m2_expected
                            if (mrs_diff > 0 and direction) or (mrs_diff < 0 and not direction):
                                self.sugar += my_sugar_delta
                                self.spice += my_spice_delta
                                n[1].sugar += neigh_sugar_delta
                                n[1].spice += neigh_spice_delta
                                # Gather information for the trading statistics.
                                # 1.) general trading stats
                                self.sugar_traded += abs(my_sugar_delta)
                                self.spice_traded += abs(my_spice_delta)
                                self.sugar_price += abs(price)
                                self.spice_price += abs(1 / price)
                                trade_count += 1
                                # 2.) wealth change between tribes, if occurred
                                if self.tribe_id != n[1].tribe_id:
                                    my_wealth_change = my_sugar_delta + my_spice_delta
                                    neigh_wealth_change = neigh_spice_delta + neigh_sugar_delta
                                    self.tribe.tribal_wealth[self.tribe_id] += my_wealth_change
                                    self.tribe.tribal_wealth[n[1].tribe_id] += neigh_wealth_change
                            else:
                                mrs_diff = 0
                        else:
                            mrs_diff = 0
                    else:
                        mrs_diff = 0
        # Finish up trading and save possibly gathered data.
        if trade_count > 0:
            self.sugar_price /= trade_count
            self.spice_price /= trade_count

    def r5_diseases(self, neighbors):
        """
        All diseases, the agent is currently infected with, are trying to spread to its neighbors.
        """
        for n in neighbors:
            if n[1] and not n[1].dead and not self.dead:
                for _, d in self.diseases.items():
                    d.spread(n[1])
        # Let the immune system build another instance
        # and then attempt to fight the diseases.
        self.im_create_antibodies()
        self.immune_reaction()
        # Reset the metabolism values of the agent to clear all past diseases.
        # That way, the diseases just fought off by the immune system are not longer
        # afflicting the body and possible new diseases can act on the agent.
        self.meta_sugar = self.chromosome.meta_sugar
        self.meta_spice = self.chromosome.meta_spice
        # Have the diseases affect the agent
        for _, d in self.diseases.items():
            d.affect(self)

    def im_create_antibodies(self):
        if self.fertility[0] < self.age < self.fertility[1] and len(self.immune_system) <= 10:
            is_copy = copy.deepcopy(self.chromosome.immune_system)
            length = len(is_copy)
            index = random.choice(range(length))
            is_copy[index] = 1 - is_copy[index]
            self.immune_system.append("".join(map(str, is_copy)))

    def immune_reaction(self):
        eliminated = set()
        for _, d in self.diseases.items():
            for i in self.immune_system:
                # If the immune system has one instance that fits
                # into the disease genome, the agent is now
                # successfully healed from it and immune to future infections.
                if i in d.genome_string:
                    eliminated.add(d.genome_string)
        # Remove all eliminated diseases from our agent dictionary
        for d in eliminated:
            del(self.diseases[d])

    def die(self, agent_positions):
        """
        As the name suggests, this method is to be executed upon the agent's death.
        """
        # Remove myself from the world
        del(agent_positions[self.x, self.y])
        self.dead = True
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
        self.check_status(agent_positions)
        if not self.dead:
            self.prev_x = self.x
            self.prev_y = self.y
            self.sugar_gathered = 0
            self.spice_gathered = 0
            self.sugar_traded = 0
            self.spice_traded = 0
            vc = ca.get_visible_cells(agent_positions, self.x, self.y, self.vision)
            self.r1_select_best_cell(vc, agent_positions)
            #self.r1_select_best_cell_w_pollution(vc)
            if not self.dead:
                nb = ca.get_neighborhood(agent_positions, self.x, self.y)
                #vc = ca.get_visible_cells(agent_positions, self.x, self.y, self.vision)
                offspring = self.r2_reproduce(nb, agent_positions)
                self.r3_culture(nb)  # vc
                self.r4_trading(nb)  # vc
                self.r5_diseases(nb)
                self.chromosome.mutate()
                return offspring