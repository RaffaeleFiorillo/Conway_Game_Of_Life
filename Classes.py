import random
import pygame
import auxiliar as a


# Class that manages the simulation. It is timeless because cells that are checked after base their changes in previous
# cells that have already been changed. In theory it's like if the later cells are checked, the later in the future this
# cells are relative to their previous neighbours. Time is directly proportional to the "X" and "Y" coordinates.
class World_Grid:
    def __init__(self, columns, rows, cell_size, screen,
                 initial_population=False, probability=False, colorful=False, time_discontinuity=False):
        self.initial_population = initial_population  # used for creating live cells based on cardinal number
        self.life_probability = probability  # used for creating live cells based on probability
        self.columns, self.rows = columns, rows  # number of cells: columns-> horizontal; rows-> vertical
        self.cell_grid = self.create_grid(cell_size, colorful, time_discontinuity)  # creates a grid of cells
        self.screen = screen  # surface where the simulation is displayed

    # creates a grid based on the cell creation method preferred by the user
    def create_grid(self, cell_size, colorful, time_discontinuity):
        if self.life_probability:  # using the probability is the priority upon initial population number
            cell_creation_method = self.alive_or_dead_1
        elif self.initial_population:  # uses the initial population number to get a probability for cells to be alive
            cell_creation_method = self.alive_or_dead_2
        else:  # 50/50 chance of a cell being alive
            cell_creation_method = self.alive_or_dead_random
        return [[self.create_cell(cell_creation_method, _1, _2,
                                  cell_size, colorful, time_discontinuity)  # creates a 2D list of cells
                 for _1 in range(self.columns)
                 ] for _2 in range(self.rows)
                ]

    @staticmethod
    def create_cell(creation_method, y, x, cell_size, colorful, time_discontinuity):
        return Cell(creation_method(), x, y, cell_size, colorful, time_discontinuity)

    def alive_or_dead_1(self):  # returns a 1 or 0 based on a probability
        life_state = 1 if random.random() <= self.life_probability else 0
        return life_state

    def alive_or_dead_2(self):  # returns a 1 or 0 based on a calculated
        life_probability = self.initial_population / (self.columns * self.rows)
        life_state = 1 if random.random() <= life_probability else 0
        return life_state

    @staticmethod
    def alive_or_dead_random():  # returns a 1 or 0 with a 50/50 chance
        return random.choice([1, 0])

    def get_surrounding(self, x, y):  # returns a list of 1&0, which are the neighbor cells state . 1-> alive; 0-> dead
        left = x - 1  # x coordinate of the left neighbors
        right = x + 1  # x coordinate of the right neighbors
        up = y - 1  # y coordinate of the upper neighbors
        low = y + 1  # y coordinate of the lower neighbors

        if left < 0:  # if the cell is in the first column it can have no left neighbors
            left = False
        if right > self.columns - 1:  # if the cell is in the last column it can have no right neighbors
            right = False
        if up < 0:  # if the cell is in the first row it can have no upper neighbors
            up = False
        if low > self.rows - 1:  # if the cell is in the last row it can have no lower neighbors
            low = False

        up_left = self.cell_grid[left][up].life_state if (left and up) else False  # upper left neighbor's state
        up_center = self.cell_grid[x][up].life_state if up else False  # upper center neighbor's state
        up_right = self.cell_grid[right][up].life_state if (right and up) else False  # upper right neighbor's state
        mid_left = self.cell_grid[left][y].life_state if left else False  # medium left neighbor's state
        mid_right = self.cell_grid[right][y].life_state if right else False  # medium right neighbor's state
        low_left = self.cell_grid[left][low].life_state if (left and low) else False  # lower left neighbor's state
        low_center = self.cell_grid[x][y + 1].life_state if low else False  # lower center neighbor's state
        low_right = self.cell_grid[right][low].life_state if (left and low) else False  # lower right neighbor's state

        return [up_left, up_center, up_right, mid_left, mid_right, low_left, low_center, low_right]

    def update_cell_grid(self):
        [[self.cell_grid[x][y].update_state(self.get_surrounding(x, y))
          for y in range(self.columns)]
         for x in range(self.rows)]

    def draw_cells(self):
        # self.print_grid()
        [[self.cell_grid[y][x].draw(self.screen) for x in range(self.columns)] for y in range(self.rows)]

    def refresh(self):
        self.update_cell_grid()  # simulation rules are applied for each existing cell
        self.draw_cells()  # each cell is drawn into the window


