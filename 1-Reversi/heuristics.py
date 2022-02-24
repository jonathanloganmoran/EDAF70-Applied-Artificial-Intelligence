import math


class CornerCaptivity:
    """Evaluates the number of corners and their adjacent squares occupied by a given player.
    Each of the four corners on the board are given equal weight (+25 pts per occupied square).
    Each of the four corners' three adjacent squares have negative weight (-8 pts per occupied square).
    """

    def disc_value(self, position, player):
        if position not in ['X', 'O']:
            return 0.0
        elif position == player:
            return 1.0
        else:
            return -1.0

    def adjacent_score(self, board, player, adjacent_locs):
        """Returns negative score for player-occupied adjacent squares."""
        score = 0.0
        adjacent = [board.get(adjacent_locs[0]), board.get(adjacent_locs[1]), board.get(adjacent_locs[2])]
        for adj in adjacent:
            score += self.disc_value(adj, player)
        return score * -33.33

    def corner_score(self, board, player, corner, adjacent_locs):
        """Returns weighted score if player is occupying a corner or its adjacent squares."""
        total = 0.0
        in_corner = board.get((corner))
        if in_corner not in ['X', 'O']:
            total = self.adjacent_score(board, player, adjacent_locs)
        else:
            total = 100.0 * self.disc_value(in_corner, player)
        total *= 0.25
        return round(total)

    def get_score(self, board, player):
        """This heuristic evaluates corners captured and gives negative weight to occupied adjacent squares."""
        c1 = self.corner_score(board, player, (1, 1), [(2, 1), (1, 2), (2, 2)])
        c2 = self.corner_score(board, player, (8, 1), [(7, 1), (8, 2), (7, 2)])
        c3 = self.corner_score(board, player, (1, 8), [(1, 7), (2, 7), (3, 8)])
        c4 = self.corner_score(board, player, (8, 8), [(8, 7), (7, 7), (7, 8)])
        return c1 + c2 + c3 + c4

class CoinParity:
    """This heuristic measures the difference in coins between players."""
    def get_score(self, board, player):
        opponent = 'O' if player == 'X' else 'X'
        return 100 * (sum(v == player for v in board.values()) - \
                      sum(v == opponent for v in board.values()) \
                     ) / len(board.values())
class Mobility:
    """This heuristic measures the difference in available moves between players."""
    def get_score(self, game, board, player):
        """Returns immediate mobility score."""
        game.is_initial = False
        opponent = 'O' if player == 'X' else 'X'
        player_moves = len(game.get_valid_moves(board, player))
        opponent_moves = len(game.get_valid_moves(board, opponent))
        if (player_moves + opponent_moves) != 0:
            return 100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)
        else:
            return 0