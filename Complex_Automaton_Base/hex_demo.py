"""
Main module of the Flow and Pressure Demo.
Uses the Complex Automaton Base.
"""
from ca.cab_cell import CellHex
from cab_global_constants import GlobalConstants
from cab_system import ComplexAutomaton
from util.cab_input_handling import InputHandler
from util.cab_visualization import Visualization

import pygame
import numpy
import math

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
        self.USE_CA_BORDERS = True
        self.DIM_X = 50  # How many cells is the ca wide?
        self.DIM_Y = 50  # How many cells is the ca high?
        self.CELL_SIZE = 10  # How long/wide is one cell?
        self.GRID_WIDTH = self.DIM_X * self.CELL_SIZE
        self.GRID_HEIGHT = self.DIM_Y * self.CELL_SIZE
        ################################
        #        ABM CONSTANTS         #
        ################################
        ################################
        #      UTILITY CONSTANTS       #
        ################################


class FlowCell(CellHex):
    def __init__(self, x, y, c_size, c):
        super().__init__(x, y, c_size, c)
        self.pressure = 10
        self.new_pressure = 10
        self.flow = 1
        self.has_color = False
        self.next_color = False
        self.is_solid = False

    def sense_neighborhood(self):
        _pressure = 0
        _neighs = 0
        for cell in self.neighbors:
            if not (cell.is_solid or cell.is_border):
                _pressure += cell.pressure
                _neighs += 1
        if _neighs > 0:
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

    def get_mouse_hex_coords(self):
        _q = (self.mx * math.sqrt(3)/3 - self.my/3)# / self.sys.gc.CELL_SIZE
        _r = self.my * 2/3# / self.sys.gc.CELL_SIZE
        cell_q, cell_r = hex_round(_q, _r)
        return cell_q, cell_r

    # def custom_mouse_motion(self):
    #     '''
    #     Converts mouse cursor position from pixel to hex
    #     and colors the cell it currently hovers.
    #     '''
    #     _q = (self.mx * math.sqrt(3)/3 - self.my/3)# / self.sys.gc.CELL_SIZE
    #     _r = self.my * 2/3# / self.sys.gc.CELL_SIZE
    #     cell_q, cell_r = hex_round(_q, _r)
    #     # print('raw coordinates: ({0}, {1})'.format(_q, _r))
    #     # print('cell coordinates: ({0}, {1})'.format(cell_q, cell_r))
    #     if (cell_q, cell_r) in self.sys.ca.ca_grid:
    #         self.sys.visualizer.highlight(self.sys.ca.ca_grid[cell_q, cell_r])


    def custom_mouse_action(self, button):
        # Click on left mouse button.
        if button == 1:
            cell_x, cell_y = self.get_mouse_hex_coords()
            self.sys.ca.ca_grid[cell_x, cell_y].pressure = 500000
            #self.sys.ca.ca_grid[cell_x, cell_y].new_pressure = 10000

        elif button == 2:
            cell_x, cell_y = self.get_mouse_hex_coords()
            self.sys.ca.ca_grid[cell_x, cell_y].pressure = -500000
            #self.sys.ca.ca_grid[cell_x, cell_y].new_pressure = 10000

        # Click on right mouse button
        elif button == 3:
            cell_x, cell_y = self.get_mouse_hex_coords()
            self.sys.ca.ca_grid[cell_x, cell_y].is_solid = not self.sys.ca.ca_grid[cell_x, cell_y].is_solid
            #self.sys.ca.ca_grid[cell_x, cell_y].pressure = -100
            #print(self.sys.ca.ca_grid[cell_x, cell_y].pressure)


class FlowVis(Visualization):
    def __init__(self, c, screen):
        super().__init__(c, screen)

    def clone(self, cab_sys):
        return FlowVis(self.gc, cab_sys)

    # def draw_cell(self, cell):
    #     """
    #     Simple exemplary visualization. Draw cell in white.
    #     """
    #     if cell is None:
    #         pass
    #     else:
    #         crnrs = cell.get_corners()
    #         # pygame.draw.aalines(self.surface, (255, 255, 255), True, crnrs, 0)
    #         # pygame.gfxdraw.filled_polygon(self.surface, crnrs, (0, 0, 0))
    #         pygame.gfxdraw.aapolygon(self.surface, crnrs, (120, 0, 0))

    def draw_cell(self, cell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        if cell is None:
            pass
        else:
            if cell.is_solid:
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (255, 0, 0))
            elif cell.is_border:
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (150, 190, 100))
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
                pygame.gfxdraw.filled_polygon(self.surface, cell.get_corners(), (red, green, blue))
                pygame.gfxdraw.aapolygon(self.surface, cell.get_corners(), (255, 255, 255))

    def highlight(self, cell):
        """
        Simple exemplary visualization. Draw cell in white.
        """
        counter = 0
        for neigh in cell.neighbors:
            counter += 1
            crnrs = neigh.get_corners()
            # pygame.draw.aalines(self.surface, (255, 255, 255), True, crnrs, 0)
            # pygame.gfxdraw.filled_polygon(self.surface, crnrs, (0, 0, 0))
            pygame.gfxdraw.filled_polygon(self.surface, crnrs, (255, 255, 0))
        crnrs = cell.get_corners()
        pygame.gfxdraw.filled_polygon(self.surface, crnrs, (60, 200, 0))


def hex_round(q, r):
    return cube_to_hex(*cube_round(*hex_to_cube(q, r)))

def cube_round(x, y, z):
    rx = round(x)
    ry = round(y)
    rz = round(z)
    dx = abs(rx - x)
    dy = abs(ry - y)
    dz = abs(rz - z)

    if dx > dy and dx > dz:
        rx = -ry - rz
    elif dy > dz:
        ry = -rx - rz
    else:
        rz = -rx - ry

    return rx, ry, rz

def cube_to_hex(x, y, z):
    return x, y

def hex_to_cube(q, r):
    z = -q - r
    return q, r, z



if __name__ == '__main__':
    gc = GC()
    pc = FlowCell(0, 0, 0, gc)
    ph = FlowIO(None)
    pv = FlowVis(gc, None)
    simulation = ComplexAutomaton(gc, proto_cell=pc, proto_handler=ph, proto_visualizer=pv)
    simulation.run_main_loop()
    # cProfile.run("simulation.run_main_loop()")