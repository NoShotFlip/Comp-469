import networkx as networkx
import heapq


class PuzzleGraph:
    def __init__(self, inital_state, goal_state):
        self.inital_state = tuple(inital_state)
        self.goal_state = tuple(goal_state)
        self.graph = nx.DiGraph()
        self.build_graph()

    def build_graph(self):
        """
        Builds the graph for the puzzle. Each state of the puzzle is a node, and each valid move between states is an edge.
        """
        queue = [self.inital_state]
        visited = set()
        while queue:
            state = queue.pop(0)
            if state in visited:
                continue
            visited.add(state)
            self.graph.add_node(state)
            for neighbor in self.get_neighbors(state):
                if neighbor not in visited:
                    queue.append(neighbor)
                self.graph.add_edge(state, neighbor)

    def get_neighbors(self, state):
        """
        Returns the neighboring states of the given state by moving the empty space in the puzzle.
        """

        neighbors = []
        empty_index = state.index(0)
        row, col = divmod(empty_index, 3)
        moves = {'up': -3, 'down': 3, 'left': -1, 'right': 1}
        for move, pos_change in moves.items():
            new_index = empty_index+pos_change
            if move == 'up' and row == 0 or move == 'down' and row == 2 or move == 'left' and col == 0 or move == 'right' and col == 2:
                continue
            new_state = list(state)
            new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
            neighbors.append(tuple(new_state))
        return neighbors

    # example usuage
    inital_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    puzzle_graph = PuzzleGraph(inital_state, goal_state)
