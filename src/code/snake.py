import pygame
from pygame.locals import *


# New snake class for cell version of game
# Snake needs its location, the ability to move to an adjacent cell, and update the next body
# segment.
# The init I think stays the same. Location will be center of cell, cell should handle positioning
class Snake:
    def __init__(self, game, cell):
        self.game = game
        self.cell = cell
        # SNAKE = 2
        self.cell.set_cell(2)
        self.body_size = cell.get_cell_size()
        # Will need to add to this. Head will get a value.
        # When food is eaten, tail will add one in its position
        # self.image = pygame.surface.Surface((self.body_size, self.body_size))
        # self.rect = self.image.get_rect(center=self.cell.get_center())
        # self.image.fill("green")
        self.next = None

    # TODO: Make snake draw itself. This will be in cell for now
    # def draw(self, surface):
    #     surface.blit(self.image, self.rect)

    # Okay hold up. Does the Snake fill out, or does the cell know it has a snake?
    # Do I need a whole snake class, or can the cell have 3 values - snake, fruit, empty?
    # I do want snake to be a linked list. But could it be a list of cell locations?
    # Head cell moves to a new location if empty or apple (board[x][y] = board[location.x][location.y])
    # Head now calls head.next to move to board[location.x][location.y]
    # head.next now does the same - board[location.x][location.y] = board[next.l.x][next.l.y]
    # and so on and so forth.
    # Snake is a linked list, with the ability to extend itself and eat fruit. It shouldn't be a surface
    # because the cell should draw itself?
    # But if we are learning pygame, should, at some point, make snake draw itself.
    def update(self, new_location, ate):
        # Don't need to check if next cell is empty - only snake head cares about this
        # Get current location to update next leg with
        location = self.cell.get_cell_location()
        # Game does the board[x][y] = board[old.x][old.y]
        self.game.update_board(new_location, location)
        # If there is more snake, continue the trend
        if self.next is not None:
            self.next.update(location, ate)
        # If snake is last we need to clear the cell, or make a new snake there.
        if ate:
            self.next = self.game.create_snake(location)
        else:
            self.game.clear_cell(location)
        self.cell = self.game.get_cell(new_location)


# I know inheritance doesn't make sense without shared methods - eventually draw will be shared
# If I stick with cell method, I will likely remove inheritance
class SnakeHead(Snake):
    # All the current init info is the same, really just want a unique update method
    def __init__(self, game, cell):
        super().__init__(game, cell)
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

    # Snake head now needs to check if it will move to a space outside of the board
    def update(self, pressed):
        # grab center to send to next in line
        x, y = self.cell.get_cell_location()
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
            target = (x, y)
            match self.direction:
                # Only update the moves function after it moves, to stop 180 turns
                case self.up:
                    # Need checks for edge of board
                    if y == 0:
                        self.game.end_game()
                        return 0
                    target = (x, y - 1)
                    self.moves = [0, 1, 3]
                case self.right:
                    if x == 49:
                        self.game.end_game()
                        return 0
                    target = (x + 1, y)
                    self.moves = [0, 1, 2]
                case self.down:
                    if y == 49:
                        self.game.end_game()
                        return 0
                    target = (x, y + 1)
                    self.moves = [1, 2, 3]
                case self.left:
                    if x == 0:
                        self.game.end_game()
                        return 0
                    target = (x - 1, y)
                    self.moves = [0, 2, 3]
            self.game.update_board(target, (x, y))
            # If there is more snake, continue the trend
            ate = False
            if self.next is not None:
                # Temp setting ate to false. Will handle apple after testing this works
                self.next.update((x, y), ate)
            # If snake is last we need to clear the cell, or make a new snake there.
            if ate:
                self.next = self.game.create_snake((x, y))
            else:
                self.game.clear_cell((x, y))
            self.cell = self.game.get_cell(target)

