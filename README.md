# Snake
Retro Snake game, using pygame. Used to continue my refresher of Python and learning of Pygame.

### December 18 update:
Initial code is in. Thought process was store snake body in Sprite Group for collisions, and a linked list for updates. The movement isnt quite what I want,
and I think part of that is it is moving very freely. It also looks like the apple isn't quite in line with the snakes movement.

I may want to actually make the game store a grid, and this is what contains the snake, apple, free spaces. It would make it much easier to scale to different
window sizes, and hopefully make it easier to decide whats currently busy for respawning apples. It would also let me update the snake, hopefully, a little easier.

Basically - a list of a list of sprites. Would allow me to check for collisions by seeing if the zone is empty, and bind me to forward mvoement
