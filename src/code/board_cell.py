import pygame
from pygame.locals import *


class Cell:
    def __init__(self, size, location, x_offset, y_offset):
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
        self.board_location = location
        x = x_offset + (location[0]*size)
        y = y_offset + (location[1]*size)
        # I think it will be header sizes + location*size? instead of 0,0
        self.rect = pygame.rect.Rect(x, y, size, size)

    def draw(self, surface):
        match self.value:
            case self._apple:
                pygame.draw.rect(surface, "white", self.rect)
            case self._snake:
                pygame.draw.rect(surface, "green", self.rect)
            # We want to skip this for now, let board just be black
            case self._empty:
                pygame.draw.rect(surface, "black", self.rect)

    def get_cell_size(self):
        return self.size

    def get_cell_location(self):
        return self.board_location

    # def get_center(self):
        # Will need this when snake draws itself?

    def clear_self(self):
        self.value = None

    def set_cell(self, value):
        self.value = value

    # For testing:
    def __str__(self):
        return str(self.value)



