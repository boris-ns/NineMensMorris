# Nine Mens Morris
AI/Game written in Python3 that plays Nine Mens Morris. <br />
Game can be player between
* user and user
* user and ai
* ai and ai, but this can run into infinite loop because both players will use same heuristics evaluation

You can change player types by making new objects for player1 and player2 in `main.py.` <br />

### How to play
`python main.py`

# How it works

Game of Nine Mens Morris is divided into 3 phases - placing figures, moving figures and "flying" (Note: "flying" isn't implemented).<br />
Main principle of how this AI works is [the minimax algorithm](http://neverstopbuilding.com/minimax).<br />
AI decides which move is the best based on [heuristics evaluation](https://kartikkukreja.wordpress.com/2014/03/17/heuristicevaluation-function-for-nine-mens-morris/). Heuristics functions for phase 1, phase 2 and "eating" figures are different because they don't use same assessment functions and coefficients.