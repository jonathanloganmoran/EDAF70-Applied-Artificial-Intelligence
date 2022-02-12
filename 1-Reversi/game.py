class Game(object):
    """
    The Reversi game engine (logic).
    """
    board = [[''] * 8 for i in range(8)]
    player_side = 'O'
    current_side = 'X'
    opponent_type = "human"
    is_initial_move = True

    def __init__(self, is_othello=True, board=None, player_side='O', current_side='X',
                 opponent_type="human", opponent_difficulty=0, is_initial_move=False):
        """Initialises the game board with or without the default (Othello) starting pieces."""
        if board is None:
            board = [[''] * 8 for i in range(8)]
        self.board = board
        self.player_side = player_side
        self.current_side = current_side
        self.opponent_type = opponent_type
        self.is_othello = is_othello
        self.opponent_difficulty = opponent_difficulty
        self.is_initial_move = is_initial_move
        self.move_count = 0

    #----------------------------------------------------------------------------------------------
    # Initialisation Functions:
    # The methods required to set up the game.                                                                      
    #----------------------------------------------------------------------------------------------

    def set_rules(self, is_othello):
        self.is_othello = is_othello

    def set_initial_discs(self):
        """Puts starting discs at the centre of the board according to the Othello rules."""
        if self.is_othello:
            self.board[3][3] = 'O'
            self.board[3][4] = 'X'
            self.board[4][3] = 'X'
            self.board[4][4] = 'O'

    def set_initial_sides(self, player_side='X'):
        """Changes player side before game starts."""
        self.player_side = player_side
        self.opponent_side = 'O' if player_side == 'X' else 'X'
        if self.player_side == 'X' and not self.is_othello:
            # Starting player, any move on board is valid
            self.is_initial_move = True

    def set_opponent_type(self, opponent_type):
        """Sets opponent type before game starts."""
        self.opponent_type = opponent_type
  
    def set_opponent_difficulty(self, opponent_difficulty):
        self.opponent_difficulty = opponent_difficulty
    
    #----------------------------------------------------------------------------------------------
    # Logical Functions:
    # The methods required to carry out game logic.                                                                      
    #----------------------------------------------------------------------------------------------

    def calc_score(self):
        """Calculate the current score for both players by counting discs of each colour)."""
        sides_scores = {'X': 0, 'O': 0}
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'X':
                    sides_scores['X'] += 1
                elif self.board[i][j] == 'O':
                    sides_scores['O'] += 1
        return sides_scores

    def change_side(self):
        """Switch players after a move."""
        self.current_side = 'X' if self.current_side == 'O' else 'O'

    def reset_board(self):
        """Restart the game by removing all discs from the board."""
        self.board = [[''] * 8 for i in range(8)]
        # Place initial discs if playing with Othello rules
        self.set_initial_discs()

    def place_disc(self, x, y, value):
        """Set [x,y] position on the board to the current disc value."""
        self.board[x][y] = value

    def get_valid_moves(self):
        """Searches the board for possible valid moves and returns a list of their coordinates."""
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.check_is_valid_move(i, j):
                    valid_moves.append([i, j])                
                # Check if position is in centre four and not occupied (if starting with Reversi rules)
                elif self.is_initial_move and not self.is_othello and self.check_is_starting_move(i, j):
                    valid_moves.append([i, j])
                
        return valid_moves

    @staticmethod
    def on_board(x_coordinate, y_coordinate):
        """Performs input validation on [x,y] coordinates to make sure they are within bounds."""
        return 0 <= x_coordinate <= 7 and 0 <= y_coordinate <= 7

    def flip_discs(self, initial_x, initial_y, x, y, x_direction, y_direction):
        """Flip opponent discs to the current player's side."""
        discs_to_flip = []
        while True:
            x -= x_direction
            y -= y_direction
            if x == initial_x and y == initial_y:
                break
            discs_to_flip.append([x, y])
        for x, y in discs_to_flip:
            self.board[x][y] = self.current_side

    def check_is_starting_move(self, position_x, position_y):
        """Checks that desired position is a valid starting move i.e. in centre four."""
        starting_locations = [[3, 3], [3, 4], [4, 3], [4, 4]]
        if self.board[position_x][position_y] not in ['X', 'O']:
            if [position_x, position_y] in starting_locations:
                return True

    def check_is_valid_move(self, position_x, position_y, flip_disc=False):
        """Checks if the desired move is valid.

        A valid move satisfies the following conditions:
        *  position [x,y] is within the board bounds
        *  position [x,y] is empty
        """
        
        directions = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        valid_move = False
        # Check if tile is empty and move is legal
        if self.board[position_x][position_y] not in ['X', 'O']:
            current_opponent_disc = 'X' if self.current_side == 'O' else 'O'
            # Check if move is legal
            for x_direction, y_direction in directions:
                x, y = [position_x + x_direction, position_y + y_direction]
                opponent_found = False
                if not Game.on_board(x, y):
                    continue
                opponent_placeholder = self.board[x][y]
                # Loop through all neighbouring tiles if they contain opponent disc
                while opponent_placeholder == current_opponent_disc:
                    opponent_found = True
                    x, y = [x + x_direction, y + y_direction]
                    if not Game.on_board(x, y):
                        break
                    opponent_placeholder = self.board[x][y]
                # Flip all opponent discs between player move
                if opponent_placeholder == self.current_side and opponent_found:
                    if flip_disc:
                        self.flip_discs(position_x, position_y, x, y, x_direction, y_direction)
                    valid_move = True
        return valid_move
