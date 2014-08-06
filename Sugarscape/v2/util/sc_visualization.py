__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame


class Visualization:
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, surface):
        """
        Initializes the visualization and passes the surface on which to draw.
        :param surface: Pygame surface object.
        :return: nothing
        """
        # TODO: add different display modes to choose from.
        self.surface = surface

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
        col = self.calculate_cell_color(cell)
        col2 = (col[0] * 0.9, col[1] * 0.9, col[2] * 0.9)
        pygame.draw.rect(self.surface, col, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        lx = cell.x * cell.w
        ly = cell.y * cell.h
        w1 = cell.w - 1
        h1 = cell.h - 1
        pygame.draw.line(cell.surface, col2, [lx + 1, ly + w1], [lx + h1, ly + w1], int(cell.w * 0.2))
        pygame.draw.line(cell.surface, col2, [lx + h1, ly + 1], [lx + h1, ly + w1], int(cell.w * 0.2))

        if cell.tribe == 0:
            pygame.draw.line(cell.surface, (0, 0, 0), [lx, ly], [lx + cell.h, ly + cell.w], 2)
            pygame.draw.line(cell.surface, (0, 0, 0), [lx + cell.h, ly], [lx, ly + cell.w], 2)
        elif cell.tribe == 1:
            pygame.draw.line(cell.surface, (255, 255, 255), [lx, ly], [lx + cell.h, ly + cell.w], 2)
            pygame.draw.line(cell.surface, (255, 255, 255), [lx + cell.h, ly], [lx, ly + cell.w], 2)
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