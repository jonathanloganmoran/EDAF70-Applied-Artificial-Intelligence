import time

TIME_LIMIT = 5          # Max time (in seconds) for AI to make move

def alphabeta_search(self, state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search the game space to determine the best action.

    The game tree is searched using alpha-beta pruning. Moves are selected
    using an evaluation function and a set of heuristics.
    Credit: [AIMA Chapter 6: Games, or Adversarial Search (`games.py`).]
    """

    player = game.to_move(state)
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = float('-infinity')
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = float('infinity')
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                  (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_v = float('-infinity')
    best_a = None
    start_time = time.time()
    # TODO: Cut off search after time limit
    # while time.time() < start_time + TIME_LIMIT:
    for a in game.actions(state):
        # TODO: Update progress bar
        # self.update_progress(time.time())
        v = min_value(state=state, alpha=float('-infinity'), beta=float('infinity'), depth=0)
        if v > best_v:
            best_v = v
            best_a = a
    return best_a
