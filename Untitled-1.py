import networkx as nx
import heapq
from collections import deque

def heuristic (state,goal):
        """
        Heuristic function for A* algorithm. Computes the Manhattan distance between the current state and the goal state.
        """
        return sum(abs(b % 3 - g % 3) + abs(b // 3 - g // 3)
                    for b, g in ((state.index(i), goal.index(i)) for i in range(1, 9)))

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
    
    def dfs(self):
        """
        Depth-First Search (DFS) to find a path to the goal state.
        """
        stack = [(self.initial_state,[])]
        visited = set()
        
        while stack :
            current_state , path = stack.pop()
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
                    stack.append((neighbor,path+[current_state]))
        return None

    

    def a_star(self):
        """
        A* Search to find the optimal path to the goal state.
        """
        heap = [(heuristic(self.initial_state, self.goal_state), 0, self.initial_state, [])]
        visited = set()

        while heap:
            h, cost , current_state , path  = heapq.heappop(heap)
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
                    heapq.heappush(heap, (heuristic(neighbor, self.goal_state) + cost + 1, cost + 1, neighbor, path + [current_state]))
        return None
    
    def greedy_best_first(self):
        """
        Greedy Best-First Search to find a path to the goal state.
        """
        heap = [(heuristic(self.initial_state, self.goal_state), self.initial_state, [])]
        visited = set()

        while heap:
            h, current_state,path = heapq.heappop(heap)
            if current_state == self.goal_state:
                return path + [current_state]
            if current_state in visited:
                continue
            visited.add(current_state)

            neighbors= self.get_neighbors(current_state)
            if neighbors is None:
                print(f"Error: get_neighbors returned None for state {current_state}")  # Debugging statement
                continue

            for neighbor in neighbors:
                if neighbor not in visited:
                    heapq.heappush(heap, (heuristic(neighbor, self.goal_state), neighbor, path + [current_state]))

        return None
    def ids(self):
        """
        Iterative Deepening Search (IDS) to find a path to the goal state.
        """
        def dls(state, path, depth):
            if depth == 0:
                if state == self.goal_state:
                    return path + [state]
                return None
            if depth > 0:
                for neighbor in self.get_neighbors(state):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        result = dls(neighbor, path + [state], depth - 1)
                        if result:
                            return result
                        visited.remove(neighbor)
            return None

        depth = 0
        while True:
            visited = set()
            result = dls(self.initial_state, [], depth)
            if result:
                return result
            depth += 1


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
print("BFS Performance:")
puzzle_graph.measure_performance(puzzle_graph.bfs)
# Measure performance using DFS
print("DFS Performance:")
puzzle_graph.measure_performance(puzzle_graph.dfs)

# Measure performance using A*
print("A* Performance:")
puzzle_graph.measure_performance(puzzle_graph.a_star)

# Measure performance using Greedy Best-First
print("Greedy Best-First Performance:")
puzzle_graph.measure_performance(puzzle_graph.greedy_best_first)

# Measure performance using Iterative Deepening Search
print("Iterative Deepening Search Performance:")
puzzle_graph.measure_performance(puzzle_graph.ids)