import networkx as nx
import heapq
from collections import deque

class PuzzleGraph:
    def __init__(self, initial_state, goal_state):
        self.initial_state = tuple(initial_state)
        self.goal_state = tuple(goal_state)
        self.graph = nx.DiGraph()
        self.build_graph()

    def build_graph(self):
        """
        Builds the graph for the puzzle. Each state of the puzzle is a node, and each valid move between states is an edge.
        """
        queue = [self.initial_state]
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
            new_index = empty_index + pos_change
            if move == 'up' and row == 0 or move == 'down' and row == 2 or move == 'left' and col == 0 or move == 'right' and col == 2:
                continue
            new_state = list(state)
            new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
            neighbors.append(tuple(new_state))
        print(f"Neighbors of {state}: {neighbors}")  # Debugging statement
        return neighbors

    def bfs(self):
        """
        Breadth-First Search (BFS) to find the shortest path to the goal state.
        """
        queue = deque([(self.initial_state, [])])
        visited = set()

        while queue:
            current_state, path = queue.popleft()
            if current_state == self.goal_state:
                return path + [current_state]

            if current_state in visited:
                continue

            visited.add(current_state)

            neighbors = self.get_neighbors(current_state)
            if neighbors is None:
                print(f"Error: get_neighbors returned None for state {current_state}")  # Debugging statement
                continue

            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [current_state]))

        return None

    def measure_performance(self, search_algorithm):
        import time
        start_time = time.time()
        solution_path = search_algorithm()
        end_time = time.time()
        if solution_path:
            print(f"Solution found in {len(solution_path) - 1} moves")
            print(f"Time taken: {end_time - start_time} seconds")
            print("Solution Path:")
            for state in solution_path:
                for i in range(0, len(state), 3):
                    print(state[i:i+3])
                print()
        else:
            print("No solution found")

# Example initial and goal states
initial_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Create a PuzzleGraph object and measure performance using BFS
puzzle_graph = PuzzleGraph(initial_state, goal_state)
puzzle_graph.measure_performance(puzzle_graph.bfs)
