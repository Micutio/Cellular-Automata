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
import numpy

__author__ = 'Michael Wagner'


class GC(GlobalConstants):
    def __init__(self):
        super().__init__()
        self.VERSION = "version: 09-2014"
        ################################
        #     SIMULATION CONSTANTS     #
        ################################
        self.RUN_SIMULATION = False
        ################################
        #         CA CONSTANTS         #
        ################################
        self.USE_MOORE_NEIGHBORHOOD = True
        self.USE_CA_BORDERS = False
        self.DIM_X = 50  # How many cells is the ca wide?
        self.DIM_Y = 50  # How many cells is the ca high?
        self.CELL_SIZE = 15  # How long/wide is one cell?
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
        self.pressure = 10
        self.new_pressure = 10
        self.flow = 1
        self.has_color = False
        self.next_color = False
        self.is_solid = False

    def sense_neighborhood(self, neighborhood):
        _pressure = 0
        _neighs = 0
        for cell in neighborhood:
            if not cell.is_solid:
                _pressure += cell.pressure
                _neighs += 1
        _pressure /= _neighs
        d_pressure = self.pressure - _pressure
        flow = self.flow * d_pressure
        a = self.pressure / 10.0
        b = -_pressure / 10.0
        if a < b:
            flow = float(numpy.clip(flow, a, b))
        else:
            flow = float(numpy.clip(flow, b, a))
        self.new_pressure -= flow
        #self.flow += flow

    def update(self):
        self.pressure = self.new_pressure

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
            self.sys.ca.ca_grid[cell_x, cell_y].pressure = 500000
            #self.sys.ca.ca_grid[cell_x, cell_y].new_pressure = 10000

        # Click on right mouse button
        elif button == 3:
            cell_x = int(self.mx)
            cell_y = int(self.my)
            self.sys.ca.ca_grid[cell_x, cell_y].is_solid = not self.sys.ca.ca_grid[cell_x, cell_y].is_solid
            #self.sys.ca.ca_grid[cell_x, cell_y].pressure = -100
            #print(self.sys.ca.ca_grid[cell_x, cell_y].pressure)


class FlowVis(Visualization):
    def __init__(self, c, screen):
        super().__init__(c, screen)

    def clone(self, cab_sys):
        return FlowVis(self.gc, cab_sys)

    def draw_cell(self, cell):
        if cell.is_solid:
            pygame.draw.rect(self.surface, (255, 0, 0), (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        else:
            if cell.pressure > 100:
                red = 255
                green = 255
                blue = 255
            elif cell.pressure < 0:
                red = 0
                green = 0
                blue = 0
            else:
                red = int((cell.pressure / 100) * 150)
                green = int((cell.pressure / 100) * 150)
                blue = int((cell.pressure / 100) * 255)
            pygame.draw.rect(self.surface, (red, green, blue), (cell.x * cell.w, cell.y * cell.h, cell.w, cell.h), 0)
        return

if __name__ == '__main__':
    gc = GC()
    pc = FlowCell(0, 0, 0, gc)
    ph = FlowIO(None)
    pv = FlowVis(gc, None)
    simulation = ComplexAutomaton(gc,
                                  proto_cell=pc,
                                  proto_agent=None,
                                  proto_handler=ph,
                                  proto_visualizer=pv)
    simulation.run_main_loop()