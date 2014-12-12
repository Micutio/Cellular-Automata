"""
Main module of the Flow and Pressure Demo.
Uses the Complex Automaton Base.
"""
from ca.cab_cell import CACell
from cab_global_constants import GlobalConstants
from cab_system import ComplexAutomaton
from util.cab_input_handling import InputHandler
from util.cab_visualization import Visualization

import pygame
import cProfile

__author__ = 'Michael Wagner'


class GC(GlobalConstants):
    def __init__(self):
        super().__init__()
        self.VERSION = 'version: 09-2014'
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        self.ONE_AGENT_PER_CELL = False
        ################################
        #         CA CONSTANTS         #
        ################################
        self.USE_MOORE_NEIGHBORHOOD = True
        self.USE_CA_BORDERS = False
        self.DIM_X = 5  # How many cells is the ca wide?
        self.DIM_Y = 10  # How many cells is the ca high?
        self.CELL_SIZE = 50  # How long/wide is one cell?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        ################################
        #        ABM CONSTANTS         #
        ################################
        ################################
        #      UTILITY CONSTANTS       #
        ################################


class FlowCell(CACell):
    def __init__(self, x, y, c_size, c):
        super().__init__(x, y, c_size, c)
        self.light = 0
        self.new_light = 0
        self.nutrition = 0
        self.new_nutrition = 0
        self.is_solid = False

    def sense_neighborhood(self):
        if not self.is_solid:
            for cell in self.neighbors:
                if cell.x == self.x:
                    if cell.y < self.y:
                        self.new_light = cell.light * 0.8
                    elif cell.y > self.y:
                        self.new_nutrition = cell.nutrition * 0.8
        #self.flow += flow

    def update(self):
        if not self.is_solid:
            self.light = self.new_light
            self.nutrition = self.new_nutrition

    def clone(self, x, y, c_size):
        return FlowCell(x, y, c_size, self.gc)


class FlowIO(InputHandler):
    def __init__(self, cab_sys):
        super().__init__(cab_sys)

    def clone(self, cab_sys):
        return FlowIO(cab_sys)

    def custom_mouse_action(self, button):
        # Click on left mouse button.
        if button == 1:
            cell_x = int(self.mx)
            cell_y = int(self.my)
            if self.sys.ca.ca_grid[cell_x, cell_y].is_solid:
                self.sys.ca.ca_grid[cell_x, cell_y].light = 0.0
                self.sys.ca.ca_grid[cell_x, cell_y].is_solid = False
            else:
                self.sys.ca.ca_grid[cell_x, cell_y].light = 1.0
                self.sys.ca.ca_grid[cell_x, cell_y].is_solid = True

            #self.sys.ca.ca_grid[cell_x, cell_y].new_pressure = 10000

        elif button == 2:
            cell_x = int(self.mx)
            cell_y = int(self.my)
            self.sys.ca.ca_grid[cell_x, cell_y].pressure = -500000
            #self.sys.ca.ca_grid[cell_x, cell_y].new_pressure = 10000

        # Click on right mouse button
        elif button == 3:
            cell_x = int(self.mx)
            cell_y = int(self.my)
            if self.sys.ca.ca_grid[cell_x, cell_y].is_solid:
                self.sys.ca.ca_grid[cell_x, cell_y].nutrition = 0.0
                self.sys.ca.ca_grid[cell_x, cell_y].is_solid = False
            else:
                self.sys.ca.ca_grid[cell_x, cell_y].nutrition = 1.0
                self.sys.ca.ca_grid[cell_x, cell_y].is_solid = True


class FlowVis(Visualization):
    def __init__(self, c, screen):
        super().__init__(c, screen)

    def clone(self, cab_sys):
        return FlowVis(self.gc, cab_sys)

    def draw_cell(self, cell):
        red = green = int(cell.light * 255)
        blue = int(cell.nutrition * 255)
        pygame.draw.rect(self.surface, (red, green, blue), (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)

if __name__ == '__main__':
    gc = GC()
    pc = FlowCell(0, 0, 0, gc)
    ph = FlowIO(None)
    pv = FlowVis(gc, None)
    simulation = ComplexAutomaton(gc, proto_cell=pc, proto_handler=ph, proto_visualizer=pv)
    #simulation.run_main_loop()
    cProfile.run("simulation.run_main_loop()")