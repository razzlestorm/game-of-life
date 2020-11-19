# game-of-life
Conway's Game of Life

This is a Python remake of Conway's Game of Life: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

It is a Flask app which uses the Python Imaging Library to convert an uploaded picture to black and white. This creates the seed and board on which the Game of Life is played out.
The image is saved, but the uploaded images are deleted once the heroku instance shuts down.

Potential feature: Include Computer Vision bounding boxes which track the various common objects that are found in Conway's' Game of Life.

# Made With:
* [Brython](https://brython.info/） - This was an experiment with using Brython to run Python in a web browser, and it wasn't bad at all! 

# Deployed at:
This app is currently deployed on [Heroku](pic-game-of-life.herokuapp.com/).

# Current Issues:
* Blurriness in the pixels. This is related to the way HTML Canvas displays what it draws, and led me down a rabbit hole about how browsers display things. If you know of a fix, please let me know, and I'll implement it. I've tried many :D.
* Speed. Images larger than 100x100 pixels are currently rescaled down to 100x100. 

# Future Roadmap:
* Optimize many things for speed.
