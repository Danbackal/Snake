import pygame
from pygame.locals import *
from random import randint
import os

from snake import Snake, SnakeHead
from board_cell import Cell

# Snake Game
# Need game class - hold creation of apples, holds score, holds snake.
# Snake class - do we need a full class? Or can we create a snake segment class
# and game just holds and updates the snake segment group?
# Initial thought - set up game holding everything. May not need multiple classes this time.

# Playable area will be 400x400. Extra 100 on top for title/score
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
FPS = 30
current_work_dir = os.getcwd()
current_work_dir = current_work_dir[:-5]
os.chdir(current_work_dir)


class Game:  # Game does not need to be a sprite - it holds sprites.
    def __init__(self, screen_width, screen_height):
        # Start with game information
        self.game_start = 0
        self.game_running = 1
        self.game_paused = 2
        self.game_end = 3
        self.game_close = 4
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Menu strings should be left aligned, but I don't want "> " to indent the active string... or do I, would that
        # look more retro
        self.active_choice = 0
        self.start = "start"
        self.resume = "resume"
        self.restart = "restart"
        self.quit = "quit"
        self.active_icon = "> "
        self.menu_cooldown = 3
        self.menu = []

        # Need font objects for the menus
        # Only ever need three at one time. Place first, second, third. Background is black, text is white
        # If third isn't used, it'll just not show up.
        # Menu update functions will update strings for us
        self.menu_font = pygame.font.Font("resources/Orbitron-Regular.ttf", 14)
        self.menu_text = []
        self.menu_rects = []
        # Hard coding locations for now, want to test functionality
        self.menu_border = pygame.rect.Rect(100, 200, 200, 200)
        self.menu_body = pygame.rect.Rect(102, 202, 196, 196)
        self.menu_locations = [(120, 220), (120, 240), (120, 260)]

        self.board_top = (screen_height/5)

        # defining pixel height for conversion - a square so don't need x and y
        self.pixel_size = screen_width / 40

        self.header = pygame.rect.Rect(0, 0, screen_width, screen_height)
        self.title_font = pygame.font.Font("resources/Orbitron-Bold.ttf", 30)
        self.title = self.title_font.render("Snake", True, "black")
        self.title_rect = self.title.get_rect(topleft=(10, 10))
        self.score = 0
        self.score_font = pygame.font.Font("resources/Orbitron-Regular.ttf", 18)
        self.scoreboard = self.score_font.render(f"Score: {self.score}", True, "black")
        self.scoreboard_rect = self.scoreboard.get_rect(topleft=(280, 60))

        # Game Start initializations. Check the best way to do this in python, this is messy
        self.game_state = 0
        self.board = [[]]
        self.available_cells = []
        self.snake_head = 0
        self.start_game()

    # Game Loop Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update(self):
        # events are for change in key status - good for menus
        # pressed keys are for status of key - good for things where keys are held down (parachuter) but
        # not needed for snake, a single input game.
        # Revamp - switch to event triggers
        for event in pygame.event.get():
            if event.type == QUIT:
                self.close_game()
            elif event.type == KEYDOWN:
                if self.game_state == self.game_running:
                    if event.key == K_p:
                        self.game_state = self.game_paused
                        self.menu_builder()
                    self.snake_head.update_movement(event.key)
                elif self.game_state == self.game_close:
                    print("Game Closing")
                else:
                    if event.key == K_UP:
                        self.menu_up()
                    elif event.key == K_DOWN:
                        self.menu_down()
                    elif event.key == K_RETURN:
                        self.menu_select()
        if self.game_state == self.game_running:
            self.snake_head.update()

    def draw(self, surface):
        # Draw header section
        pygame.draw.rect(surface, "grey", self.header)
        surface.blit(self.title, self.title_rect)
        surface.blit(self.scoreboard, self.scoreboard_rect)

        # Draw board section
        for i in self.board:
            for j in i:
                j.draw(surface)

        # If in menu - draw over board
        if self.game_state != self.game_running:
            pygame.draw.rect(surface, "white", self.menu_border)
            pygame.draw.rect(surface, "black", self.menu_body)
            for i in range(len(self.menu_text)):
                surface.blit(self.menu_text[i], self.menu_rects[i])

    # Game Set UP and Run Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Function to start up game. Moving out of init func to make it easy to restart game
    def start_game(self):
        self.game_state = 0
        # Board is now List of List of Surfaces
        # Draw for board will be drawing each cell, and each cell will have an empty or not functionality
        # If cell is empty, it will draw black. else, draw the sprite it contains

        # Board space should be... 40x40
        # Each cell gets passed top left offset for rect definition
        self.board = [[Cell(self.pixel_size, (i, j), 0, self.board_top) for j in range(50)]
                      for i in range(50)]

        # List of available spaces. When last snake part leaves a space, it enters this list again.
        # When snake head enters area, it is removed from this list.
        self.available_cells = []
        for x in range(40):
            for y in range(40):
                self.available_cells.append((x, y))
        # Don't want to initialize snake cells with cell removal, so pre-empting snake head here
        self.available_cells.remove((19, 19))

        # Game Pieces
        self.snake_head = SnakeHead(self, self.board[19][19])
        self.score = -1
        self.new_apple()
        self.menu_builder()

    def run_game(self):
        return self.game_state != self.game_close

    def end_game(self):
        self.game_state = self.game_end
        self.menu_builder()

    def close_game(self):
        self.game_state = self.game_close

    def get_pixel_size(self):
        return self.pixel_size

    # Cell related function
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def update_board(self, target, value):
        # Used for updating the snake
        self.board[target[0]][target[1]].set_cell(self.board[value[0]][value[1]].get_value())
        # SNAKE = 2
        self.board[target[0]][target[1]].set_cell(2)

    def remove_available_cells(self, target):
        self.available_cells.remove(target)

    def clear_cell(self, cell):
        self.board[cell[0]][cell[1]].clear_self()
        self.available_cells.append(cell)

    def get_cell(self, cell):
        return self.board[cell[0]][cell[1]]

    def fruit_check(self, target):
        return self.board[target[0]][target[1]].get_value() == 1

    # Apple functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Random apple location from available cells
    def new_apple(self):
        x, y = self.available_cells[randint(0, len(self.available_cells))]
        # APPLE = 1
        self.board[x][y].set_cell(1)
        self.score += 1
        self.scoreboard = self.score_font.render(f"Score: {self.score}", True, "black")
        self.scoreboard_rect = self.scoreboard.get_rect(topleft=(280, 60))


    # Snake Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def create_snake(self, location):
        return Snake(self, self.board[location[0]][location[1]])

    # Menu Functions
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Thought is we keep a list of texts that we can manipulate in place.
    # This seems to not be working
    def menu_up(self):
        if self.active_choice > 0:
            self.menu[self.active_choice] = self.menu[self.active_choice][2:]
            self.menu_text[self.active_choice] = self.menu_font.render(self.menu[self.active_choice], True,
                                                                       "white", "black")
            self.menu_rects[self.active_choice] = (self.menu_text[self.active_choice]
                                                   .get_rect(topleft=self.menu_locations[self.active_choice]))
            self.active_choice -= 1
            self.menu[self.active_choice] = self.active_icon + self.menu[self.active_choice]
            self.menu_text[self.active_choice] = self.menu_font.render(self.menu[self.active_choice], True,
                                                                       "white", "black")
            self.menu_rects[self.active_choice] = (self.menu_text[self.active_choice]
                                                   .get_rect(topleft=self.menu_locations[self.active_choice]))

    def menu_down(self):
        if self.active_choice < len(self.menu) - 1:
            self.menu[self.active_choice] = self.menu[self.active_choice][2:]
            self.menu_text[self.active_choice] = self.menu_font.render(self.menu[self.active_choice], True,
                                                                       "white", "black")
            self.menu_rects[self.active_choice] = (self.menu_text[self.active_choice]
                                                   .get_rect(topleft=self.menu_locations[self.active_choice]))
            self.active_choice += 1
            self.menu[self.active_choice] = self.active_icon + self.menu[self.active_choice]
            self.menu_text[self.active_choice] = self.menu_font.render(self.menu[self.active_choice], True,
                                                                       "white", "black")
            self.menu_rects[self.active_choice] = (self.menu_text[self.active_choice]
                                                   .get_rect(topleft=self.menu_locations[self.active_choice]))

    def menu_select(self):
        match self.menu[self.active_choice]:
            case "> start":
                self.game_state = 1
            case "> resume":
                self.game_state = 1
            case "> restart":
                self.start_game()
            case "> quit":
                self.game_state = 4

    def menu_builder(self):
        self.active_choice = 0
        self.menu = []
        self.menu_text = []
        self.menu_rects = []
        match self.game_state:
            case self.game_start:
                # start of game
                self.menu.append(self.active_icon + self.start)
                self.menu.append(self.quit)
                self.menu_text.append(self.menu_font.render(self.menu[0], True, "white", "black"))
                self.menu_rects.append(self.menu_text[0].get_rect(topleft=self.menu_locations[0]))
                self.menu_text.append(self.menu_font.render(self.menu[1], True, "white", "black"))
                self.menu_rects.append(self.menu_text[1].get_rect(topleft=self.menu_locations[1]))
            case self.game_paused:
                self.menu.append(self.active_icon + self.resume)
                self.menu.append(self.restart)
                self.menu.append(self.quit)
                self.menu_text.append(self.menu_font.render(self.menu[0], True, "white", "black"))
                self.menu_rects.append(self.menu_text[0].get_rect(topleft=self.menu_locations[0]))
                self.menu_text.append(self.menu_font.render(self.menu[1], True, "white", "black"))
                self.menu_rects.append(self.menu_text[1].get_rect(topleft=self.menu_locations[1]))
                self.menu_text.append(self.menu_font.render(self.menu[2], True, "white", "black"))
                self.menu_rects.append(self.menu_text[2].get_rect(topleft=self.menu_locations[2]))
            case self.game_end:
                self.menu.append(self.active_icon + self.restart)
                self.menu.append(self.quit)
                self.menu_text.append(self.menu_font.render(self.menu[0], True, "white", "black"))
                self.menu_rects.append(self.menu_text[0].get_rect(topleft=self.menu_locations[0]))
                self.menu_text.append(self.menu_font.render(self.menu[1], True, "white", "black"))
                self.menu_rects.append(self.menu_text[1].get_rect(topleft=self.menu_locations[1]))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)

# Game loop
while _game.run_game():

    _game.update()

    # draw
    screen.fill("black")
    _game.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
