import pygame
from pygame.locals import *
from random import randint

from snake import Snake, SnakeHead

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
        self.board_top = (screen_height/5) + 4
        self.board_bottom = screen_height - 4
        self.board_left = 4
        self.board_right = screen_width - 4

        # defining pixel height for conversion - a square so don't need x and y
        self.pixel_size = 4

        self.header = pygame.rect.Rect(0, 0, screen_width, screen_height)
        self.board = pygame.rect.Rect(self.board_left, self.board_top,
                                      self.board_right - self.board_left, self.board_bottom - self.board_top)

        # Game Pieces
        self.snake = pygame.sprite.Group()
        self.snake_head = SnakeHead(self, (((self.board_right - self.board_left) / 2) + self.pixel_size / 2,
                                       (self.board_top + (self.board_bottom - self.board_top) / 2)
                                       - self.pixel_size / 2))
        self.snake.add(self.snake_head)
        # Will need to make this a function that chooses a random place on the board not currently occupied by snake
        # possibly eventually an "available spaces" type list, and choose a random
        # list and index from the size available
        self.apple = pygame.rect.Rect(randint(self.board_left, self.board_right),
                                      randint(self.board_top, self.board_bottom - self.pixel_size),
                                      self.pixel_size, self.pixel_size)

    def update(self, event):
        match self.game_state:
            # I shouldn't have button pressing problem when I pull the latest event each time
            case self.game_start:
                print()
            case self.game_running:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_p]:
                    print("Pause here")
                # have to check here for new snake to update our group for drawing
                new_snake = self.snake_head.update(pressed_keys)
                if new_snake is not None:
                    self.snake.add(new_snake)
            case self.game_paused:
                print()
            case self.game_end:
                print()
            case self.game_close:
                print("Game Closing")

    def draw(self, surface):
        # Draw header section
        pygame.draw.rect(surface, "grey", self.header)

        # Draw board section
        pygame.draw.rect(surface, "black", self.board)
        pygame.draw.rect(surface, "white", self.apple)
        self.snake.draw(surface)

    def run_game(self):
        return self.game_state != self.game_close

    def close_game(self):
        self.game_state = self.game_close

    def get_pixel_size(self):
        return self.pixel_size

    def get_apple(self):
        return self.apple

    # For now, random location.
    def new_apple(self):
        self.apple = pygame.rect.Rect(randint(self.board_left, self.board_right),
                                      randint(self.board_top, self.board_bottom - self.pixel_size),
                                      self.pixel_size, self.pixel_size)


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
    _game.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
