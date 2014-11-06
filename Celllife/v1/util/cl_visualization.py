__author__ = 'Michael Wagner'

import pygame
from cab_visualization import Visualization


class CellLifeVisualizer(Visualization):
    def __init__(self, gc, surface):
        super().__init__(gc, surface)

    def clone(self, surface):
        return CellLifeVisualizer(self.gc, surface)

    def draw_agent(self, agent):
        """
        Simple exemplary visualization. Draw agent as a black circle
        """
        if not agent.dead:
            radius = int(agent.size / 2)
            pygame.draw.circle(self.surface, (0, 0, 0), [agent.x, agent.y], radius, 0)
        return

    def draw_cell(self, cell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        pygame.draw.rect(self.surface, (255, 255, 255), (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        return