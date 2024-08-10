import math
import random

def print_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print()

def create_board():
    return [[0]*8 for _ in range(8)]

def place_queens(board):
    for i in range(8):
        row = random.randint(0, 7)
        board[row][i] = 1
    return board

def get_attacking_pairs(board):
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
                    if i+k < 8 and j+k < 8 and board[i+k][j+k] == 1:
                        attacking_pairs += 1
                    if i-k >= 0 and j+k < 8 and board[i-k][j+k] == 1:
                        attacking_pairs += 1
                    if i+k < 8 and j-k >= 0 and board[i+k][j-k] == 1:
                        attacking_pairs += 1
                    if i-k >= 0 and j-k >= 0 and board[i-k][j-k] == 1:
                        attacking_pairs += 1
    return attacking_pairs // 2

def get_random_neighbor(board):
    new_board = [r[:] for r in board]
    col = random.randint(0, 7)
    row = random.randint(0, 7)
    for r in range(8):
        new_board[r][col] = 0
    new_board[row][col] = 1
    return new_board

def simulated_annealing(board, max_steps=1000, initial_temp=100.0, cooling_rate=0.95):
    current_board = board
    current_attacks = get_attacking_pairs(current_board)
    temp = initial_temp

    for step in range(max_steps):
        if current_attacks == 0:
            break

        neighbor = get_random_neighbor(current_board)
        neighbor_attacks = get_attacking_pairs(neighbor)

        if neighbor_attacks < current_attacks:
            current_board = neighbor
            current_attacks = neighbor_attacks
        else:
            delta = neighbor_attacks - current_attacks
            probability = math.exp(-delta / temp)
            if random.uniform(0, 1) < probability:
                current_board = neighbor
                current_attacks = neighbor_attacks

        temp *= cooling_rate

    return current_board, current_attacks

initial_board = place_queens(create_board())
solution, attacks = simulated_annealing(initial_board)

print("Initial Board:")
print_board(initial_board)
print("Solution Board:")
print_board(solution)
print(f"Attacking Pairs: {attacks}")
