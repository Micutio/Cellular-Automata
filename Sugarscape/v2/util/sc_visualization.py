__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import matplotlib.pyplot as plt


class Visualization:
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, surface):
        """
        Initializes the visualization and passes the surface on which to draw.
        :param surface: Pygame surface object.
        """
        # TODO: add different display modes to choose from.
        self.surface = surface
        # 0 = tribe, 1 = gender, 3 = age
        self.draw_agent_mode = 0
        self.tribe_colors = {0: (0, 0, 0),
                             1: (1, 1, 1),
                             2: (0.7, 0, 0.5),
                             3: (0, 0.7, 0.5),
                             4: (0.7, 0.9, 0.2),
                             5: (0.6, 0.4, 0.1)}
        # 0 = resources+tribes, 1 = only tribes, 2 = heat map
        self.draw_cell_mode = 0
        self.ticks = 0

    def update(self):
        self.ticks += 1

    def draw_agent(self, agent):
        """
        Draw agent with 1) age, 2) gender, 3) tribe or something else.
        :param agent:
        """
        radius = int(agent.size / 2)
        if not agent.dead:
            col = self.get_agent_color(agent)
            pygame.draw.circle(self.surface, col[0], [agent.x, agent.y], radius, 0)
            pygame.draw.circle(self.surface, col[1], [agent.x, agent.y], radius - 2, 0)
        else:
            pygame.draw.circle(self.surface, (0, 0, 0), [agent.x, agent.y], radius, 0)
        return

    def get_agent_color(self, agent):
        # First color: the ring
        r0 = g0 = b0 = 0
        if agent.is_fertile():
            ratio = 1 - (agent.age / agent.dying_age)
            if agent.gender == "m":
                b0 = 255 * ratio
            else:
                r0 = 255 * ratio
        elif agent.age > agent.fertility[1]:
            r0 = g0 = b0 = 80
        elif agent.age < agent.fertility[0]:
            r0 = g0 = 150
            b0 = 0
        # Second color: the inner circle
        if agent.culture.count(0) > agent.culture.count(1):
            r1 = g1 = b1 = 0
        else:
            r1 = g1 = b1 = 255
        return [(r0, g0, b0), (r1, g1, b1)]

    def draw_cell(self, cell):
        """
        Draw cell with
        :param cell:
        :return:
        """

        if self.draw_cell_mode == 0:
            col = self.calculate_cell_color(cell)
            col2 = (col[0] * 0.9, col[1] * 0.9, col[2] * 0.9)
            pygame.draw.rect(self.surface, col, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
            lx = cell.x * cell.w
            ly = cell.y * cell.h
            w1 = cell.w - 1
            h1 = cell.h - 1
            pygame.draw.line(cell.surface, col2, [lx + 1, ly + w1], [lx + h1, ly + w1], int(cell.w * 0.2))
            pygame.draw.line(cell.surface, col2, [lx + h1, ly + 1], [lx + h1, ly + w1], int(cell.w * 0.2))

            tribe = self.tribe_colors[cell.tribe_id]
            color = (255 * tribe[0], 255 * tribe[1], 255 * tribe[2])
            pygame.draw.line(cell.surface, color, [lx, ly], [lx + cell.h, ly + cell.w], 2)
            pygame.draw.line(cell.surface, color, [lx + cell.h, ly], [lx, ly + cell.w], 2)

        elif self.draw_cell_mode == 1:
            tribe = self.tribe_colors[cell.tribe_id]
            color = (255 * tribe[0], 255 * tribe[1], 255 * tribe[2])
            color2 = (color[0] * 0.9, color[1] * 0.9, color[2] * 0.9)
            pygame.draw.rect(self.surface, color, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
            lx = cell.x * cell.w
            ly = cell.y * cell.h
            w1 = cell.w - 1
            h1 = cell.h - 1
            pygame.draw.line(cell.surface, color2, [lx + 1, ly + w1], [lx + h1, ly + w1], int(cell.w * 0.2))
            pygame.draw.line(cell.surface, color2, [lx + h1, ly + 1], [lx + h1, ly + w1], int(cell.w * 0.2))

        elif self.draw_cell_mode == 2:
            col_map = plt.get_cmap("jet")
            color = col_map(cell.visits / self.ticks)
            pygame.draw.rect(self.surface, color, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        return

    def calculate_cell_color(self, cell):
        if cell.max_sugar == 0:
            normalized_su = 0
        else:
            normalized_su = cell.sugar / cell.max_sugar
        if cell.max_spice == 0:
            normalized_sp = 0
        else:
            normalized_sp = cell.spice / cell.max_sugar

        green = 200 * normalized_su
        red = 150 * normalized_sp
        blue = 0
        return red, green, blue