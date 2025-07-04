import heapq
from Q20 import Quoridor
from quoridor_state import QuoridorState


def a_star(state : QuoridorState, start, goal):
    rows, cols = 5, 5

    def heuristic(a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(node):
        legal_directions = state.game.get_legal_directions(node)
        neighbors = []
        for dir in legal_directions:
            direction = dir[0]
            if direction == 'D':
                neighbors.append((node[0] + 1, node[1]))
            elif direction == "U":
                neighbors.append((node[0] - 1, node[1]))
            elif direction == "R":
                neighbors.append((node[0], node[1] + 1))
            elif direction == "L":
                neighbors.append((node[0], node[1] - 1))
        return neighbors


    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, cost, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # reverse

        for neighbor in get_neighbors(current):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                came_from[neighbor] = current

    return None  # No path found

if __name__ == "__main__":
    grid = [
        [False, 0, 0, 0, 1],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
    ]

    start = (4, 2)
    goal = (0, 2)

    game = Quoridor(5)
    game.place_wall(("V",3,1))
    game.place_wall(("H",3,2))
    game.place_wall(("H",2,3))
    #game.setPos((2,1),(2,4),1)
    state = QuoridorState(game)
    state.game.print_board()
    path = a_star(state, start, goal)

    if path:
        for p in path:
            print(p)
    else:
        print("Aucun chemin trouvé.")
