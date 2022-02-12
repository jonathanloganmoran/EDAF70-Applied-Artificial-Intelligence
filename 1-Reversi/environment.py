import sys
import random
from functools import partial

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.core.window import Window

from game import Game
from search import Minimax


class ReversiApp(App):
    """The Reversi (Othello) simulation environment.
    
    Renders the game board and interacts with user.

    Parameters
    ----------
    App : Kivy object
        Main entry point into the Kivy run loop.

    Returns
    -------
    main_layout : Kivy object
        Container object of all Kivy widgets.
    """

    scores_layout = GridLayout(cols=2, padding=[10])
    main_layout = GridLayout(cols=2, padding=[10])
    menu_layout = BoxLayout(orientation="vertical", padding=[50], spacing=100)
    game_layout = GridLayout(rows=8, cols=8, padding=[30], size_hint_x=0)
    information_label = Label(text="1) Choose your side\n"
                                   "2) Choose opponent type\n"
                                   "3) Start game\n",
                              color=(0,0,0,1))
    white_label = Label(text="White: ", color=(0,0,0,1))
    black_label = Label(text="Black: ", color=(0,0,0,1))
    game_buttons = [[0] * 8 for i in range(8)]
    game = Game(is_othello=True, player_side='X', opponent_type="human", opponent_difficulty=0)

    #----------------------------------------------------------------------------------------------
    # Initialisation Functions:
    # The methods required to set up the game.                                                                      
    #----------------------------------------------------------------------------------------------

    def start_game(self, instance):
        """Starts a new game when app is run, renders game scene and determines the first player."""
        self.game_layout.size_hint_x = 1
        instance.text = "Restart game"
        instance.unbind(on_press=self.start_game)
        instance.bind(on_press=self.restart_game)
        self.game.reset_board()
        self.refresh_board()
        self.update_score()
        self.show_possible_moves()
        self.game.is_initial_move = True
        Window.size = (1100, 600)
        # Opponent goes first if player chose White (Othello rules)
        if self.game.opponent_type == "computer" and self.game.is_othello and self.game.player_side == 'O':
            self.make_move_ai()

    def restart_game(self, instance=None):
        """Reinitialises parameters for a new game."""
        self.game.current_side = 'X'                    # Black moves first in Othello
        self.game.reset_board()
        self.refresh_board()
        self.update_score()
        self.show_possible_moves()
        self.game.is_initial_move = True
        self.game.move_count = 0
        # Opponent goes first if player chose White (Othello rules)
        if self.game.opponent_type == "computer" and self.game.is_othello and self.game.player_side == 'O':
            self.make_move_ai()

    def end_game(self):
        """Displays the final score and winning player if a game has ended."""
        current_score = self.game.calc_score()
        winner = "Black won." if (current_score['X'] > current_score['O']) else "White won."
        self.information_label.text = winner

    def init_human_opponent(self):
        """Initialises the game for a human opponent."""
        self.game.set_opponent_difficulty(0)
        self.menu_layout.remove_widget(self.select_difficulty)
        self.game.set_opponent_type("human")

    def init_ai_opponent(self):
        """Sets the opponent to computer and configures desired difficulty."""
        if self.ai_toggle_shown:
            # Prevent rendering toggle buttons more than once
            self.menu_layout.remove_widget(self.select_difficulty)
        self.game.set_opponent_type("computer")
        self.game.set_opponent_difficulty(1)
        self.select_difficulty = StackLayout()
        self.select_difficulty.add_widget(Label(text="Select difficulty", size_hint=(1, .5)))
        self.difficulty_states = StackLayout()
        self.difficulty_states.allow_no_selection = False
        self.difficulty_states.add_widget(
            ToggleButton(text="Easy", group="difficulty", state="down", size_hint=(.33, .7),
                         on_press=lambda x: self.game.set_opponent_difficulty(1)))
        self.difficulty_states.add_widget(
            ToggleButton(text="Medium", group="difficulty", size_hint=(.33, .7),
                         on_press=lambda x: self.game.set_opponent_difficulty(2)))
        self.difficulty_states.add_widget(
            ToggleButton(text="Hard", group="difficulty", size_hint=(.33, .7),
                         disabled=True,    # Not yet implemented
                         on_press=lambda x: self.game.set_opponent_difficulty(3)))
        self.select_difficulty.add_widget(self.difficulty_states)
        self.menu_layout.add_widget(self.select_difficulty)
        self.ai_toggle_shown = True

    def init_rules(self, is_othello):
        """Sets the desired game rules and restarts the game."""
        self.game.set_rules(is_othello)
        self.restart_game()

    def init_player_side(self, player_side):
        """Sets the user-selected player side and restarts the game."""
        self.game.set_initial_sides(player_side)
        self.restart_game()

    #----------------------------------------------------------------------------------------------
    # Drawing Functions:
    # The methods required to render updates to the game board.                                                                      
    #----------------------------------------------------------------------------------------------

    def build(self):
        """The main entry point into Reversi program.
        Builds the scene elements and game board based on the selected configuration.
        """

        Window.size = (500, 600)
        Window.clearcolor = (1, 1, 1, 1)
        ### Choosing Reversi rule-set
        rule_states = StackLayout()
        rule_states.add_widget(
            ToggleButton(text="Othello", group="rule", state="down", size_hint=(.5, .7),
                         on_press=lambda x: self.init_rules(True)))
        rule_states.add_widget(
            ToggleButton(text="Classic", group="rule", size_hint=(.5, .7),
                         on_press=lambda x: self.init_rules(False)))
        self.menu_layout.add_widget(rule_states)
        ### Choosing player side
        side_states = StackLayout()
        side_states.add_widget(
            ToggleButton(text="Black", group="side", state="down", size_hint=(.5, .7),
                         on_press=lambda x: self.init_player_side('X')))
        side_states.add_widget(
            ToggleButton(text="White", group="side", size_hint=(.5, .7),
                         on_press=lambda x: self.init_player_side('O')))
        self.menu_layout.add_widget(side_states)
        ### Choosing opponent type
        opponent_states = StackLayout()
        opponent_states.add_widget(
            ToggleButton(text="Human", group="opponent", state="down", size_hint=(.5, .7),
                         on_press=lambda x: self.init_human_opponent()))
        self.ai_toggle_shown = False
        opponent_states.add_widget(
            ToggleButton(text="Computer", group="opponent", size_hint=(.5, .7),
                         on_press=lambda x: self.init_ai_opponent()))
        self.menu_layout.add_widget(opponent_states)
        black_player_score = StackLayout()
        black_player_score.add_widget(
            Image(source='assets/images/game/black.png'))
        black_player_score.add_widget(self.black_label)
        white_player_score = StackLayout()
        white_player_score.add_widget(
            Image(source='assets/images/game/white.png'))
        white_player_score.add_widget(self.white_label)
        self.scores_layout.add_widget(black_player_score)
        self.scores_layout.add_widget(white_player_score)
        self.menu_layout.add_widget(self.scores_layout)
        self.menu_layout.add_widget(self.information_label)
        self.menu_layout.add_widget(Button(text="Start game", size_hint=(1, 1), on_press=self.start_game))
        ### Render empty game board buttons
        for i in range(8):
            for j in range(8):
                self.game_buttons[i][j] = Button(size=(65, 65), background_normal="assets/images/game/empty.png",
                                                 on_press=partial(self.make_move_human, i, j))
                                                 # partial for avoiding mutability
                self.game_layout.add_widget(self.game_buttons[i][j])
        self.main_layout.add_widget(self.menu_layout)
        self.main_layout.add_widget(self.game_layout)
        #self.game.reset_board()
        #self.refresh_board()
        return self.main_layout

    def refresh_board(self):
        """Updates the discs shown on the game board after each move."""
        for i in range(8):
            for j in range(8):
                if self.game.board[i][j] == 'X':
                    self.game_buttons[i][j].background_normal = "assets/images/game/black0.png"
                elif self.game.board[i][j] == 'O':
                    self.game_buttons[i][j].background_normal = "assets/images/game/white0.png"
                else:
                    self.game_buttons[i][j].background_normal = "assets/images/game/empty.png"
    
    def show_possible_moves(self):
        """Searches all possible moves and displays them on the game board."""
        possible_moves = self.game.get_valid_moves()
        if len(possible_moves) == 0:
            self.end_game()
        for x, y in possible_moves:
            self.game_buttons[x][y].background_normal = "assets/images/game/possible_move.png"

    #----------------------------------------------------------------------------------------------
    # Logical Functions:
    # The methods required to carry out game logic.                                                                      
    #----------------------------------------------------------------------------------------------

    def update_score(self):
        """Calculates score for each side and shows result to player(s)."""
        current_score = self.game.calc_score()
        current_player = "Current player: " + str(self.game.current_side)
        self.information_label.text = current_player + "\n\n"
        self.black_label.text = "Black: " + str(current_score['X'])
        self.white_label.text = "White: " + str(current_score['O'])
    
    def validate_move(self, position_x, position_y):
        """Checks if the move is legal, then if so, carries out a complete move cycle."""
        is_valid_move = False
        if self.game.is_initial_move and not self.game.is_othello:
            is_valid_move = self.game.check_is_starting_move(position_x, position_y)
        else:
            is_valid_move = self.game.check_is_valid_move(position_x, position_y, True)
        if is_valid_move:
            self.game.board[position_x][position_y] = self.game.current_side
            self.refresh_board()
            self.game.change_side()
            self.update_score()
        else:
            self.information_label.text = "That is not a valid move."
        return is_valid_move

    def get_best_move(self, possible_moves):
        """Searches the list of possible moves and returns the index of the most optimal one."""
        optimal_value = -sys.maxsize if self.game.current_side == 'X' else sys.maxsize
        optimal_move = 0
        for move_idx, move_coordinates in enumerate(possible_moves):
            # Search for best move using Minimax algorithm with alpha-beta pruning
            minimax = Minimax(self.game.board, self.game.player_side, self.game.opponent_type,
                              self.game.current_side)
            if self.game.current_side == 'X':
                current_value = minimax.minimax_with_pruning(move_coordinates)
                # Maximising player objective
                if current_value > optimal_value:
                    optimal_value = current_value
                    optimal_move = move_idx
            else:
                current_value = minimax.minimax_with_pruning(move_coordinates)
                # Minimising player objective
                if current_value < optimal_value:
                    optimal_value = current_value
                    optimal_move = move_idx
            return optimal_move

    def make_move_ai(self):
        """Searches all possible moves and chooses one of them based on Minimax algorithm."""
        possible_moves = self.game.get_valid_moves()
        if len(possible_moves) == 0:
            self.end_game()
        selected_move = sys.maxsize
        if self.game.opponent_difficulty == 1:
            selected_move = random.randint(0, len(possible_moves) - 1)
        elif self.game.opponent_difficulty == 2:
            selected_move = self.get_best_move(possible_moves)
        else:
            self.end_game()
            return NotImplementedError
        self.validate_move(possible_moves[selected_move][0], possible_moves[selected_move][1])
        self.show_possible_moves()

    def make_move_human(self, position_x, position_y, instance):
        """Places disc on board if the desired move is valid then gives next move to opponent."""
        if self.validate_move(position_x, position_y):
            self.game.move_count += 1
            # Check if human players made centre four moves
            if self.game.move_count == 4 and not self.game.is_othello:
                self.game.is_initial_move = False
            elif self.game.move_count == 3 and not self.game.is_othello and self.game.opponent_type == "computer":
                self.game.is_initial_move = False
            #if self.game.is_initial_move:
            #   print(self.game.move_count)
            if self.game.opponent_type == "computer":
                self.make_move_ai()
            else:
                self.show_possible_moves()


if __name__ == "__main__":
    ReversiApp().run()