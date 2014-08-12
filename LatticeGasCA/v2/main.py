__author__ = 'Michael Wagner'
__version__ = '2.0'

# This is a python prototype for a complex automaton, which
# integrates a CA and ABM. The CA is supposed to simulate heat emission
# of an object passing through the CA grid.

# Original CA code taken from
# "http://pygame.org/project-Cellular+Automata-1286-.html"

#import time
import sys

from ca import *
import pygame
from pygame.locals import *

#########################################################################
###                       Global Variables                            ###
#########################################################################


class GlobalConstants:
    def __init__(self):
        self.run_ca = False
GC = GlobalConstants()

#########################################################################
###                            CLASSES                                ###
#########################################################################


class InputHandler:
    def __init__(self):
        self.mx = 0
        self.my = 0

    def process_in(self, ca, rule):
        for event in pygame.event.get():
            # The 'x' on the window is clicked
            if event.type == QUIT:
                sys.exit()

            # Mouse is moved
            elif event.type == MOUSEMOTION:
                self.mx, self.my = pygame.mouse.get_pos()
                self.mx = (self.mx / 10)
                self.my = (self.my / 10)

            # Mouse button is pressed
            elif event.type == pygame.MOUSEBUTTONUP:
                # Click on left mouse button, set temperature of cell to max
                # Click again to disable / enable cooling of the cell
                if event.button == 1:
                    if ca.ca_grid[int(self.mx), int(self.my)].pop == 0:
                        ca.ca_grid[int(self.mx), int(self.my)].pop = 1
                    else:
                        ca.ca_grid[int(self.mx), int(self.my)].pop = 0
                    print("Cell %i, %i = 1, P = %i" % (self.mx, self.my, ca.ca_grid[int(self.mx), int(self.my)].pop))

                # Click on right mouse button
                elif event.button == 3:
                    if ca.ca_grid[int(self.mx), int(self.my)].is_wall:
                        ca.ca_grid[int(self.mx), int(self.my)].is_wall = False
                        ca.ca_grid[int(self.mx), int(self.my)].pop = 0
                    else:
                        ca.ca_grid[int(self.mx), int(self.my)].is_wall = True
                        ca.ca_grid[int(self.mx), int(self.my)].pop = 1
                    print("Cell %i, %i = 1, P = %i" % (self.mx, self.my, ca.ca_grid[int(self.mx), int(self.my)].pop))

            # Keyboard key is pressed
            elif event.type == pygame.KEYUP:
                # space bar is pressed
                if event.key == pygame.K_SPACE:
                    GC.run_ca = not GC.run_ca
                    if GC.run_ca:
                        print("> unpause simulation")
                    else:
                        print("> pause simulation")
                # s pressed, perform one step of the simulation
                if event.key == pygame.K_s:
                    ca.cycle()
                # r pressed, reset the simulation
                if event.key == pygame.K_r:
                    ca.__init__(rule)
                # w pressed, create walls around the field
                if event.key == pygame.K_w:
                    ca.create_walls()

#########################################################################
###                          GLOBAL METHODS                           ###
#########################################################################


def main():
    """
    Main method. It executes the CA.
    :return: nothing
    """
    # initialize GUI
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
    pygame.display.set_caption('LGCA')

    # Initialize the ca grid.
    BBM = [0, 8, 4, 3, 2, 5, 9, 7, 1, 6, 10, 11, 12, 13, 14, 15]
    Bounce_Gas1 = [0, 8, 4, 3, 2, 5, 9, 14, 1, 6, 10, 13, 12, 11, 7, 15]
    Bounce_Gas2 = [0, 8, 4, 12, 2, 10, 9, 7, 1, 6, 5, 11, 3, 13, 14, 15]
    Critters = [15, 14, 13, 3, 11, 5, 6, 1, 7, 9, 10, 2, 12, 4, 8, 0]
    HPP_gas = [0, 8, 4, 12, 2, 10, 9, 14, 1, 6, 5, 13, 3, 11, 7, 15]
    Rotations1 = [0, 2, 8, 12, 1, 10, 9, 11, 4, 6, 5, 14, 3, 7, 13, 15]
    Rotations2 = [0, 2, 8, 12, 1, 10, 9, 13, 4, 6, 5, 7, 3, 14, 11, 15]
    Rotations3 = [0, 4, 1, 10, 8, 3, 9, 11, 2, 6, 12, 14, 5, 7, 13, 15]
    Rotations4 = [0, 4, 1, 12, 8, 10, 6, 14, 2, 9, 5, 13, 3, 11, 7, 15]
    Sand = [0, 4, 8, 12, 4, 12, 12, 13, 8, 12, 12, 14, 12, 13, 14, 15]
    String_Thing1 = [0, 1, 2, 12, 4, 10, 9, 7, 8, 6, 5, 11, 3, 13, 14, 15]
    String_Thing2 = [0, 1, 2, 12, 4, 10, 6, 7, 8, 9, 5, 11, 3, 13, 14, 15]
    Swap_On_Diag = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
    Tron = [15, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0]

    rule = Sand
    ca = LGCA(rule)
    ih = InputHandler()

    while 1:

        if GC.run_ca:
            ca.cycle()

        ca.draw_cells(screen)
        pygame.display.flip()
        ih.process_in(ca, rule)


if __name__ == '__main__':
    main()
