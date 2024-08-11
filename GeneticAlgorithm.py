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


def fitness(board):
    """
    Returns the fitness of a board configuration. This is inversely correlated
    to the number of attacking pairs, because we want to have the least amount
    of attacking pairs possible.
    """
    return 1 / (1 + get_attacking_pairs(board))


def reproduce(parent1, parent2):
    """
    Creates a new board configuration from the two parent configurations.
    The child gets parent1's columns from 0 to crossover_point, and parent2's
    columns from crossover_point + 1 to 7

    Returns:
        list of list of int: the child board reproduced
    """
    crossover_point = random.randint(0, 7)
    child = create_board()
    # for each column, copy it with each row in that column to the child
    # the if-else statement chooses whether we take the column from
    # parent1 or parent2 depending on the crossover point.
    for i in range(8):
        if i <= crossover_point:
            for row in range(8):
                child[row][i] = parent1[row][i]
        else:
            for row in range(8):
                child[row][i] = parent2[row][i]
    return child


def mutate(board):
    """
    Randomly mutates the board by changing the position
    of one queen in a column.

    Returns:
        list of list of int: the mutated board
    """
    # choose a random column
    col = random.randint(0, 7)

    # for each row in that column set it to 0
    for r in range(8):
        board[r][col] = 0
    # now put a queen in a random row in that column
    row = random.randint(0, 7)
    board[row][col] = 1
    return board


def genetic_algorithm(population_size=50, mutation_rate=0.1, max_generations=500):
    """
    Creates a solution to the 8-queens problem using a genetic algorithm.

    Args:
        population_size: int: The number of boards in the population.
                                         defaults to 50
        mutation_rate float: The probability of mutation occurring during reproduction.
                                         defaults to 0.1
        max_generations int: The maximum number of generations to run the algorithm.
                                         defaults to 500

    Returns:
        tuple: A tuple containing: the solution board and number of attacks
    """
    # initialize the starting population
    population = [place_queens(create_board()) for _ in range(population_size)]

    for generation in range(max_generations):
        # sort by fitness (evolution)
        population.sort(key=lambda board: fitness(board), reverse=True)
        # if we find a solution terminate
        if get_attacking_pairs(population[0]) == 0:
            return population[0], get_attacking_pairs(population[0])
        # only take the best 2 individuals from this generation (elitism)
        new_population = population[:2]
        # generate the rest of the new population, because we culled the rest
        while len(new_population) < population_size:
            # choose two parents weighted based on fitness
            parent1 = random.choices(
                population, weights=[fitness(board) for board in population], k=1
            )[0]
            parent2 = random.choices(
                population, weights=[fitness(board) for board in population], k=1
            )[0]
            child = reproduce(parent1, parent2)
            # random mutation may occur to the child with low probability
            if random.random() < mutation_rate:
                child = mutate(child)

            new_population.append(child)
        # overwrite the population to the new one
        population = new_population
    # if we reached the max generations, return the best solution we have
    return population[0], get_attacking_pairs(population[0])

def measure_performance_genetic_algorithm(runs=100):
    start_time = time.time()
    solutions_found = 0
    for _ in range(runs):
        solution, attacks = genetic_algorithm()
        if attacks == 0:
            solutions_found += 1
    end_time = time.time()
    elapsed_time = end_time - start_time
    success_rate = solutions_found / runs
    return elapsed_time, success_rate

# Measure the performance of the genetic algorithm
elapsed_time, success_rate = measure_performance_genetic_algorithm()

print(f"Genetic Algorithm Performance: Time = {elapsed_time:.2f}s, Success Rate = {success_rate:.2%}")
# default arguments used
solution, attacks = genetic_algorithm()

print("Solution Board:")
print_board(solution)
print(f"Attacking Pairs: {attacks}")
