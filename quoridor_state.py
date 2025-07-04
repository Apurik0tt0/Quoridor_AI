import copy
from Q20 import Quoridor

class QuoridorState:
    def __init__(self, game: Quoridor):
        self.game = copy.deepcopy(game)  # on fait une copie pour ne pas modifier l'état original

#return a list of possible moves
    def get_legal_actions(self):
        return self.game.get_legal_moves()

#apply a move and return the new state
    def move(self, action):
        new_game = copy.deepcopy(self.game)
        if action[0] in ['U', 'D', 'L', 'R']:
            new_game.move_player(action)
        else:
            new_game.place_wall(action)
        return QuoridorState(new_game)
    
#during the rollout phase (no copy of the state)
    def move_inplace(self, action):
        if action[0] in ['U', 'D', 'L', 'R']:
            self.game.move_player(action)
        else:
            self.game.place_wall(action)
    
#return if the state is a terminal state
    def is_game_over(self):
        return self.game.game_over

#return the winner of the game (-1,0,1)
    def game_result(self):
        if not self.is_game_over():
            return None
    
        if self.game.move_log[-1][0] == 'P1':
            return 1  # P1 win
        elif self.game.move_log[-1][0] == 'P2':
            return -1  # P2 win
        return 0  # Tie

