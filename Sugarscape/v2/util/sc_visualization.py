__author__ = 'Michael Wagner'
__version__ = '1.0'

import pygame
import matplotlib.cm as cm


class Visualization:
    """
    This class incorporates all methods necessary for visualizing the simulation.
    """

    def __init__(self, surface, gc):
        """
        Initializes the visualization and passes the surface on which to draw.
        :param surface: Pygame surface object.
        """
        # TODO: add different display modes to choose from.
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
                    red = int(128 * (1 - (agent.age / agent.fertility[0])))
                    green = 255
                    blue = int(128 * (1 - (agent.age / agent.fertility[0])))
                elif agent.fertility[0] <= agent.age <= agent.fertility[1]:  # Case 2: agent is adult.
                    red = 255
                    green = 255
                    blue = int(128 * (1 - (agent.age / agent.fertility[1])))
                else:  # Case 3: agent is old.
                    red = int(255 * (agent.age / agent.dying_age))
                    green = 0
                    blue = 0
                color1 = (red, green, blue)
                color2 = self.gc.TRIBE_COLORS[agent.tribe_id]
                pygame.draw.circle(self.surface, color1, [agent.x, agent.y], radius, 0)
                pygame.draw.circle(self.surface, color2, [agent.x, agent.y], radius - 2, 0)
            elif self.draw_agent_mode == 1:
            # Show gender and age of the agents.
                # Case 1: agent is a child.
                if agent.age < agent.fertility[0]:
                    red = int(128 * (1 - (agent.age / agent.fertility[0])))
                    green = 255
                    blue = int(128 * (1 - (agent.age / agent.fertility[0])))
                # Case 2: agent is adult, display its gender.
                elif agent.fertility[0] <= agent.age <= agent.fertility[1]:
                    ratio = (agent.age / agent.fertility[1])
                    if agent.gender == 0:  # A man.
                        red = 100 * ratio
                        green = 150 * ratio
                        blue = 255 * ratio
                    else:  # A woman.
                        red = 255 * ratio
                        green = 100 * ratio
                        blue = 180 * ratio
                # Case 3: agent is old.
                else:
                    red = int(255 * (agent.age / agent.dying_age))
                    green = 0
                    blue = 0
                color = (red, green, blue)
                pygame.draw.circle(self.surface, color, [agent.x, agent.y], radius, 0)
            elif self.draw_agent_mode == 2:
            # Show only tribe of the agents.
                color = self.gc.TRIBE_COLORS[agent.tribe_id]
                pygame.draw.circle(self.surface, color, [agent.x, agent.y], radius, 0)
        return

    def draw_cell(self, cell, max_visit):
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

            #if cell.tribe_id != -1:
            #    color = self.gc.TRIBE_COLORS[cell.tribe_id]
            #    pygame.draw.line(self.surface, color, [lx, ly], [lx + cell.h, ly + cell.w], 2)
            #    pygame.draw.line(self.surface, color, [lx + cell.h, ly], [lx, ly + cell.w], 2)

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
            j = cm.jet((cell.visits / self.gc.TICKS))#max_visit))
            color = (255 * j[0], 255 * j[1], 255 * j[2])
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