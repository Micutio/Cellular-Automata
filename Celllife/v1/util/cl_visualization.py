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
        if not agent.dead and agent.x >= 0 and agent.y >= 0:
            radius = int(agent.size / 2)
            x = int((agent.x * self.gc.CELL_SIZE) + (self.gc.CELL_SIZE / 2))
            y = int((agent.y * self.gc.CELL_SIZE) + (self.gc.CELL_SIZE / 2))
            pygame.draw.circle(self.surface, (0, 0, 0), [x, y], radius, 0)
        return

    def draw_cell(self, cell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        pygame.draw.rect(self.surface, (255, 255, 255), (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        lx = cell.x * cell.w
        ly = cell.y * cell.h
        w1 = cell.w - 1
        h1 = cell.h - 1
        color2 = (100, 100, 100)
        pygame.draw.line(self.surface, color2, [lx + 1, ly + w1], [lx + h1, ly + w1], 1)
        pygame.draw.line(self.surface, color2, [lx + h1, ly + 1], [lx + h1, ly + w1], 1)
        return