# same world but with an additional being. The being moves freely among cells and affects them
class World_Grid_Complex(World_Grid):
    def __init__(self, columns, rows, cell_size, screen, being_code,
                 initial_population=False, probability=False, colorful=False, time_discontinuity=False):
        super().__init__(columns, rows, cell_size, screen)
        self.being = Being(being_code)

    def update_cell_grid(self):
        # code for alteration due the existence of the Being. May have to be done after updating the cells
        [[self.cell_grid[x][y].update_state(self.get_surrounding(x, y))
          for y in range(self.columns)]
         for x in range(self.rows)]

    def move_being(self, event):
        self.being.move(event)

    def draw_cells(self):
        [[self.cell_grid[y][x].draw(self.screen) for x in range(self.columns)] for y in range(self.rows)]
        self.being.draw(self.screen)


# Class that represents the Cells in the simulation
class Cell:
    def __init__(self, alive, x, y, size, colorful=False, time_discontinuity=False):
        self.life_state = 1 == alive
        self.future_life_state = self.life_state
        self.colors = self.get_colors(colorful)
        self.color = random.choice(a.COLORS)
        self.draw = self.draw_time_discontinuous if time_discontinuity else self.draw_time_continuous
        self.update_state = self.update_state_time_discontinuous if time_discontinuity\
            else self.update_state_time_continuous
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
        self.color = random.choice(a.COLORS)
        return 0, 0, 0

    @staticmethod
    def black_color():
        return 0, 0, 0

    @staticmethod
    def white_color():
        return 255, 255, 255

    def update_state_time_discontinuous(self, surrounding):
        life_level = sum(surrounding)
        if life_level < 2:
            self.life_state = False
        elif life_level > 3:
            self.life_state = False
        elif life_level == 3:
            self.life_state = True

    def update_state_time_continuous(self, surrounding):
        life_level = sum(surrounding)
        if life_level < 2:
            self.future_life_state = False
        elif life_level > 3:
            self.future_life_state = False
        elif life_level == 3:
            self.future_life_state = True

    def draw_time_discontinuous(self, screen):
        color = self.colors[self.life_state]()
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))

    def draw_time_continuous(self, screen):
        self.life_state = self.future_life_state
        color = self.colors[self.life_state]()
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))


class Being:
    def __init__(self, code):
        self.color = None  # color of the being
        self.x = None  # x coordinate of the being
        self.y = None  # y coordinate of the being
        self.speed_x = None  # speed at which the being moves inside the screen in the X axis
        self.speed_y = None  # speed at which the being moves inside the screen in the Y axis
        self.size = None  # size of the being
        self.draw_function = None  # function responsible for drawing the being on the screen
        self.movement_control_function = None   # function responsible for moving the being on the screen
        self.initialize_being(code)

    def initialize_being(self, code):
        data = a.get_being(code)
        self.color = data[0]
        self.x = data[1]
        self.y = data[2]
        self.speed_x = data[3]
        self.speed_y = data[4]
        self.size = data[5]
        self.draw_function = data[6][0]
        self.movement_control_function = data[6][1]

    def draw(self, screen):
        self.draw_function(screen, self.x, self.y, self.size, self.color)

    def move(self, event):
        result = self.movement_control_function(self.x, self.y, self.speed_x, self.speed_y, event)
        if 0 < result[0] < a.WINDOW_WIDTH:
            self.x = result[0]
        if 0 < result[1] < a.WINDOW_HEIGHT:
            self.y = result[1]
        if -a.MAX_SPEED_MODULE < result[2] < a.MAX_SPEED_MODULE:
            self.speed_x = result[2]
        if -a.MAX_SPEED_MODULE < result[3] < a.MAX_SPEED_MODULE:
            self.speed_y = result[3]
