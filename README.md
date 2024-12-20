# Snake
Retro Snake game, using pygame. Used to continue my refresher of Python and learning of Pygame.

### December 19 update:
Game is now focused on a grid of available cells, which handle the drawing and storage of info. The snake movement is still in its own class, 
and cleanup is needed, but everything is working as intended. Will handle menus and scoreboards and things next.

*********************************************************************************************

Early today I fixed the snake growing and updating - kind of. It updates, but because it isnt bound to a proper grid, the movement is WONKY. 
I think I officially need to structure a grid, and bind things to the center of a cell, rather than trying to figure out the coordinate system with math.
The cell could be decided by the screen size (game could always be, say, 50x50, and a larger game space just means each cell is larger).
This is in line with what I need for deciding the next apple location, as it needs to be in an unoccupied cell. It might make sense for the Board to be a part of the Game class
and have it store this object, that has a unique draw function? Like we draw the board cell by cell. Empty cells do nothing (check for cell value is not None) and other cells
call the cell values draw function. 

### December 18 update:
Initial code is in. Thought process was store snake body in Sprite Group for collisions, and a linked list for updates. The movement isnt quite what I want,
and I think part of that is it is moving very freely. It also looks like the apple isn't quite in line with the snakes movement.

I may want to actually make the game store a grid, and this is what contains the snake, apple, free spaces. It would make it much easier to scale to different
window sizes, and hopefully make it easier to decide whats currently busy for respawning apples. It would also let me update the snake, hopefully, a little easier.

Basically - a list of a list of sprites. Would allow me to check for collisions by seeing if the zone is empty, and bind me to forward mvoement
