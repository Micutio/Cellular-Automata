#!/usr/bin/python

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
import random
import time
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

    def process_in(self, ca):
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
                    ca[int(self.mx), int(self.my)].cells = [True, True, True, True]
                    print("Cell %i, %i = 1, T = %i" % (self.mx, self.my, ca[int(self.mx), int(self.my)].pop))

                # Click on right mouse button
                elif event.button == 3:
                    ca[int(self.mx), int(self.my)].cells = [True, True, True, True]
                    print("Cell %i, %i = 1, T = %i" % (self.mx, self.my, ca[int(self.mx), int(self.my)].pop))

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
                    ca = cycle_ca(ca)

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
    ca = init_ca()
    ih = InputHandler()

    while 1:

        if GC.run_ca:
            ca = cycle_ca(ca)

        draw_cells(ca, screen)
        pygame.display.flip()
        ih.process_in(ca)


if __name__ == '__main__':
    main()
