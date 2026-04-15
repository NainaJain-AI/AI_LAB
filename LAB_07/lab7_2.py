import random
import math

N = 8

def heuristic(board):
    """Number of pairs of queens attacking each other."""
    h = 0
    for i in range(N):
        for j in range(i+1, N):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                h += 1
    return h

def random_board():
    """Randomly place one queen in each column."""
    return [random.randint(0, N-1) for _ in range(N)]

def get_neighbors(board):
    """Generate all neighbors by moving one queen in its column."""
    neighbors = []
    for col in range(N):
        for row in range(N):
            if board[col] != row:
                neighbor = list(board)
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors

def steepest_ascent_hill_climbing(initial_board):
    board = list(initial_board)
    steps = 0
    h = heuristic(board)
    while True:
        neighbors = get_neighbors(board)
        neighbor_hs = [heuristic(nb) for nb in neighbors]
        min_h = min(neighbor_hs)
        if min_h >= h:
            break
        idx = neighbor_hs.index(min_h)
        board = neighbors[idx]
        h = min_h
        steps += 1
    return board, h, steps

def first_choice_hill_climbing(initial_board, max_attempts=100):
    board = list(initial_board)
    h = heuristic(board)
    steps = 0
    for _ in range(max_attempts):
        col = random.randint(0, N-1)
        row = random.randint(0, N-1)
        if board[col] == row:
            continue
        neighbor = list(board)
        neighbor[col] = row
        neighbor_h = heuristic(neighbor)
        if neighbor_h < h:
            board = neighbor
            h = neighbor_h
            steps += 1
            if h == 0:
                break
    return board, h, steps

def random_restart_hill_climbing(max_restarts=50):
    total_steps = 0
    for restart in range(max_restarts):
        board = random_board()
        h = heuristic(board)
        steps = 0
        while True:
            neighbors = get_neighbors(board)
            neighbor_hs = [heuristic(nb) for nb in neighbors]
            min_h = min(neighbor_hs)
            if min_h >= h:
                break
            idx = neighbor_hs.index(min_h)
            board = neighbors[idx]
            h = min_h
            steps += 1
            if h == 0:
                total_steps += steps
                return board, h, total_steps, restart+1
        total_steps += steps
    return board, h, total_steps, max_restarts

def simulated_annealing(initial_board, max_steps=1000, T0=100, cooling=0.99):
    board = list(initial_board)
    h = heuristic(board)
    steps = 0
    T = T0
    while steps < max_steps and h > 0:
        col = random.randint(0, N-1)
        row = random.randint(0, N-1)
        if board[col] == row:
            continue
        neighbor = list(board)
        neighbor[col] = row
        neighbor_h = heuristic(neighbor)
        delta = neighbor_h - h
        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-10)):
            board = neighbor
            h = neighbor_h
        T *= cooling
        steps += 1
    return board, h, steps

def run_experiment(algorithm, runs=50):
    results = []
    for i in range(runs):
        initial_board = random_board()
        initial_h = heuristic(initial_board)
        if algorithm == "steepest":
            final_board, final_h, steps = steepest_ascent_hill_climbing(initial_board)
            status = "Solved" if final_h == 0 else "Fail"
            results.append((initial_h, final_h, steps, status))
        elif algorithm == "first_choice":
            final_board, final_h, steps = first_choice_hill_climbing(initial_board)
            status = "Solved" if final_h == 0 else "Fail"
            results.append((initial_h, final_h, steps, status))
        elif algorithm == "random_restart":
            final_board, final_h, steps, restarts = random_restart_hill_climbing()
            status = "Solved" if final_h == 0 else "Fail"
            results.append((None, final_h, steps, status, restarts))
        elif algorithm == "annealing":
            final_board, final_h, steps = simulated_annealing(initial_board)
            status = "Solved" if final_h == 0 else "Fail"
            results.append((initial_h, final_h, steps, status))
    return results

def print_results(results, algo_name):
    print(f"\n{algo_name} Results:")
    if algo_name == "Random Restart Hill Climbing":
        print("Run\tFinal_h\tSteps\tRestarts\tStatus")
        for i, r in enumerate(results):
            print(f"{i+1}\t{r[1]}\t{r[2]}\t{r[4]}\t\t{r[3]}")
    else:
        print("Run\tInitial_h\tFinal_h\tSteps\tStatus")
        for i, r in enumerate(results):
            print(f"{i+1}\t{r[0]}\t\t{r[1]}\t{r[2]}\t{r[3]}")
    fails = [r for r in results if (r[1] if algo_name == "Random Restart Hill Climbing" else r[1]) > 0]
    if fails:
        print("Presence of local minimum is proven by failed runs.")
    else:
        print("No local minimum encountered in these runs.")

if __name__ == "__main__":
    steepest_results = run_experiment("steepest")
    first_choice_results = run_experiment("first_choice")
    random_restart_results = run_experiment("random_restart")
    annealing_results = run_experiment("annealing")

    print_results(steepest_results, "Steepest Ascent Hill Climbing")
    print_results(first_choice_results, "First Choice Hill Climbing")
    print_results(random_restart_results, "Random Restart Hill Climbing")
    print_results(annealing_results, "Simulated Annealing")

    print("\nComparison Summary:")
    print("Algorithm\tSolved\tFail")
    for name, results in [
        ("Steepest", steepest_results),
        ("First Choice", first_choice_results),
        ("Random Restart", random_restart_results),
        ("Annealing", annealing_results)
    ]:
        solved = sum(1 for r in results if r[1] == 0)
        fail = len(results) - solved
        print(f"{name}\t\t{solved}\t{fail}")