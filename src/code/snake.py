import pygame
from pygame.locals import *


# Snake class really just implements a body section of the snake.
# This allows us to iterate through a list, and tell the next segment where to move
# It also allows us to keep a snake head
# It will function like a linked list, where the node value is the rectangle, and next is the next segment
class Snake(pygame.sprite.Sprite):
    def __init__(self, game, location):
        super().__init__()
        self.game = game
        self.body_size = game.get_pixel_size()
        # Will need to add to this. Head will get a value.
        # When food is eaten, tail will add one in its position
        self.image = pygame.surface.Surface((self.body_size, self.body_size))
        self.rect = self.image.get_rect(center=location)
        self.image.fill("green")
        self.next = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, new_location, ate):
        # Get current location to update next leg with
        location = self.rect.center
        # Set current leg to new location
        self.rect.move_ip(new_location[0] - self.rect.x, new_location[1] - self.rect.y)

        # If there is more snake, continue the trend
        if self.next is not None:
            return self.next.update(location, ate)
        elif ate:
            new_snake = Snake(self.game, location)
        else:
            new_snake = None
        # If we added a new snake, we need to pass it back to the game update, to add to group
        self.next = new_snake
        return new_snake


class SnakeHead(Snake):
    # All the current init info is the same, really just want a unique update method
    def __init__(self, game, location):
        super().__init__(game, location)
        self.up = 0
        self.right = 1
        self.down = 2
        self.left = 3
        self.direction = 1
        self.speed = 0
        self.moves = [0, 1, 2]

    # Current update function allows one to hold down the up key and spam left and right, letting the snake turn
    # 180 degrees. I think I need to consider an array of locations, and a next allowed location function
    # Something that says the snake can only ever move in 3 directions. Instead of saying
    # Is the next direction 180 of the current direction, say
    # is next direction allowed. So if traveling right, the allowed directions are right, up, and down.
    # Then, until it moves, it tracks the last valid input.
    def update(self, pressed):
        # grab center to send to next in line
        location = self.rect.center
        # Don't want to be able to change direction 180 degrees
        if pressed[K_UP] and 0 in self.moves:
            self.direction = 0
        if pressed[K_RIGHT] and 1 in self.moves:
            self.direction = 1
        if pressed[K_DOWN] and 2 in self.moves:
            self.direction = 2
        if pressed[K_LEFT] and 3 in self.moves:
            self.direction = 3
        if self.speed < 0:
            self.speed -= 1
        else:
            self.speed = 1000
            match self.direction:
                # Only update the moves function after it moves, to stop 180 turns
                case self.up:
                    self.rect.move_ip(0, -self.body_size)
                    self.moves = [0, 1, 3]
                case self.right:
                    self.rect.move_ip(self.body_size, 0)
                    self.moves = [0, 1, 2]
                case self.down:
                    self.rect.move_ip(0, self.body_size)
                    self.moves = [1, 2, 3]
                case self.left:
                    self.rect.move_ip(-self.body_size, 0)
                    self.moves = [0, 2, 3]
        ate = self.rect.colliderect(self.game.get_apple())
        if self.next is not None:
            snake = self.next.update(location, ate)
        if ate:
            self.game.new_apple()
            if self.next is not None:
                return snake
            self.next = Snake(self.game, location)
            return self.next
        return None

