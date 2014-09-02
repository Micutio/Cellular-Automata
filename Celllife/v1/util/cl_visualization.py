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
        # TODO: Comment what the modes do, for better overview.
        self.surface = surface
        self.draw_agent_mode = 1
        self.draw_cell_mode = 1
        self.gc = gc

    def draw_agent(self, agent):
        """
        Draw agent as a simple red circle
        :param agent:
        """
        radius = int(agent.size / 3)
        if not agent.dead:
            if agent.type == "chloroplast":
                color1 = (0, 255, 0)
            else:
                color1 = (1, 1, 1)
            pygame.draw.circle(self.surface, color1, [agent.x, agent.y], radius, 0)
        return

    def draw_cell(self, cell):
        """
        Draw cell in following colors:
        a) Red indicates the amount of glucose in relation to the current maximum in the world.
        b) Green indicates the amount of o2 in relation to the current maximum in the world.
        c) Blue indicates the amount of h2o in relation to the current maximum in the world.
        :param cell:
        :return:
        """
        cell_total = cell.h2o + cell.o2 + cell.glucose
        if cell_total == 0:
            red = green = blue = 0
        else:
            red = 255 * (max(cell.glucose, cell.o2) / cell_total)
            green = 255 * (cell.o2 / cell_total)
            blue = 255 * (cell.h2o / cell_total)

        color1 = (red, green, blue)
        pygame.draw.rect(self.surface, color1, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)

        lx = cell.x * cell.w
        ly = cell.y * cell.h
        w1 = cell.w - 1
        h1 = cell.h - 1
        color2 = (color1[0] * 0.9, color1[1] * 0.9, color1[2] * 0.9)
        if red > blue and red > green:
            pygame.draw.line(self.surface, color2, [lx + 1, ly + w1], [lx + h1, ly + w1], int(cell.w * 0.2))
            pygame.draw.line(self.surface, color2, [lx + h1, ly + 1], [lx + h1, ly + w1], int(cell.w * 0.2))
        elif blue > red and blue > green:
            pygame.draw.line(self.surface, color2, [lx + 1, ly + 1], [lx + 1, ly + w1], int(cell.w * 0.2))
            pygame.draw.line(self.surface, color2, [lx + 1, ly + 1], [lx + h1, ly + 1], int(cell.w * 0.2))
        return