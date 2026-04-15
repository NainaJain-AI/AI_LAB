import random

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

def get_best_move(board):
    """Find the best move for each queen (steepest descent)."""
    best_board = list(board)
    best_h = heuristic(board)
    for col in range(N):
        original_row = board[col]
        for row in range(N):
            if row == original_row:
                continue
            board[col] = row
            h = heuristic(board)
            if h < best_h:
                best_h = h
                best_board = list(board)
        board[col] = original_row
    return best_board, best_h

def steepest_ascent_hill_climbing(initial_board):
    board = list(initial_board)
    steps = 0
    h = heuristic(board)
    while True:
        next_board, next_h = get_best_move(board)
        if next_h >= h:
            break
        board = next_board
        h = next_h
        steps += 1
    return board, h, steps

results = []
for i in range(50):
    initial_board = random_board()
    initial_h = heuristic(initial_board)
    final_board, final_h, steps = steepest_ascent_hill_climbing(initial_board)
    status = "Solved" if final_h == 0 else "Fail"
    results.append({
        "initial_h": initial_h,
        "final_h": final_h,
        "steps": steps,
        "status": status
    })

print("Run\tInitial_h\tFinal_h\tSteps\tStatus")
for i, r in enumerate(results):
    print(f"{i+1}\t{r['initial_h']}\t\t{r['final_h']}\t{r['steps']}\t{r['status']}")

failures = [r for r in results if r['status'] == "Fail"]
if failures:
    print("\nPresence of local minimum is proven by runs that failed to reach h=0 (solution).")
else:
    print("\nNo local minimum encountered in these runs.")