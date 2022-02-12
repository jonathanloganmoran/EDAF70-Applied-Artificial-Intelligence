# Assignment 1: The Reversi Game
## Playing Reversi (Othello) With An AI Opponent
#### By Jonathan L. Moran (jo6155mo-s@student.lu.se) and Oleksii Shupikov (ol5180sh@student.lu.se)
From the EDAF70 - Applied Artificial Intelligence course given at Lunds Tekniska Högskola (LTH) | Vt1 2019.

## File Descriptions

Filename           | Description
-------------------|---------------------------------------------------------------------------------------
`environment.py`   | GUI implementation in Kivy; main entry point into Reversi program.             
`game.py`          | Reversi/Othello logic (turn taking, score reporting, move validation, etc).
`search.py`        | AI opponent algorithms (Minimax with alpha-beta pruning).


## Gameplay
### Introduction
[Reversi](https://en.wikipedia.org/wiki/Reversi) is a game played on an 8x8 board between two players– "Black" and "White". The objective of the game is to maximise the number of pieces ("discs") on the board belonging to a given player. Consequently, each player must make moves that attempt to minimise the number of their opponent's discs on the board. Each turn consists of making a single move that reverses ("flanks") _one or more_ of their opponent's discs. If no such move exists, the player forfeits their turn. To flank a disc(s), a player must surround a row, column or diagonal of opponent discs with two discs of their own colour. For example,

![Figure 1. Flanking demonstration - before White moves.](assets/images/wiki/Reversi-Figure-1.png)

the above configuration allows White to place their next disc in an open position that surrounds the three adjacent Black discs.

![Figure 2. Flanking demonstration - after White moves.](assets/images/wiki/Reversi-Figure-2.png)

The resulting move, shown above, flanks the three Black discs into White.


When the board is filled, or no other valid moves are available for either player, the game ends. The player with the most discs on the board wins.

**Fun fact**: A 1978 computerised version of Othello titled [Computer Othello](https://nintendo.fandom.com/wiki/Computer_Othello) was the first ever video game both developed and published by Nintendo.


### Reversi vs. Othello
Two popular variations of the game exist: Reversi ("classic") and Othello. While the gameplay and objective remain the same with either version, Othello places two additional restrictions at the start of the game. The first important distinction is that Othello fixes Black as the starting player. In classic Reversi, the players have the freedom to choose who makes the first move (which is usually decided with a coin toss). The other distinction is that Othello begins the game with the centre four squares already occupied in an diagonal pattern (alternating colours on the top and bottom rows). Reversi lets players place their starting discs in any configuration within the centre four squares.


### Starting a game
Once the dependencies are installed, run `python environment.py` inside the project directory to start the GUI.

If you receive into an error, make sure that `kivy` framework is installed (`pip install kivy`).

When you've successfully started the game (after selecting rule set, player side, opponent type/difficulty), you should see the following:

![Figure 3. The Othello game board – opening moves.](assets/images/wiki/Reversi-Figure-3.png). 

If so – congrats! You're all set to play 🎉


## AI Opponent Strategy
This program supports three "computer" difficulty modes (AI strategies):
   1. **Easy**: random choice;
   2. **Medium**: best move calculation using Minimax adversarial search with alpha-beta pruning;
   ~~3. **Hard**: best move calculation (using _Medium_ strategy), but with heuristic function evaluation.~~

### Random choice
When **Easy** is selected, the AI opponent is configured with a very basic random move evaluator.
*  Any valid move is chosen at random from the list of moves returned by `get_valid_moves()`.

### Best move (without heuristics)
When **Medium** is selected, the AI opponent chooses the "best" available move returned by `get_best_move()`.

The Minimax adversarial search algorithm recursively examines all possible board configurations (_states_) in a game tree. Each state in the tree is connected and reachable by executing a move. The `minimax_with_pruning()_` algorithm finds the next most optimal move in the game by looking a fixed number of moves ahead in the game tree.

*  `minimax_with_pruning()` recursively examines all possible game states following a move of the opponent (`depth` is the number of move iterations);
*  Calculates the best move by _minimising_ the opponent's immediate gain (number of discs flipped on next move).

Alpha-beta pruning is an optimisation applied to the Minimax algorithm which allows us to discard (_prune_) particular moves in the game tree that are said with certainty to be suboptimal. This grants us the ability to look more moves ahead in the game without compromising runtime [2].
*  `alpha`: best already-explored move along path to the root for the player (the _maximiser_).
*  `beta`: best already-explored move along path to the root for the opponent (the _minimiser_).
The recursive algorithm gracefully exits when a legal move satisfying `alpha >= beta` has been found.

### Best move (with heuristics)
_Not yet implemented._


## Future Implementations
-[x] Support for classic Reversi rule set
-[x] Improve GUI design and functionality
-[ ] Refactor codebase (AIMA `Game` class)
-[ ] Heuristic-based evaluation
-[ ] Improve performance (e.g., transposition table, move ordering)
-[ ] Implement Monte Carlo Tree Search (MCTS)

## Credits
This assignment was prepared by J. Malec et al., VT1 2019 (link [here](https://web.archive.org/web/20190514105836/http://cs.lth.se/edaf70/programming-assignments-2019/search/)).

*  Stuart, R. and Norvig, P. (2010). Artificial Intelligence: A Modern Approach. 3rd ed. Englewood Cliffs: Prentice-Hall, pp.167-174. (what's covered: alpha-beta evaluation fn, cutoff-test)

*  _Paradigms of Artificial Intelligence_, Peter Norvig (Ch. 18).

*  [1] Github - Rahul Arya (https://github.com/rahularya50/reversi).

Helpful explanations:
*  [Algorithms Explained - minimax and alpha-beta pruning](https://www.youtube.com/watch?v=l-hh51ncgDI).
*  [Step by Step: Alpha Beta Pruning](https://www.youtube.com/watch?v=xBXHtz4Gbdo).
*  [Thomas Wolf: The Anatomy of a Game Program](http://home.datacomm.ch/t_wolf/tw/misc/reversi/html/index.html).

