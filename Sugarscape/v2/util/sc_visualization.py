__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame


class Visualization:
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, surface, gc):
        """
        Initializes the visualization and passes the surface on which to draw.
        :param surface: Pygame surface object.
        """
        self.surface = surface
        # 0 = tribe, 1 = gender, 2 = age
        self.draw_agent_mode = 0
        # 0 = resources+tribes, 1 = only tribes, 2 = heat map
        self.draw_cell_mode = 0
        self.gc = gc

    def draw_agent(self, agent):
        """
        Draw agent with 1) age, 2) gender, 3) tribe or something else.
        :param agent:
        """
        radius = int(agent.size / 2)
        if not agent.dead:
            if self.draw_agent_mode == 0:
            # Show tribe and age of the agents.
                if agent.age < agent.fertility[0]:  # Case 1: agent is a child.
                    red = 0
                    green = 200
                    blue = 0
                elif agent.fertility[0] <= agent.age <= agent.fertility[1]:  # Case 2: agent is adult.
                    if agent.gender == 0:  # A man.
                        red = 0
                        green = 0
                        blue = 255
                    else:  # A woman.
                        red = 255
                        green = 0
                        blue = 0
                else:  # Case 3: agent is old.
                    red = 90
                    green = 90
                    blue = 90
                color1 = (red, green, blue)
                color2 = self.gc.TRIBE_COLORS[agent.tribe_id]
                pygame.draw.circle(self.surface, color1, [agent.x, agent.y], radius, 0)
                pygame.draw.circle(self.surface, color2, [agent.x, agent.y], radius - 2, 0)
            elif self.draw_agent_mode == 1:
            # Show gender and age of the agents.
                # Case 1: agent is a child.
                if agent.age < agent.fertility[0]:
                    red = 90
                    green = 255
                    blue = 90
                # Case 2: agent is adult, display its gender.
                elif agent.fertility[0] <= agent.age <= agent.fertility[1]:
                    if agent.gender == 0:  # A man.
                        red = 0
                        green = 0
                        blue = 255
                    else:  # A woman.
                        red = 255
                        green = 0
                        blue = 0
                # Case 3: agent is old.
                else:
                    red = 160
                    green = 160
                    blue = 160
                color = (red, green, blue)
                pygame.draw.circle(self.surface, color, [agent.x, agent.y], radius, 0)
            elif self.draw_agent_mode == 2:
            # Show only tribe of the agents.
                color = self.gc.TRIBE_COLORS[agent.tribe_id]
                pygame.draw.circle(self.surface, color, [agent.x, agent.y], radius, 0)
        return

    def draw_cell(self, cell):
        """
        Draw cell with
        :param cell:
        :return:
        """
        if self.draw_cell_mode == 0:
            # Show resources and tribal territory.
            col = self.calculate_cell_color(cell)
            col2 = (col[0] * 0.9, col[1] * 0.9, col[2] * 0.9)
            pygame.draw.rect(self.surface, col, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
            lx = cell.x * cell.w
            ly = cell.y * cell.h
            w1 = cell.w - 1
            h1 = cell.h - 1
            pygame.draw.line(self.surface, col2, [lx + 1, ly + w1], [lx + h1, ly + w1], int(cell.w * 0.2))
            pygame.draw.line(self.surface, col2, [lx + h1, ly + 1], [lx + h1, ly + w1], int(cell.w * 0.2))

        elif self.draw_cell_mode == 1:
            # Show only tribal territories.
            if cell.tribe_id != -1:
                color = self.gc.TRIBE_COLORS[cell.tribe_id]
                pygame.draw.rect(self.surface, color, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
            else:
                color = (80, 80, 80)
                pygame.draw.rect(self.surface, color, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)

        elif self.draw_cell_mode == 2:
        # Show a heat map indicating which cells are the most visited.
            color = self.calculate_density_color(cell)
            pygame.draw.rect(self.surface, color, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        return

    def calculate_cell_color(self, cell):
        if cell.max_sugar == 0:
            normalized_su = 0
        else:
            normalized_su = cell.sugar / self.gc.MAX_SUGAR
        if cell.max_spice == 0:
            normalized_sp = 0
        else:
            normalized_sp = cell.spice / self.gc.MAX_SUGAR

        red = 150 * normalized_sp
        green = 200 * normalized_su
        blue = 0
        return red, green, blue

    def calculate_density_color(self, cell):
        """
        Calculates the RGB values depending on the cell's current temperature.
        :return:
        """
        if self.gc.TICKS == 0:
            normalized_v = 0
        else:
            normalized_v = cell.visits / self.gc.TICKS
        red = 0
        green = 0
        blue = 0
        if 0 <= normalized_v <= 1 / 8:
            red = 0
            green = 0
            blue = 4 * normalized_v + 0.5
        elif 1 / 8 < normalized_v <= 3 / 8:
            red = 0
            green = 4 * normalized_v - 0.5
            blue = 1
        elif 3 / 8 < normalized_v <= 5 / 8:
            red = 4 * normalized_v - 1.5
            green = 1
            blue = -4 * normalized_v + 2.5
        elif 5 / 8 < normalized_v <= 7 / 8:
            red = 1
            green = -4 * normalized_v + 3.5
            blue = 0
        elif 7 / 8 < normalized_v <= 1:
            red = -4 * normalized_v + 4.5
            green = 0
            blue = 0
        else:
            pass

        return red * 255, green * 255, blue * 255