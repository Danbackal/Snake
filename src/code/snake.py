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
        self.direction = 4
        self.speed = 0

    def update(self, pressed, ate):
        # grab center to send to next in line
        location = self.rect.center
        # Don't want to be able to change direction 180 degrees
        if pressed[K_UP]:
            if self.direction != self.down:
                self.direction = 0
        if pressed[K_RIGHT]:
            if self.direction != self.left:
                self.direction = 1
        if pressed[K_DOWN]:
            if self.direction != self.up:
                self.direction = 2
        if pressed[K_LEFT]:
            if self.direction != self.right:
                self.direction = 3
        if self.speed < 0:
            self.speed -= 1
        else:
            self.speed = 4
            match self.direction:
                case self.up:
                    self.rect.move_ip(0, -self.body_size)
                case self.right:
                    self.rect.move_ip(self.body_size, 0)
                case self.down:
                    self.rect.move_ip(0, self.body_size)
                case self.left:
                    self.rect.move_ip(-self.body_size, 0)
        # return self.next.update(location, ate)

