import unittest
from game2 import Reversi
from heuristics import CornerCaptivity
from heuristics import CoinParity
from heuristics import Mobility


class TestCornerHeuristic(unittest.TestCase):

    def test_corner_player(self):
        """Evaluates score returned for player in upper left corner."""
        player_corner = dict.fromkeys([(1, 1)], 'X')
        opponent_corner = {}
        board = {**player_corner, **opponent_corner}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        corner_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect +25 for player in corner (+25 per player corner)
        self.assertEqual(corner_score, 25)

    def test_corner_opponent(self):
        """Evaluates score returned for opponent in upper left corner."""
        player_corner = {}
        opponent_corner = dict.fromkeys([(1, 1)], 'O')
        board = {**player_corner, **opponent_corner}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        corner_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect -25 for opponent in corner (-25 per opponent corner)
        self.assertEqual(corner_score, -25)

    def test_corners_player(self):
        """Evaluates score returned for player in upper right and lower left corners."""
        player_corner = dict.fromkeys([(8, 8), (1, 8)], 'X')
        opponent_corner = {}
        board = {**player_corner, **opponent_corner}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        corner_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect +50 for player in corners (+25 per player corner)
        self.assertEqual(corner_score, 50)

    def test_corners_opponent(self):
        """Evaluates score returned for opponent in upper right and lower left corners."""
        player_corner = {}
        opponent_corner = dict.fromkeys([(8, 8), (1, 8)], 'O')
        board = {**player_corner, **opponent_corner}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        corner_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect -50 for opponent in corners (-25 per opponent corner)
        self.assertEqual(corner_score, -50)

    def test_corners_equal(self):
        """Evaluates score returned for one player, one opponent corner."""
        player_corner = dict.fromkeys([(1, 8)], 'X')
        opponent_corner = dict.fromkeys([(8, 8)], 'O')
        board = {**player_corner, **opponent_corner}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        corner_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect 0 for opponent in corner (-25) and player in corner (+25)
        self.assertEqual(corner_score, 0)


