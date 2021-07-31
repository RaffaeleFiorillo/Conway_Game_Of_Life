import random
import pygame

# -------------------------------------------- WORLD DEFINITION --------------------------------------------------------
LIFE_PROBABILITY = 0.09  # probability of a cell to be initiated as alive
COLUMNS = 100  # number of horizontal cells
ROWS = 100  # number of vertical cells
CELL_SIZE = 7  # side length of a cell (cells are squares)
BEING_SIZE = CELL_SIZE*3
BEING_CODE = 3  # type of being that will appear in the simulation. Only affects "Complex" simulation
COLORFUL = False  # True: live cells can be different colors | False: live cells are white | dead cells are always black
CONTINUITY = True  # True: cells interact with cells in different time references | False: " " " " same time reference
X_SPEED= 20  # speed of a being in the x axis
Y_SPEED= 20  # speed of a being in the y axis
SPEED_CHANGE_PROBABILITY = 0.7  # probability for a being to change his speed
MAX_SPEED_MODULE = 100  # the simulation's being can reach speeds inside: [- MAX_SPEED_MODULE; MAX_SPEED_MODULE] range

# ------------------------------------------- WINDOW DEFINITION --------------------------------------------------------
WINDOW_WIDTH = ROWS * CELL_SIZE  # width of the simulation window based on rows number and cell size
WINDOW_HEIGHT = COLUMNS * CELL_SIZE  # length of the simulation window based on column number and cell size
WINDOW_LABEL = "Conway's Game of Life"  # the lable that appears in the window border
CLOCK = pygame.time.Clock()  # clock to control the simulation loop regarding the frame rate
FRAME_RATE = 10  # how many times per second the screen is updated


COLORS = [(255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 0, 255), (255, 255, 255)]  # cell colors


# --------------------------------------------- BEING CREATION ---------------------------------------------------------
def center_screen_y():
    return (WINDOW_HEIGHT - BEING_SIZE)//2


def center_screen_x():
    return (WINDOW_WIDTH - BEING_SIZE)//2


def random_change(speed):
    return (speed+random.randint(5, 10) * random.choice([-1, 1])) * random.choice([-1, 1])\
        if (random.random() > SPEED_CHANGE_PROBABILITY) else speed


def random_movement(x, y, x_speed, y_speed, events=None):
    x_speed = random_change(x_speed)
    y_speed = random_change(y_speed)
    x += x_speed
    y += y_speed
    return x, y, x_speed, y_speed


def controlled_movement(x, y, x_speed, y_speed, event=None):
    movements = {None: (0, 0), "r": (x_speed, 0), "l": (-x_speed, 0), "u": (0, -y_speed), "d": (0, x_speed)}[event]
    return x+movements[0], y+movements[1], x_speed, y_speed


def draw_filled_square(screen, x, y, size, color):
    pygame.draw.rect(screen, color, (x+size//2, y+size//2, size, size))


def draw_unfilled_square(screen, x, y, size, color):
    pygame.draw.rect(screen, color, (x+size//2, y+size//2, size, size), int(size*0.1))


def draw_filled_circle(screen, x, y, size, color):
    pygame.draw.circle(screen, color, (x+size/2, y+size//2), size//2)


def draw_unfilled_circle(screen, x, y, size, color):
    pygame.draw.circle(screen, color, (x+size/2, y+size//2), size//2, int(size*0.1))


def get_being(code):
    # code 1 to 4 -> being with random movement | code 5 to 8 -> being with keyboard controlled movement
    # odd code -> being is a circle | even code -> being is circle
    being_behaviours = {1: [draw_unfilled_circle, random_movement],
                        2: [draw_unfilled_square, random_movement],
                        3: [draw_filled_circle, random_movement],
                        4: [draw_filled_square, random_movement],
                        5: [draw_unfilled_circle, controlled_movement],
                        6: [draw_unfilled_square, controlled_movement],
                        7: [draw_filled_circle, controlled_movement],
                        8: [draw_filled_square, controlled_movement]}

    being = [random.choice(COLORS),
             center_screen_x(),
             center_screen_y(),
             X_SPEED, Y_SPEED,
             BEING_SIZE,
             being_behaviours[code]]

    return being




