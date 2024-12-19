import pygame
from pygame.locals import *
from random import randint

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


class Game:  # Game does not need to be a sprite - it holds sprites.
    def __init__(self, screen_width, screen_height):
        # Start with game information
        self.game_start = 0
        self.game_running = 1
        self.game_paused = 2
        self.game_end = 3
        self.game_close = 4
        self.game_state = 1  # Will change when I build the menus
        self.screen_width = screen_width
        self.screen_height = screen_height

        # defining sizes as variable, in case I want to change the size of the game later
        # defining board borders for collision and bounding
        # TODO Change this. Wont work with cell format (I think)
        self.board_top = (screen_height/5) + 4

        # defining pixel height for conversion - a square so don't need x and y
        self.pixel_size = screen_width / 40

        self.header = pygame.rect.Rect(0, 0, screen_width, screen_height)

        # Board is now List of List of Surfaces (or sprites?)
        # Draw for board will be drawing each cell, and each cell will have an empty or not functionality
        # If cell is empty, it will draw black. else, draw the sprite it contains
        # Won't need a Sprite Group for snake drawing this way

        # Need a way to get all empty cells for new Apple creation. Come up with this later
        # (Maybe a set of unvisited - when tail of snake leaves cell, if re-adds it to options, and
        # when snake head enters one, it takes it away)
        # That is good - does mean snake needs to know what cell it is in. This should help collisions I think.

        # Board space should be... 40x40?
        # For now, 40x40 to work with 400. We will work out kinks later. No border
        # X offset is just the small border: self.board_left
        # similarly, Y is header: self.board_top
        # Do we want to give each cell the top left? Yes, because of def of rect
        self.board = [[Cell(self.pixel_size, (i, j), 0, self.board_top) for j in range(50)]
                      for i in range(50)]

        # Game Pieces
        self.snake_head = SnakeHead(self, self.board[19][19])
        # Will need to make this a function that chooses a random place on the board not currently occupied by snake
        # possibly eventually an "available spaces" type list, and choose a random
        # list and index from the size available

        # TODO: Build apple
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # self.apple = pygame.rect.Rect(randint(self.board_left, self.board_right),
        #                               randint(self.board_top, self.board_bottom - self.pixel_size),
        #                               self.pixel_size, self.pixel_size)

    def update(self, event):
        match self.game_state:
            # I shouldn't have button pressing problem when I pull the latest event each time
            case self.game_start:
                print()
            case self.game_running:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_p]:
                    print("Pause here")
                self.snake_head.update(pressed_keys)
            case self.game_paused:
                print()
            case self.game_end:
                print("Game Over")
            case self.game_close:
                print("Game Closing")

    def draw(self, surface):
        # Draw header section
        pygame.draw.rect(surface, "grey", self.header)

        # TODO:
        # Current draw shows board uneven, and split up by white lines, where pixel space leaks through.
        # This is okay, if background is also black. Would also let us not draw empty cells (space saver)
        # But still needs big fixes
        # Draw board section
        for i in self.board:
            for j in i:
                j.draw(surface)

    def run_game(self):
        return self.game_state != self.game_close

    def end_game(self):
        self.game_state = self.game_end

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

    def clear_cell(self, cell):
        self.board[cell[0]][cell[1]].clear_self()

    def get_cell(self, cell):
        return self.board[cell[0]][cell[1]]

    # def get_apple(self):
    #     return self.apple

    # For now, random location.
    # TODO: New apple func
    # def new_apple(self):
    #     self.apple = pygame.rect.Rect(randint(self.board_left, self.board_right),
    #                                   randint(self.board_top, self.board_bottom - self.pixel_size),
    #                                   self.pixel_size, self.pixel_size)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
_game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)

# Game loop
while _game.run_game():
    # check for closures
    # Need a way to say if this is a mouse click, pass it to update also
    for event in pygame.event.get():
        if event.type == QUIT:
            _game.close_game()

    _game.update("Pass")

    # draw
    screen.fill("black")
    _game.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