class TestAdjacentCornerHeuristic(unittest.TestCase):

    def test_adjacent_player(self):
        """Evaluates score for player not in upper left corner but in one of its adjacent square."""
        player_corner = {}
        player_adjacent = dict.fromkeys([(2, 1)], 'X')
        opponent_corner = {}
        opponent_adjacent = {}
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect -8 for player not in corner but in adjacent square (-8.33 per adjacent)
        self.assertEqual(adjacent_score, -8)

    def test_two_adjacents_player(self):
        """Evaluates score for player not in upper left corner but in two of its adjacent square."""
        player_corner = {}
        player_adjacent = dict.fromkeys([(2, 1), (1, 2)], 'X')
        opponent_corner = {}
        opponent_adjacent = {}
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect -17 for player not in corner but in adjacent squares (-8.33 per adjacent)
        self.assertEqual(adjacent_score, -17)

    def test_three_adjacents_player(self):
        """Evaluates score for player not in upper left but in all three adjacent squares."""
        player_corner = {}
        player_adjacent = dict.fromkeys([(2, 1), (1, 2), (2, 2)], 'X')
        opponent_corner = {}
        opponent_adjacent = {}
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect -25 for player not in corner but in adjacent squares (-8.33 per adjacent)
        self.assertEqual(adjacent_score, -25)

    def test_corner_player_adjacents_player(self):
        """Evaluates score for player in upper left corner but in one of its adjacent squares."""
        player_corner = dict.fromkeys([(1, 1)], 'X')
        player_adjacent = dict.fromkeys([(2, 1), (1, 2), (2, 2)], 'X')
        opponent_corner = {}
        opponent_adjacent = {}
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect +25 for player in one corner (no adjacent penalty if corner is occupied by player)
        self.assertEqual(adjacent_score, 25)

    def test_adjacent_opponent(self):
        """Evaluates score for opponent in adjacent square."""
        player_corner = {}
        player_adjacent = {}
        opponent_corner = {}
        opponent_adjacent = dict.fromkeys([(1, 2)], 'O')
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect +8 for opponent in adjacent (+8.33 per opponent adjacent)
        self.assertEqual(adjacent_score, 8)

    def test_two_adjacents_opponent(self):
        """Evaluates score for opponent in adjacent square."""
        player_corner = {}
        player_adjacent = {}
        opponent_corner = {}
        opponent_adjacent = dict.fromkeys([(1, 2), (2, 1)], 'O')
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect +17 for opponent in adjacents (+8.33 per opponent adjacent)
        self.assertEqual(adjacent_score, 17)

    def test_three_adjacents_opponent(self):
        """Evaluates score for opponent in adjacent square."""
        player_corner = {}
        player_adjacent = {}
        opponent_corner = {}
        opponent_adjacent = dict.fromkeys([(1, 2), (2, 1), (2, 2)], 'O')
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect +25 for opponent in adjacents (+8.33 per opponent adjacent)
        self.assertEqual(adjacent_score, 25)

    def test_adjacent_equal(self):
        """Evaluates score for player and opponent not in corners but in adjacent squares."""
        player_corner = {}
        player_adjacent = dict.fromkeys([(2, 1)], 'X')
        opponent_corner = {}
        opponent_adjacent = dict.fromkeys([(1, 2)], 'O')
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect 0, +8 for opponent and -8 for player in adjacents (+/-8.33 per adjacent)
        self.assertEqual(adjacent_score, 0)

    def test_corner_player_adjacent_opponent(self):
        """Evaluates score for player in corner and opponent in adjacent squares."""
        player_corner = dict.fromkeys([(1, 1)], 'X')
        player_adjacent = {}
        opponent_corner = {}
        opponent_adjacent = dict.fromkeys([(2, 1), (1, 2), (2, 2)], 'O')
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect +25 for player in corner (no adjacent penalty if corner is occupied by player)
        self.assertEqual(adjacent_score, 25)

    def test_corner_opponent_adjacent_player(self):
        """Evaluates score for opponent in corner and player in adjacent squares."""
        player_corner = {}
        player_adjacent = dict.fromkeys([(2, 1), (1, 2), (2, 2)], 'X')
        opponent_corner = dict.fromkeys([(1, 1)], 'O')
        opponent_adjacent = {}
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect -25 for opponent in corner (no adjacent score if corner is occupied by opponent)
        self.assertEqual(adjacent_score, -25)

    def test_corner_player_adjacent_player(self):
        """Evaluates score for player in corner and player in adjacent squares."""
        player_corner = dict.fromkeys([(1, 1)], 'X')
        player_adjacent = dict.fromkeys([(2, 1), (1, 2), (2, 2)], 'X')
        opponent_corner = {}
        opponent_adjacent = {}
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect +25 for player in corner (no adjacent penalty if corner is occupied by player)
        self.assertEqual(adjacent_score, 25)

    def test_corner_opponent_adjacent_opponent(self):
        """Evaluates score for opponent in corner and opponent in adjacent squares."""
        player_corner = {}
        player_adjacent = {}
        opponent_corner = dict.fromkeys([(1, 1)], 'O')
        opponent_adjacent = dict.fromkeys([(2, 1), (1, 2), (2, 2)], 'O')
        board = {**player_corner, **player_adjacent, **opponent_corner, **opponent_adjacent}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        adjacent_score = CornerCaptivity().get_score(state.board, state.to_move)
        # Expect -25 for opponent in corner (no adjacent penalty if corner is occupied by opponent)
        self.assertEqual(adjacent_score, -25)


