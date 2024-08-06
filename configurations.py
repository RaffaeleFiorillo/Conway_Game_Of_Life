from random import choices, randint, random

ALL_COLORS = [(255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 0, 255), (255, 255, 255)]
COLORS = choices(ALL_COLORS, k=randint(1, len(ALL_COLORS)))  # cell colors

COLORFUL = False  # True: live cells can be different colors | False: live cells are white | dead cells are always black
CONTINUITY = False  # True: cells interact with cells in different time references | False: " " " " same time reference
MAKE_LIFE_PROBABILITY_RANDOM = True

MIN_LIFE_PROBABILITY = 0.005
MAX_LIFE_PROBABILITY = 0.7
LIFE_PROBABILITY = 0.05  # probability of a cell to be initiated as alive
if MAKE_LIFE_PROBABILITY_RANDOM:
	prob = random()/randint(2, 10)
	LIFE_PROBABILITY = min(MAX_LIFE_PROBABILITY, max(MIN_LIFE_PROBABILITY, prob))
	
COLUMNS = 260  # number of horizontal cells
ROWS = 260  # number of vertical cells
CELL_SIZE = 3  # side length of a cell (cells are squares)
BEING_SIZE = CELL_SIZE*3

BEING_CODE = 0  # type of being that will appear in the simulation. Only affects "Complex" simulation
X_SPEED = 20  # speed of a being in the x-axis
Y_SPEED = 20  # speed of a being in the y-axis
SPEED_CHANGE_PROBABILITY = 0.8  # probability for a being to change his speed
MAX_SPEED_MODULE = 100  # the simulation's being can reach speeds inside: [- MAX_SPEED_MODULE; MAX_SPEED_MODULE] range
BEING_EFFECT_NATURE = False  # effect of the being when touching cells. True: revives; False: kills
WINDOW_LABEL = "Conway's Game of Life"  # the lable that appears in the window border
FRAME_RATE = 60  # how many times per second the screen is updated
