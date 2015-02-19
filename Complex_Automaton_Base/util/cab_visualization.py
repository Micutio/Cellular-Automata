"""
This module contains a simple visualization class, which the actual simulation visualizer should inherit from.
"""
__author__ = 'Michael Wagner'

import pygame
import pygame.gfxdraw


class Visualization:
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, gc, surface):
        """
        Initializes the visualization and passes the surface on which to draw.
        :param surface: Pygame surface object.
        """
        if surface is None:
            self.surface = None
        else:
            self.surface = surface
        self.gc = gc

    def clone(self, surface):
        return Visualization(self.gc, surface)

    def draw_agent(self, agent):
        """
        Simple exemplary visualization. Draw agent as a black circle
        """
        if not agent.dead:
            radius = int(agent.size / 2)
            pygame.draw.circle(self.surface, (0, 0, 0), [agent.x, agent.y], radius, 0)

    def draw_cell(self, cell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        if cell is None:
            pass
        elif cell.rectangular:
            pygame.draw.rect(self.surface, (255, 255, 255), (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        else:
            crnrs = cell.get_corners()
            pygame.draw.polygon(self.surface, (255, 255, 255), crnrs, 1)
            pygame.gfxdraw.aacircle(self.surface, 50, 50, 10 + 10, (0,255,0))
            pygame.gfxdraw.filled_circle(self.surface, 50, 50, 10, (0,255,0))
            pygame.gfxdraw.aacircle(self.surface, 50, 50, 10 - 2, (0,0,0))
            pygame.gfxdraw.filled_circle(self.surface, 50, 50, 10 - 2, (0,0,0))
            # print(crnrs)
            # pygame.draw.aalines(self.surface, (255, 255, 255), True, crnrs, 0)
            # pygame.gfxdraw.aapolygon(self.surface, crnrs, (255, 255, 255))