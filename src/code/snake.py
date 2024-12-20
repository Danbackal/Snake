import pygame
from pygame.locals import *


class Snake:
    def __init__(self, game, cell):
        self.game = game
        self.cell = cell
        # SNAKE = 2
        self.cell.set_cell(2)
        self.body_size = cell.get_cell_size()
        self.next = None

    # Head cell moves to a new location if empty or apple (board[x][y] = board[location.x][location.y])
    # Head now calls head.next to move to board[location.x][location.y]
    # head.next now does the same - board[location.x][location.y] = board[next.l.x][next.l.y]
    # and so on and so forth.
    # Snake is a linked list, with the ability to extend itself and eat fruit. It shouldn't be a surface
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
        elif ate:
            self.next = self.game.create_snake(location)
            self.game.new_apple()
        else:
            self.game.clear_cell(location)
        self.cell = self.game.get_cell(new_location)


# I know inheritance doesn't make sense without shared methods - eventually draw will be shared
# If I stick with cell method, I will likely remove inheritance
class SnakeHead:
    # All the current init info is the same, really just want a unique update method
    def __init__(self, game, cell):
        self.game = game
        self.cell = cell
        self.cell.set_cell(2)
        self.body_size = cell.get_cell_size()
        self.next = None
        self.up = 0
        self.right = 1
        self.down = 2
        self.left = 3
        self.direction = 1
        self.speed = 0
        self.moves = [0, 1, 2]

    # Snake head takes care of hitting a wall/snake segment, and direction. Snake body just listens to head
    # No need for checks from snake body
    def update(self, pressed):
        # grab center to send to next in line
        x, y = self.cell.get_cell_location()
        target = (x, y)
        # Don't want to be able to change direction 180 degrees
        if pressed[K_UP] and 0 in self.moves:
            self.direction = 0
        if pressed[K_RIGHT] and 1 in self.moves:
            self.direction = 1
        if pressed[K_DOWN] and 2 in self.moves:
            self.direction = 2
        if pressed[K_LEFT] and 3 in self.moves:
            self.direction = 3
        if self.speed > 0:
            self.speed -= 1
        else:
            self.speed = 2
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
                    if x == 39:
                        self.game.end_game()
                        return 0
                    target = (x + 1, y)
                    self.moves = [0, 1, 2]
                case self.down:
                    if y == 39:
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
            if self.game.get_cell(target).get_value() == 2:
                self.game.end_game()
                return 0
            # Set ate before moving, so we don't override the apple cell
            ate = self.game.fruit_check(target)
            self.game.update_board(target, (x, y))
            self.game.remove_available_cells(target)
            if self.next is not None:
                self.next.update((x, y), ate)
            # If snake is last we need to clear the cell, or make a new snake there.
            elif ate:
                self.next = self.game.create_snake((x, y))
                self.game.new_apple()
            else:
                self.game.clear_cell((x, y))
            self.cell = self.game.get_cell(target)

