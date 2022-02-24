from collections import namedtuple
from collections import Counter

from heuristics import CornerCaptivity
from heuristics import CoinParity
from heuristics import Mobility


GameState = namedtuple('GameState', 'to_move, utility, board, moves')
board = {}


class Game:
    """
    A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement
    legal_moves, make_move, utility, and terminal_test. You may
    override display and successors or you can inherit their default
    methods. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor.

    Credit: [AIMA Chapter 6 - Russell and Norvig, 2010]
    """

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
        raise NotImplementedError

    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
        raise NotImplementedError

    def utility(self, state, player):
        "Return the value of this final state to player."
        raise NotImplementedError

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print(state)

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(move, state))
                for move in self.legal_moves(state)]

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def play_game(self, move, state):
        """Play an n-person move-alternating game."""
        new_state = self.result(state, move)
        return new_state


class Reversi(Game):
    """
    The Reversi game engine. Based on [Figure 5.2 - AIMA, Russell and Norvig (2010)].

    This class implements the following game functions:
    *  Reversi board initialisation;
    *  Player turn-taking;
    *  Valid move checking;
    *  Disc flipping;
    *  Score calculation.
    """

    def __init__(self, is_othello=False, player_side='X', opponent_type='human',
                 opponent_difficulty=0, is_initial=False, height=8, width=8, board={}, moves_made=0):
        """Initialises the game board with or without the default (Othello) starting pieces."""
        board = board
        self.height = height
        self.width = width
        self.is_othello = is_othello
        self.player_side = player_side
        self.opponent_side = 'O' if self.player_side == 'X' else 'X'
        self.opponent_type = opponent_type
        self.opponent_difficulty = opponent_difficulty
        self.is_initial = is_initial
        self.moves_made = moves_made
        if self.is_othello:
            board = self.put_initial_discs()
        elif self.moves_made > 3:
            self.is_initial = False
        else:
            self.is_initial = True
        self.initial = GameState(
            to_move='X' if self.is_othello else self.player_side,
            utility=0, 
            board=board, 
            moves=self.get_valid_moves(board, 'X' if self.is_othello else self.player_side))

    @staticmethod
    def put_initial_discs():
        """Resets the board representation with Othello opening moves."""
        black_discs = dict.fromkeys([(4, 5), (5, 4)], 'X')
        white_discs = dict.fromkeys([(4, 4), (5, 5)], 'O')
        board = {**black_discs, **white_discs}
        return board

    def set_initial_sides(self, player_side='X'):
        """Initialises the player and opponent disc colours."""
        self.player_side = player_side
        self.opponent_side = 'O' if player_side == 'X' else 'X'

    def set_rules(self, is_othello):
        self.is_othello = is_othello

    def set_opponent_type(self, opponent_type):
        self.opponent_type = opponent_type

    def set_opponent_difficulty(self, opponent_difficulty):
        self.opponent_difficulty = opponent_difficulty

    def reset_board(self):
        """Removes all discs from board and initialises starting moves."""
        self.board = {}
        if self.is_othello:
            self.put_initial_discs()
        self.initial = GameState(
            to_move='X' if self.is_othello else self.player_side, 
            utility=0, 
            board=board, 
            moves=self.get_valid_moves(board, 'X' if self.is_othello else self.player_side))
        return GameState(
            to_move='X' if self.is_othello else self.player_side, 
            utility=0, 
            board=board, 
            moves=self.get_valid_moves(board, 'X' if self.is_othello else self.player_side))

    @staticmethod
    def is_on_board(x_coordinate, y_coordinate):
        return 1 <= x_coordinate <= 8 and 1 <= y_coordinate <= 8
    
    @staticmethod
    def is_in_centre(move):
        x, y = move
        return 4 <= x <= 5 and 4 <= y <= 5

    @staticmethod
    def flank_opponent(board, move, player, direction):
        """Flank opponent disc(s) to the current player's side."""
        opponent = 'O' if player == 'X' else 'X'
        (x_direction, y_direction) = direction
        x, y = move
        x, y = x + x_direction, y + y_direction
        flank_positions = []
        while board.get((x, y)) == opponent:
            flank_positions.append((x, y))
            x, y = x + x_direction, y + y_direction
        if board.get((x, y)) != player:
            del flank_positions[:]
        # Move in opposite direction
        x, y = move
        x, y = x - x_direction, y - y_direction
        other_flank_positions = []
        while board.get((x, y)) == opponent:
            other_flank_positions.append((x, y))
            x, y = x - x_direction, y - y_direction
        if board.get((x, y)) != player:
            del other_flank_positions[:]
        return flank_positions + other_flank_positions

    def valid_move(self, board, move, player):
        """Checks if the desired move is valid.

        A valid move satisfies the following conditions:
        *  Position (x, y) is within the board bounds;
        *  Position (x, y) is empty;
        *  Position (x, y) can flank the opponent.
        """

        if self.is_initial and not self.is_othello:
            return self.is_in_centre(move)
        else:
            return self.flank_opponent(board, move, player, (0, 1)) \
                 + self.flank_opponent(board, move, player, (1, 0)) \
                 + self.flank_opponent(board, move, player, (1, -1)) \
                 + self.flank_opponent(board, move, player, (1, 1))

    def get_valid_moves(self, board, player):
        """Searches the board for possible valid moves and returns a list of their coordinates."""
        return [(x, y) for x in range(1, self.width + 1)
                       for y in range(1, self.height + 1)
                       if (x, y) not in board.keys() 
                       and self.valid_move(board, (x, y), player)]

    def calc_score(self, board):
        black_score = Counter(board.values())['X']
        white_score = Counter(board.values())['O']
        return {'X': black_score, 'O': white_score}

    def actions(self, state):
        """Legal moves are any valid square that is not yet taken and can flank the opponent's discs."""
        return state.moves

    def result(self, state, move):
        """Returns the state that results from make a move from a state."""
        if move not in state.moves:
            return state
        if self.moves_made == 4 and not self.is_othello:
            self.is_initial = False
        opponent = 'X' if state.to_move == 'O' else 'O'
        board = state.board.copy()
        # Update position with disc
        board[move] = state.to_move
        # Flank all opponent discs captured by player's move
        if not self.is_initial:
            for opponent_disc in self.valid_move(board, move, state.to_move):
                board[opponent_disc] = state.to_move
        # Get set of possible moves for next player
        valid_moves = self.get_valid_moves(board, opponent)
        return GameState(to_move=opponent,
                         utility=self.compute_utility(board, valid_moves, state.to_move),
                         board=board,
                         moves=valid_moves)

    def utility(self, state, player):
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        return len(state.moves) == 0

    def compute_utility(self, board, moves, player):
        # End of game, return utility
        if len(moves) == 0:
            return 100 if player == 'X' else -100
        elif self.opponent_difficulty == 3 and not self.is_initial:
            return 0.7 * CornerCaptivity().get_score(board, player) \
                 + 0.2 * Mobility().get_score(self, board, player)  \
                 + 0.1 * CoinParity().get_score(board, player)
        else:
            return self.calc_score(board)[player]




