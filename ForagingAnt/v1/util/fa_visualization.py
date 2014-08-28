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
        radius = int(agent.size / 2)
        if not agent.dead:
            color1 = (255, 0, 0)
            pygame.draw.circle(self.surface, color1, [agent.x, agent.y], radius, 0)
        return

    def draw_cell(self, cell):
        """
        Draw cell in following colors:
        a) Dark green if it is a hive.
        b) Yellow if it is food.
        c) According to pheromones there, if it is none of the above.
        :param cell:
        :return:
        """
        if cell.is_hive:
            color1 = (0, 0, 200)
        elif cell.food > 0:
            food_ratio = cell.food / self.gc.MAX_FOOD
            red = green = int(255 * food_ratio)
            color1 = (red, green, 0)
        else:
            green = int(255 * (cell.pheromones["hive"] / self.gc.MAX_PHEROMONE))
            blue = int(255 * (cell.pheromones["food"] / self.gc.MAX_PHEROMONE))
            red = int((green + blue) / 2)
            color1 = (red, green, blue)
        pygame.draw.rect(self.surface, color1, (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        return