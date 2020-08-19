# game-of-life
Conway's Game of Life

This is a Python remake of Conway's Game of Life: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

It is a Flask app which uses the Python Imaging Library to convert an uploaded picture to black and white. This creates the seed and board on which the Game of Life is played out.
The image is not saved to any database, and is deleted once the user moves away from the site or uploads a new picture. 

Potential feature: Include Computer Vision bounding boxes which track the various common objects that are found in Conway's' Game of Life.
