import pygame
from pygame.locals import *


class Cell:
    def __init__(self, size, location):
        # Initialize to empty. If empty, when drawing, will draw a black rectangle
        # Alternatively, initialize to a black square, since that won't be how we check for collision
        # TODO: Move drawing into classes. For now, this handles everything
        self._empty = 0
        self._apple = 1
        self._snake = 2
        self.value = 0
        # store how big each cell is. This could maybe be at game level.
        self.size = size
        # Location storage, so snake head can easily remove it from available set, and snake tail
        # can easily add it to available set
        self.location = location
        # I think it will be header sizes + location*size? instead of 0,0
        self.rect = pygame.rect.Rect(0, 0, size, size)

    def draw(self, surface):
        match self.value:
            case self._empty:
                pygame.draw.rect(surface, "black", self.rect)
            case self._apple:
                pygame.draw.rect(surface, "white", self.rect)
            case self._snake:
                pygame.draw.rect(surface, "green", self.rect)

    def get_cell_size(self):
        return self.size

    def get_cell_location(self):
        return self.location

    def clear_self(self):
        self.value = None