class TestCoinParityHeuristic(unittest.TestCase):

    def test_coin_parity_player(self):
        """Evaluates score for player with one move, opponent with none."""
        player_moves = dict.fromkeys([(4, 5)], 'X')
        opponent_moves = {}
        board = {**player_moves, **opponent_moves}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        parity_score = CoinParity().get_score(state.board, state.to_move)
        # Expect +100 for player (100% more moves made by player)
        self.assertEqual(round(parity_score), 100)

    def test_coin_parity_player_2(self):
        """Evaluates score for player with two moves, opponent with one."""
        player_moves = dict.fromkeys([(4, 4), (5, 5)], 'X')
        opponent_moves = dict.fromkeys([(4, 5)], 'O')
        board = {**player_moves, **opponent_moves}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        parity_score = CoinParity().get_score(state.board, state.to_move)
        # Expect +33 (~33.33) for player (1/3 more moves made by player)
        self.assertEqual(round(parity_score), 33)

    def test_coin_parity_opponent(self):
        """Evaluates score for opponent with one move, player with none."""
        player_moves = {}
        opponent_moves = dict.fromkeys([(4, 5)], 'O')
        board = {**player_moves, **opponent_moves}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        parity_score = CoinParity().get_score(state.board, state.to_move)
        # Expect -100 for player (100% more moves made by opponent)
        self.assertEqual(round(parity_score), -100)

    def test_coin_parity_opponent_2(self):
        """Evaluates score for opponent with two moves, player with one."""
        player_moves = dict.fromkeys([(4, 5)], 'X')
        opponent_moves = dict.fromkeys([(4, 4), (5, 5)], 'O')
        board = {**player_moves, **opponent_moves}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        parity_score = CoinParity().get_score(state.board, state.to_move)
        # Expect -33 for player (1/3 more moves made by opponent)
        self.assertEqual(round(parity_score), -33)

    def test_coin_parity_equal(self):
        """Evaluates score for player with two moves, opponent with two."""
        player_moves = dict.fromkeys([(4, 4), (5, 5)], 'X')
        opponent_moves = dict.fromkeys([(4, 5), (5, 4)], 'O')
        board = {**player_moves, **opponent_moves}
        game = Reversi(board=board)
        state = game.initial
        # Get utility for player
        parity_score = CoinParity().get_score(state.board, state.to_move)
        # Expect 0 for player (equal number of moves between players)
        self.assertEqual(parity_score, 0)


class TestMobilityHeuristic(unittest.TestCase):

    def test_mobility_player(self):
        """Evaluates score for player on move with player advantage."""
        black = [(5, 4), (5, 5), (6, 5)]
        white = [(4, 4), (5, 4), (6, 4), (5, 6), (6, 6)]
        player_moves = dict.fromkeys(black, 'X')
        opponent_moves = dict.fromkeys(white, 'O')
        board = {**player_moves, **opponent_moves}
        game = Reversi(is_othello=False, player_side='X', is_initial=False, board=board)
        state = game.initial
        # Get utility for player
        mobility_score = Mobility().get_score(game, state.board, state.to_move)
        # Expect +50 for player (50% more moves possible for player, 9 player : 3 opponent)
        self.assertEqual(mobility_score, 50)

    def test_mobility_opponent(self):
        """Evaluates score for player on move with opponent advantage."""
        black = [(4, 4), (5, 4), (6, 4), (5, 6), (6, 6)]
        white = [(5, 4), (5, 5), (6, 5)]
        player_moves = dict.fromkeys(black, 'X')
        opponent_moves = dict.fromkeys(white, 'O')
        board = {**player_moves, **opponent_moves}
        game = Reversi(is_othello=False, player_side='X', is_initial=False, board=board)
        state = game.initial
        # Get utility for player
        mobility_score = Mobility().get_score(game, state.board, state.to_move)
        # Expect -50 for player (50% more moves possible for opponent, 3 player : 9 opponent)
        self.assertEqual(mobility_score, -50)

    def test_mobility_equal(self):
        """Evaluates score for player on move with equal advantage."""
        game = Reversi(is_othello=True, player_side='X', is_initial=False, moves_made=4)
        state = game.initial
        # Get utility for player
        mobility_score = Mobility().get_score(game, state.board, state.to_move)
        # Expect 0, both players have equal mobility at start of game
        self.assertEqual(mobility_score, 0)


if __name__ == '__main__':
    unittest.main()