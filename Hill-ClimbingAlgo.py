import random
import time

def print_board(board):
    """
    Prints the chess board to the console by joining
    cells with a space between them.

    Args:
        board (list of list of int)
        An 8x8 list representing the chess board, where
        each cell contains 0 for empty or 1 for a queen.
    """
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print()


def create_board():
    """
    Creates an 8x8 Chessboard initialized with all 0's

    Returns:
        list of list of int
    """
    return [[0] * 8 for _ in range(8)]


def place_queens(board):
    """
    Randomly places 8 queens on the board, one for each column.

    Returns:
        list of list of int
    """
    for i in range(8):
        row = random.randint(0, 7)
        board[row][i] = 1
    return board


def get_attacking_pairs(board):
    """
    Calculates the number of pairs where queens are attacking each other.
    Since each pair gets counted twice, we have to return half the number of
    attacking pairs.

    Returns:
        int
    """
    attacking_pairs = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                for k in range(8):
                    if k != j and board[i][k] == 1:
                        attacking_pairs += 1
                    if k != i and board[k][j] == 1:
                        attacking_pairs += 1
                for k in range(1, 8):
                    if i + k < 8 and j + k < 8 and board[i + k][j + k] == 1:
                        attacking_pairs += 1
                    if i - k >= 0 and j + k < 8 and board[i - k][j + k] == 1:
                        attacking_pairs += 1
                    if i + k < 8 and j - k >= 0 and board[i + k][j - k] == 1:
                        attacking_pairs += 1
                    if i - k >= 0 and j - k >= 0 and board[i - k][j - k] == 1:
                        attacking_pairs += 1
    return attacking_pairs // 2


def get_neighbors(board):
    neighbors = []
    for col in range(8):
        for row in range(8):
            if board[row][col] == 0:
                new_board = [r[:] for r in board]
                for r in range(8):
                    new_board[r][col] = 0
                new_board[row][col] = 1
                neighbors.append(new_board)
    return neighbors


def hill_climb(board):
    current_board = board
    current_attacks = get_attacking_pairs(current_board)
    while True:
        neighbors = get_neighbors(current_board)
        next_board = None
        next_attacks = current_attacks
        for neighbor in neighbors:
            attacks = get_attacking_pairs(neighbor)
            if attacks < next_attacks:
                next_board = neighbor
                next_attacks = attacks
        if next_attacks >= current_attacks:
            break
        current_board = next_board
        current_attacks = next_attacks
    return current_board, current_attacks

def measure_performance_hill_climb(runs=100):
    start_time = time.time()
    solutions_found = 0
    for _ in range(runs):
        initial_board = place_queens(create_board())
        solution, attacks = hill_climb(initial_board)
        if attacks == 0:
            solutions_found += 1
    end_time = time.time()
    elapsed_time = end_time - start_time
    success_rate = solutions_found / runs
    return elapsed_time, success_rate

elapsed_time, success_rate = measure_performance_hill_climb()
print(f"Hill-Climbing Performance: Time = {elapsed_time:.2f}s, Success Rate = {success_rate:.2%}")
initial_board = place_queens(create_board())
solution, attacks = hill_climb(initial_board)

print("Initial Board:")
print_board(initial_board)
print("Solution Board:")
print_board(solution)
print(f"Attacking Pairs: {attacks}")
