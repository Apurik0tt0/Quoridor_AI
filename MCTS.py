import copy
import numpy as np
from collections import defaultdict
from quoridor_state import QuoridorState
from a_star import a_star
from Q20 import Quoridor


class MonteCarloTreeSearchNode():
    def __init__(self, state: QuoridorState, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

#print best move
    def getState(self):
        return self.parent_action

#return list of untried action
    def untried_actions(self):

        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

#return wins-loses
    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

#return number of time visited
    def n(self):
        return self._number_of_visits

#create a new child by using a remaining not tried action
    def expand(self):
        
        action = self._untried_actions.pop()
        next_state = self.state.move(action)
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node 

#return if the node is a leaf or not
    def is_terminal_node(self):
        return self.state.is_game_over()

#plays a game until 1 person win or tie (-1 loss | 0 tie | 1 win)
#here we need to define the rollout policy wich is the way of chosing moves at each turn
    def rollout(self):
        current_state = copy.deepcopy(self.state)  # only one copy here
        #current_state.game.print_board()
        while not current_state.is_game_over():
            possible_moves = current_state.get_legal_actions()
            action = self.rollout_policy(current_state,possible_moves)
            current_state.move_inplace(action)  
        #print(current_state.game.getPosPlayer(ply=1))
        return current_state.game_result()

#update all the nodes after a rollout
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

#return if all actions have been used at least 1 time
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

#Selection part : once fully expanded, select the best child to explore (UCB1)
    def best_child(self, c_param=0.1):
    
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

#return the move to play
#Shouldn't be random, not the best way I think
#Faire que si on ne trouve pas de chemin, renvoyer move au hasard      return possible_moves[np.random.randint(len(possible_moves))]
    def rollout_policy(self,state: QuoridorState, possible_moves):
        #return possible_moves[np.random.randint(len(possible_moves))]
        pos, ply = state.game.getPosPlayer()
        objectif = (2, 0) if ply == 0 else (4, 2)

        path = a_star(state, pos, objectif)

        # No path found
        if not path or len(path) < 2:
            return possible_moves[np.random.randint(len(possible_moves))]

        # Next Move
        new_pos = path[1]  # path[0] == current position
        move = (new_pos[0] - pos[0], new_pos[1] - pos[1])

        if move == (1, 0):
            action = ("D",)
        elif move == (-1, 0):
            action = ("U",)
        elif move == (0, 1):
            action = ("R",)
        elif move == (0, -1):
            action = ("L",)
        else:
            # We never know (not supposed to happen)
            action = possible_moves[np.random.randint(len(possible_moves))]
        #print(action)
        #if legal move
        if action in possible_moves:
            return action
        else:
            return possible_moves[np.random.randint(len(possible_moves))]

#select node to run rollout on
    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
    
#Return the best move to play
    def best_action(self):
        simulation_no = 50 #number of simulation 
        
        
        for i in range(simulation_no):
            
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.best_child(c_param=0.)
    

if __name__ == "__main__":

    game = Quoridor(5)
    #game.place_wall(("H",1,2))
    #game.place_wall(("H",2,3))
    game.setPos((2,2),(0,0),0)
    root = MonteCarloTreeSearchNode(state = QuoridorState(game))
    selected_node = root.best_action()
    print(selected_node.getState())
    #game.print_board()
    







