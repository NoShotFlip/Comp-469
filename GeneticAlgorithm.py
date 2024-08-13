import random
import time
from concurrent.futures import ThreadPoolExecutor


def print_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print()


def create_board():
    return [[0] * 8 for _ in range(8)]


def place_queens(board):
    for i in range(8):
        row = random.randint(0, 7)
        board[row][i] = 1
    return board


def optimized_get_attacking_pairs(board):
    attacking_pairs = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                # Check row
                attacking_pairs += sum(board[i]) - 1
                # Check column
                attacking_pairs += sum(board[k][j] for k in range(8)) - 1
                # Check diagonals
                attacking_pairs += sum(
                    board[i + k][j + k] == 1
                    for k in range(1, 8)
                    if i + k < 8 and j + k < 8
                )
                attacking_pairs += sum(
                    board[i - k][j + k] == 1
                    for k in range(1, 8)
                    if i - k >= 0 and j + k < 8
                )
                attacking_pairs += sum(
                    board[i + k][j - k] == 1
                    for k in range(1, 8)
                    if i + k < 8 and j - k >= 0
                )
                attacking_pairs += sum(
                    board[i - k][j - k] == 1
                    for k in range(1, 8)
                    if i - k >= 0 and j - k >= 0
                )
    return attacking_pairs // 2


def optimized_fitness(board):
    return 1 / (1 + optimized_get_attacking_pairs(board))


def reproduce(parent1, parent2):
    crossover_point = random.randint(0, 7)
    child = create_board()
    for i in range(8):
        if i <= crossover_point:
            for row in range(8):
                child[row][i] = parent1[row][i]
        else:
            for row in range(8):
                child[row][i] = parent2[row][i]
    return child


def mutate(board):
    col = random.randint(0, 7)
    for r in range(8):
        board[r][col] = 0
    row = random.randint(0, 7)
    board[row][col] = 1
    return board


def optimized_genetic_algorithm(
    population_size=50, mutation_rate=0.05, max_generations=500
):
    population = [place_queens(create_board()) for _ in range(population_size)]
    for generation in range(max_generations):
        with ThreadPoolExecutor() as executor:
            fitness_values = list(executor.map(optimized_fitness, population))
        population = [
            x for _, x in sorted(zip(fitness_values, population), reverse=True)
        ]
        if optimized_get_attacking_pairs(population[0]) == 0:
            return population[0], optimized_get_attacking_pairs(population[0])
        new_population = population[:2]
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, weights=fitness_values, k=2)
            child = reproduce(parent1, parent2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)
        population = new_population
    return population[0], optimized_get_attacking_pairs(population[0])


# Measure the performance of the optimized genetic algorithm


def measureperformance_genetic_algorithm(runs=10):
    start_time = time.time()
    solutions_found = 0
    for run in range(runs):
        solution, attacks = optimized_genetic_algorithm()
        if attacks == 0:
            print(f"Found solution on run {run}")
            print(f"Num attacks:{attacks}")
            print_board(solution)
            solutions_found += 1
    end_time = time.time()
    elapsed_time = end_time - start_time
    success_rate = solutions_found / runs
    return elapsed_time, success_rate


elapsed_time, success_rate = measureperformance_genetic_algorithm()


print(f"Optimized Genetic Algorithm Performance: Time = {elapsed_time:.2f}s")
print(f"Solution Board: {success_rate}")
