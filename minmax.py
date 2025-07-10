from Q20 import Quoridor
from quoridor_state import QuoridorState
from a_star import a_star

pos_infinite = 5000000
neg_infinite = -5000000

class MinmaxNode:
    def __init__(self, state : QuoridorState, isMax, parentMove=None):
        self.state : QuoridorState = state
        self.childrens = []
        self.parentMove = parentMove
        self.isMax = isMax
        self.value = -1

    def generateChildrens(self):
        moves = self.state.get_legal_actions()
        for action in moves:
            self.childrens.append(MinmaxNode(self.state.move(action), not root.isMax, action))

    def heuristic(self):
        pos, ply = state.game.getPosPlayer()
        objectif = (0, 2) if ply == 0 else (4, 2)
        return len(a_star(state, pos, objectif))
        

def minmax(root : MinmaxNode,alpha,beta,depth):
    root.generateChildrens()
    if(root.state.is_game_over() or depth == 0):
        root.value = root.heuristic()
        return root.heuristic()
    else:
        if(not root.isMax): #noeud de type min
            v = pos_infinite
            for child in root.childrens:
                v = min(v, minmax(child, alpha, beta, depth-1))
                if(alpha >= v):
                    root.value = v
                    return v
                beta = min(beta, v)
        else:               #noeud de type max
            v = neg_infinite
            for child in root.childrens:
                v = max(v, minmax(child, alpha, beta, depth-1))
                if(v >= beta):
                    root.value = v
                    return v
                alpha = max(alpha, v)
    root.value = v
    return v


if __name__ == "__main__":

    game = Quoridor(5)
    game.place_wall(("V",3,1))
    game.place_wall(("H",3,2))
    game.place_wall(("H",2,3))
    game.setPos((2,2),(3,2),1)

    state = QuoridorState(game)
    state.game.print_board()

    root = MinmaxNode(state, True)
    minmax = minmax(root,neg_infinite, pos_infinite, 2)
    max_child = root.childrens[0]
    for child in root.childrens:
        if child.value >= max_child.value:
            max_child = child
    print(max_child.parentMove)

    print(game.walls, game.ply)

    

