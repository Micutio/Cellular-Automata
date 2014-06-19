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


TMP = 0

#########################################################################
###                            CLASSES                                ###
#########################################################################


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
    pygame.display.set_caption('Complex Automaton')

    tick_delay = 0.05
    # Initialize the ca grid.
    ca = init_ca()

    # draw_grid(grid, 10)
    run_ca = False
    run_scenario = False
    while 1:
        for event in pygame.event.get():
            # The 'x' on the window is clicked
            if event.type == QUIT:
                sys.exit()

            # Mouse is moved
            elif event.type == MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                mx = (mx / 10)
                my = (my / 10)

            # Mouse button is pressed
            elif event.type == pygame.MOUSEBUTTONUP:
                # Click on left mouse button, set temperature of cell to max
                # Click again to disable / enable cooling of the cell
                if event.button == 1:
                    print("Cell %i, %i = 1, T = %i" % (mx, my, ca[int(mx), int(my)].temperature))
                    ca[int(mx), int(my)].temperature = MAX_TEMPERATURE
                    ca[int(mx), int(my)].persist = True

                # Click on right mouse button
                elif event.button == 3:
                    print("Cell %i, %i = 1, T = %i" % (mx, my, ca[int(mx), int(my)].temperature))
                    ca[int(mx), int(my)].temperature = 0
                    ca[int(mx), int(my)].persist = False

            # Keyboard key is pressed
            elif event.type == pygame.KEYUP:
                # space bar is pressed
                if event.key == pygame.K_SPACE:
                    run_ca = not run_ca
                # up arrow is pressed, speed up simulation
                if event.key == pygame.K_UP:
                    tick_delay /= 2
                    print("< seconds per simulation tick = " + str(tick_delay))
                # down arrow is pressed, slow down simulation
                if event.key == pygame.K_DOWN:
                    tick_delay *= 2
                    print("< seconds per simulation tick = " + str(tick_delay))

        if run_ca:
            ca = cycle_ca(ca)

        draw_cells(ca, screen)

        pygame.display.flip()
        time.sleep(tick_delay)


if __name__ == '__main__':
    main()
