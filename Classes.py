import random
import pygame

COLORS = [(255, 0, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 0, 255), (255, 255, 255)]  # cell colors


# Class that manages the simulation. It is timeless because cells that are checked after base their changes in previous
# cells that have already been changed. In theory it's like if the later cells are checked, the later in the future this
# cells are relative to their previous neighbours. Time is directly proportional to the "X" and "Y" coordinates.
class World_Grid_Timeless:
    def __init__(self, columns, rows, cell_size, screen, initial_population=False, probability=False, colorful=False):
        self.initial_population = initial_population  # used for creating live cells based on cardinal number
        self.life_probability = probability   # used for creating live cells based on probability
        self.columns, self.rows = columns, rows  # number of cells: columns-> horizontal; rows-> vertical
        self.cell_grid = self.create_grid(cell_size, colorful)  # creates a grid of cells according to parameters
        self.screen = screen  # surface where the simulation is displayed

    # creates a grid based on the cell creation method preferred by the user
    def create_grid(self, cell_size, colorful):
        if self.life_probability:  # using the probability is the priority upon initial population number
            cell_creation_method = self.alive_or_dead_1
        elif self.initial_population:  # uses the initial population number to get a probability for cells to be alive
            cell_creation_method = self.alive_or_dead_2
        else:  #
            cell_creation_method = self.alive_or_dead_random
        return [[self.create_cell(cell_creation_method, _1, _2, cell_size, colorful)
                 for _1 in range(self.columns)
                 ] for _2 in range(self.rows)
                ]

    def print_grid(self):
        [[print(self.cell_grid[y][x].alive) for x in range(self.columns)] for y in range(self.rows)]
        print()

    @staticmethod
    def create_cell(creation_method, y, x, cell_size, colorful):
        return Cell(creation_method(), x, y, cell_size, colorful)

    def alive_or_dead_1(self):
        life_state = 1 if random.random() <= self.life_probability else 0
        return life_state

    def alive_or_dead_2(self):
        life_probability = self.initial_population / (self.columns * self.rows)
        life_state = 1 if random.random() <= life_probability else 0
        return life_state

    @staticmethod
    def alive_or_dead_random():
        return random.choice([1, 0])

    def get_surrounding(self, x, y):
        left = x - 1
        right = x + 1
        sup = y - 1
        low = y + 1

        if left < 0:
            left = False
        if right > self.columns - 1:
            right = False
        if sup < 0:
            sup = False
        if low > self.rows - 1:
            low = False

        sup_left = self.cell_grid[left][sup].life_state if (left and sup) else False
        sup_center = self.cell_grid[x][sup].life_state if sup else False
        sup_right = self.cell_grid[right][sup].life_state if (right and sup) else False
        mid_left = self.cell_grid[left][y].life_state if left else False
        mid_right = self.cell_grid[right][y].life_state if right else False
        low_left = self.cell_grid[left][low].life_state if (left and low) else False
        low_center = self.cell_grid[x][y + 1].life_state if low else False
        low_right = self.cell_grid[right][low].life_state if (left and low) else False

        return [sup_left, sup_center, sup_right, mid_left, mid_right, low_left, low_center, low_right]

    def update_cell_grid(self):
        [[self.cell_grid[x][y].update_state(self.get_surrounding(x, y))
          for y in range(self.columns)]
         for x in range(self.rows)]

    def draw_cells(self):
        # self.print_grid()
        [[self.cell_grid[y][x].draw(self.screen) for x in range(self.columns)] for y in range(self.rows)]


# Class that represents the Cells in the simulation
class Cell:
    def __init__(self, alive, x, y, size, colorful=False):
        self.life_state = 1 == alive
        self.colors = self.get_colors(colorful)
        self.color = random.choice(COLORS)
        self.x = x * size
        self.y = y * size
        self.size = size

    def get_colors(self, colorful):
        variety_colors = {True: self.alive_color, False: self.dead_color}
        binary_colors = {True: self.white_color, False: self.dead_color}
        return {True: variety_colors, False: binary_colors}[colorful]

    def alive_color(self):
        return self.color

    def dead_color(self):
        self.color = random.choice(COLORS)
        return 0, 0, 0

    @staticmethod
    def black_color():
        return 0, 0, 0

    @staticmethod
    def white_color():
        return 255, 255, 255

    def update_state(self, surrounding):
        life_level = sum(surrounding)
        if life_level < 2:
            self.life_state = False
        elif life_level > 3:
            self.life_state = False
        elif life_level == 3:
            self.life_state = True

    def draw(self, screen):
        color = self.colors[self.life_state]()
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))
