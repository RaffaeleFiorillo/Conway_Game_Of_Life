import Classes as Cl
from configurations import COLORFUL, WINDOW_LABEL, COLUMNS, ROWS, LIFE_PROBABILITY, CONTINUITY, FRAME_RATE
from auxiliar import WINDOW_WIDTH, WINDOW_HEIGHT, CLOCK
import pygame
import sys


# --------------------------------------------    FUNCTIONS       ------------------------------------------------------
def keyboard_control():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:  # closing the window pressing SPACE
        return False
    
    if pressed[pygame.K_UP]:
        WORLD.move_being("u")
    if pressed[pygame.K_DOWN]:
        WORLD.move_being("d")
    if pressed[pygame.K_LEFT]:
        WORLD.move_being("l")
    if pressed[pygame.K_RIGHT]:
        WORLD.move_being("r")
    return True


# --------------------------------------------      SETUP         ------------------------------------------------------
pygame.init()  # initiate pygame and all it's components in order to work with it
SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))  # create the window/screen
RUN = True  # state of the simulation. "True" means it's running
pygame.display.set_caption(WINDOW_LABEL)  # set the window lable to be displayed

""" Conway's game of life """
WORLD = Cl.World_Grid(COLUMNS, ROWS, SCREEN, LIFE_PROBABILITY, colorful=COLORFUL, time_discontinuity=CONTINUITY)

""" Conway's game of life but with additional beings """
# WORLD = Cl.World_Grid_Complex(COLUMNS, ROWS, SCREEN, BEING_CODE, LIFE_PROBABILITY, colorful=COLORFUL,
# time_discontinuity=CONTINUITY)


# --------------------------------------------    GAME LOOP       ------------------------------------------------------

while RUN:
    CLOCK.tick(FRAME_RATE)  # run simulation with predefined frame rate
    # CLOCK.tick()  # run simulation with CPU full capacity

    movement_events = []  # will contain all the events relevant to the moving of a being, occurring in the simulation
    for event in pygame.event.get():  # iterates over simulation events (like pressing a button)
        EVENT = event.type  # current event in the iteration
        if EVENT == pygame.QUIT:  # closing the window pressing the red "X" in the window's border
            sys.exit()

    # RUN = keyboard_control(pygame.key.get_pressed())  # takes action based on keyboard input. Returns LOOP's run state

    # refresh the simulation to show alterations in the world's state
    WORLD.refresh()
    # WORLD.move_being(None)
    pygame.display.update()  # pygame updates the screen
