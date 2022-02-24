import sys
import random
from functools import partial
import time

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.graphics import Rectangle
# TODO: Display progress bar and popup while AI makes move
# from kivy.uix.popup import Popup
# from kivy.uix.progressbar import ProgressBar

from game import Reversi
import search


class Board(App):
    """The Reversi (Othello) simulation environment.

    Renders the game board and interacts with user.

    Parameters
    ----------
        App     Kivy object     Main entry point into the Kivy run loop.
    """
    
    scores_layout = GridLayout(cols=2, padding=[10])
    main_layout = GridLayout(cols=2, padding=[10])
    menu_layout = BoxLayout(orientation="vertical", padding=[50], spacing=100)
    game_layout = GridLayout(rows=8, cols=8, padding=[30], size_hint_x=0)
    information_label = Label(text="1) Choose your side\n"
                                   "2) Choose opponent type\n"
                                   "3) Start game\n",
                              color=(0,0,0,1))
    black_label = Label(text="Black: ", color=(0,0,0,1))
    white_label = Label(text="White: ", color=(0,0,0,1))
    buttons = {}
    game = Reversi(is_othello=True, opponent_type="human", opponent_difficulty=0)
    state = game.initial
    moves_made = 0
    
    #----------------------------------------------------------------------------------------------
    # Initialisation Functions:
    # The methods required to set up the game.                                                                      
    #----------------------------------------------------------------------------------------------

    def start_game(self, instance):
        """Starts a new game and gives opening move to starting player."""
        self.game_layout.size_hint_x = 1
        instance.text = "Restart game"
        instance.unbind(on_press=self.start_game)
        instance.bind(on_press=self.restart_game)
        Window.size = (1100, 600)
        if self.game.opponent_type == "computer" and self.game.is_othello and self.game.player_side == 'O':
            self.make_move_ai()

    def restart_game(self, instance=None):
        """Reinitialises parameters for a new game."""
        self.game = Reversi(is_othello=self.game.is_othello, player_side=self.game.player_side,
                            opponent_type=self.game.opponent_type, opponent_difficulty=self.game.opponent_difficulty)
        self.state = self.game.initial
        self.game.moves_made = 0
        self.update_score()
        self.refresh_board()
        # Opponent goes first if player chose White (Othello)
        if self.game.opponent_type == "computer" and self.game.is_othello and self.game.player_side == 'O':
            self.make_move_ai()

    def end_game(self):
        """Displays the final score and the winning player when game has ended."""
        current_score = self.game.calc_score(self.state.board)
        winner = "Black won." if (current_score['X'] > current_score['O']) else "White won."
        self.information_label.text = winner

    def init_human_opponent(self):
        self.menu_layout.remove_widget(self.select_difficulty)
        self.game.set_opponent_difficulty(0)
        self.menu_layout.remove_widget(self.select_difficulty)
        self.game.set_opponent_type("human")

    def init_ai_opponent(self):
        """Sets the opponent to computer and configures desired difficulty."""
        if self.ai_toggle_selected:
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
                         on_press=lambda x: self.game.set_opponent_difficulty(3)))
        self.select_difficulty.add_widget(self.difficulty_states)
        self.menu_layout.add_widget(self.select_difficulty)
        self.ai_toggle_selected = True

    def init_rules(self, is_othello):
        """Sets the desired game rules and restarts the game."""
        self.game.set_rules(is_othello)
        self.restart_game()

    def init_player_side(self, player_side):
        """Sets the desired player side and restarts the game."""
        self.game.set_initial_sides(player_side)
        self.restart_game()

    #----------------------------------------------------------------------------------------------
    # Logical Functions:
    # The methods required to carry out game logic.                                                                      
    #----------------------------------------------------------------------------------------------
    
    def update_score(self):
        """Calculates score for each side and shows result to player(s)."""
        current_score = self.game.calc_score(self.state.board)
        current_player = "Current player: " + str(self.state.to_move)
        self.information_label.text = current_player + "\n\n"
        self.black_label.text = "Black: " + str(current_score['X'])
        self.white_label.text = "White: " + str(current_score['O'])

    def make_move_ai(self):
        """Searches all possible moves and chooses one of them based on Minimax algorithm."""
        selected_move = sys.maxsize
        # TODO: Display popup window while AI makes move
        # self.show_progress_dialog()
        if self.game.opponent_difficulty == 1:
            rand_move = random.randint(0, len(self.state.moves) - 1)
            selected_move = self.state.moves[rand_move]
        elif self.game.opponent_difficulty == 2:
            selected_move = search.alphabeta_search(self, self.state, self.game, d=2)
        elif self.game.opponent_difficulty == 3:
            selected_move = search.alphabeta_search(self, self.state, self.game)
        else:
            raise NotImplementedError
        self.game.moves_made += 1
        # TODO: Dismiss popup window after AI makes move
        # self.popup_window.dismiss()
        self.state = self.game.result(self.state, selected_move)
        self.update_score()
        self.refresh_board()
        if self.game.terminal_test(self.state):
            self.end_game()

    def make_move_human(self, move, instance):
        """Places disc on board if the desired move is valid then gives next move to opponent."""
        button_clicked = self.buttons[move]
        if button_clicked.state == 'disabled':
            # Ignore invalid moves
            return
        self.game.moves_made += 1
        self.state = self.game.result(self.state, move)
        self.update_score()
        if self.game.terminal_test(self.state):
            self.end_game()
        elif self.game.opponent_type == "computer":
            self.make_move_ai()
        else:
            self.refresh_board()

    #----------------------------------------------------------------------------------------------
    # Drawing Functions:
    # The methods required to render updates to the game board.                                                                      
    #----------------------------------------------------------------------------------------------
    
    def refresh_board(self):
        """Updates the discs shown on the game board after each move."""
        for row in range(1, self.game.height + 1):
            for col in range(1, self.game.width + 1):
                button = self.buttons.get((row, col))
                if (row, col) in self.state.board:
                    button.disabled = True
                    button.background_disabled_normal = "assets/images/game/black0.png" \
                    if self.state.board.get((row, col)) == 'X' \
                    else "assets/images/game/white0.png"
                elif (row, col) in self.state.moves:
                    button.disabled = False
                    button.background_normal = "assets/images/game/possible_move.png"
                else:
                    button.disabled = True
                    button.background_disabled_normal = "assets/images/game/empty.png"
                self.buttons[(row, col)] = button
    
    # TODO: Display progress bar while AI makes move
    def update_progress(self, value):
        """Updates progress bar."""
        pass

    def show_dialog(self):
        """Displays window with progress bar."""
        pass

    def build(self):
        """The main entry point into Reversi program.

        Builds the scene elements and game board based on the selected configuration:
        *           side:    Desired colour of player's discs (i.e. White or Black)
        *  opponent type:    Who the player wants to play against (i.e. Human or Computer)

        Returns
        -------
            main_layout     Kivy object     Main UI window.
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
        self.ai_toggle_selected = False
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
        for row in range(1, self.game.height + 1):
            for col in range(1, self.game.width + 1):
                if (row, col) in self.state.board:
                    button = Button(size=(65, 65), disabled=True,
                        background_disabled_normal="assets/images/game/black0.png"
                        if self.state.board.get((row, col)) == 'X'
                        else "assets/images/game/white0.png",
                        on_press=partial(self.make_move_human, (row, col)))
                elif (row, col) in self.state.moves:
                    button = Button(size=(65, 65), disabled=False,
                        background_normal="assets/images/game/possible_move.png",
                        on_press=partial(self.make_move_human, (row, col)))
                else:
                    button = Button(size=(65, 65), disabled=True,
                        background_disabled_normal="assets/images/game/empty.png",
                        on_press=partial(self.make_move_human, (row, col)))
                self.buttons[(row, col)] = button
                self.game_layout.add_widget(self.buttons[(row, col)])
        self.main_layout.add_widget(self.menu_layout)
        self.main_layout.add_widget(self.game_layout)
        return self.main_layout


if __name__ == '__main__':
    # Start Kivy run loop
    Board().run()
