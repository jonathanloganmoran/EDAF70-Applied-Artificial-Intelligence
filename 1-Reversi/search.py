import copy
from game import Game


class Minimax(object):
	"""
	Implementation of the Minimax algorithm with alpha-beta pruning.
	"""
	game = None
	depth = 0
	max_depth = 20

	def __init__(self, current_state, player_side, opponent_type, current_side):
		self.game = Game(False, copy.deepcopy(current_state), copy.copy(player_side), copy.copy(current_side),
						 copy.copy(opponent_type), 2)    # copy usage to avoid mutability

	def max_alpha_beta(self, current_state, move_coordinates, alpha, beta):
		self.depth += 1
		# Simulate next move
		temp_board = Game(False, copy.deepcopy(current_state.board), copy.copy(current_state.player_side),
						  copy.copy(current_state.current_side), copy.copy(current_state.opponent_type), 2, False)
		temp_board.check_is_valid_move(move_coordinates[0], move_coordinates[1], True)
		temp_board.place_disc(move_coordinates[0], move_coordinates[1], 'X')
		temp_board.change_side()
		possible_moves = temp_board.get_valid_moves()

		# Check if it was the last move
		if len(possible_moves) == 0 or self.depth >= self.max_depth:
			return current_state.calc_score()['X']
		for move in possible_moves:
			# Considers opponent's next-best move, minimises opponent's immediate gain
			score = self.min_alpha_beta(temp_board, move, alpha, beta)
			alpha = max(score, alpha)
			if alpha >= beta:
				return beta
		return alpha

	def min_alpha_beta(self, current_state, move_coordinates, alpha, beta):
		self.depth += 1
		# Simulate next move
		temp_board = Game(False, copy.deepcopy(current_state.board), copy.copy(current_state.player_side),
						 copy.copy(current_state.current_side), copy.copy(current_state.opponent_type), 2, False)
		temp_board.check_is_valid_move(move_coordinates[0], move_coordinates[1], True)
		temp_board.place_disc(move_coordinates[0], move_coordinates[1], 'O')
		temp_board.change_side()
		possible_moves = temp_board.get_valid_moves()

		# Check if it was the last move
		if len(possible_moves) == 0 or self.depth >= self.max_depth:
			return current_state.calc_score()['O']
		for move in possible_moves:
			# Considers player's best move, maximises player's immediate gain
			score = self.max_alpha_beta(temp_board, move, alpha, beta)
			beta = min(score, beta)
			if alpha >= beta:
				return alpha
		return beta

	def minimax_with_pruning(self, move_coordinates):
		if self.game.current_side == 'X':
			return self.max_alpha_beta(self.game, move_coordinates, float('-inf'), float('inf'))
		else:
			return self.min_alpha_beta(self.game, move_coordinates, float('-inf'), float('inf'))
