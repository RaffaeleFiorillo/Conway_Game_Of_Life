import Classes as Cl
import pygame

# -------------------------------------------- WORLD DEFINITION --------------------------------------------------------
LIFE_PROBABILITY = 0.2  # probability of a cell to be initiated as alive
COLUMNS = 90  # number of horizontal cells
ROWS = 90  # number of vertical cells
CELL_SIZE = 10  # side length of a cell (cells are squares)
COLORFUL = False  # True: live cells can be different colors | False: live cells are white | dead cells are always black
CONTINUITY = False  # True: cells interact with cells in different time references | False: " " " " same time reference

# ------------------------------------------- WINDOW DEFINITION --------------------------------------------------------
WINDOW_WIDTH = ROWS * CELL_SIZE  # width of the simulation window based on rows number and cell size
WINDOW_HEIGHT = COLUMNS * CELL_SIZE  # length of the simulation window based on column number and cell size
WINDOW_LABEL = "Conway's Game of Life"  # the lable that appears in the window border
CLOCK = pygame.time.Clock()  # clock to control the simulation loop regarding the frame rate
FRAME_RATE = 10  # how many times per second the screen is updated


# --------------------------------------------    FUNCTIONS       ------------------------------------------------------
def refresh():  # updates the simulation for each generation
    WORLD.update_cell_grid()  # simulation rules are applied for each existing cell
    WORLD.draw_cells()  # each cell is drawn into the window
    pygame.display.update()  # pygame updates the screen


# --------------------------------------------      SETUP         ------------------------------------------------------
pygame.init()  # initiate pygame and all it's components in order to work with it
SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))  # create the window/screen
RUN = True  # state of the simulation. "True" means it's running
pygame.display.set_caption(WINDOW_LABEL)  # set the window lable to be displayed

""" Timeless Version of Conway's game of life"""
WORLD = Cl.World_Grid(COLUMNS, ROWS, CELL_SIZE, SCREEN,
                      probability=LIFE_PROBABILITY, colorful=COLORFUL, time_discontinuity=CONTINUITY)

""" Classic Version of Conway's game of life"""
# WORLD = Cl.World_Grid_Timeless(COLUMNS, ROWS, CELL_SIZE, SCREEN, probability=LIFE_PROBABILITY, colorful=COLORFUL)

refresh()  # first world update that the user sees

# --------------------------------------------    GAME LOOP       ------------------------------------------------------
while RUN:
    CLOCK.tick(FRAME_RATE)  # run simulation with predefined frame rate
    # CLOCK.tick()  # run simulation with CPU full capacity
    for event in pygame.event.get():  # iterates over simulation events (like pressing a button)
        EVENT = event.type  # current event in the iteration
        if EVENT == pygame.QUIT:  # closing the window pressing the red "X" in the window's border
            RUN = False
        if EVENT == pygame.KEYDOWN:  # closing the window pressing SPACE
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                RUN = False
    refresh()  # refresh the simulation to show alterations in the world's state
