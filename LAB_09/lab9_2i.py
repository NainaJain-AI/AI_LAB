# Tic Tac Toe with Alpha-Beta + Tree Visualization

EMPTY = " "
X = "X"
O = "O"

nodes = 0
calls = 0
prunes = 0


# ---------------- BASIC FUNCTIONS ---------------- #

def create_board():
    return [EMPTY]*9


def print_board(board):
    print("\n     0   1   2")
    print("   -----------")
    for i in range(3):
        r = i*3
        print(f" {i} | {board[r]} | {board[r+1]} | {board[r+2]} |")
        print("   -----------")
    print()


def winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] and board[a] != EMPTY:
            return board[a]
    return None


def terminal(board):
    return winner(board) != None or EMPTY not in board


def utility(board):
    w = winner(board)
    if w == X: return 1
    if w == O: return -1
    return 0


def actions(board):
    return [i for i in range(9) if board[i] == EMPTY]


def result(board, move, player):
    new = board.copy()
    new[move] = player
    return new


# ---------------- ALPHA-BETA ---------------- #

def max_value(board, alpha, beta):
    global nodes, calls, prunes
    nodes += 1
    calls += 1

    if terminal(board):
        return utility(board), None

    v = -999
    best = None

    for a in actions(board):
        val, _ = min_value(result(board, a, X), alpha, beta)

        if val > v:
            v = val
            best = a

        alpha = max(alpha, v)

        if alpha >= beta:
            prunes += 1
            break   # PRUNE

    return v, best


def min_value(board, alpha, beta):
    global nodes, calls, prunes
    nodes += 1
    calls += 1

    if terminal(board):
        return utility(board), None

    v = 999
    best = None

    for a in actions(board):
        val, _ = max_value(result(board, a, O), alpha, beta)

        if val < v:
            v = val
            best = a

        beta = min(beta, v)

        if alpha >= beta:
            prunes += 1
            break   # PRUNE

    return v, best


def alphabeta(board):
    return max_value(board, -999, 999)


# ---------------- TREE PRINTING ---------------- #

def print_tree(board, depth=0, max_depth=3, alpha=-999, beta=999, is_max=True):
    """Print tree with pruning indication"""

    indent = "  " * depth

    if terminal(board):
        print(indent + f"[TERMINAL] Utility={utility(board)}")
        return

    if depth >= max_depth:
        return

    player = "X(MAX)" if is_max else "O(MIN)"
    print(indent + f"Depth {depth} | {player} | α={alpha} β={beta}")

    if is_max:
        v = -999
        for move in actions(board):
            new_board = result(board, move, X)
            print(indent + f"|-- Move {move}")

            val, _ = min_value(new_board, alpha, beta)

            print(indent + f"   Value={val}")

            v = max(v, val)
            alpha = max(alpha, v)

            if alpha >= beta:
                print(indent + "   ✂ PRUNED")
                break

    else:
        v = 999
        for move in actions(board):
            new_board = result(board, move, O)
            print(indent + f"|-- Move {move}")

            val, _ = max_value(new_board, alpha, beta)

            print(indent + f"   Value={val}")

            v = min(v, val)
            beta = min(beta, v)

            if alpha >= beta:
                print(indent + "   ✂ PRUNED")
                break


# ---------------- GAME LOOP ---------------- #

print("\nTIC TAC TOE (Alpha-Beta + Tree)\n")
print("YOU = O | AI = X\n")

board = create_board()
move_count = 0

while not terminal(board):

    print_board(board)

    # USER MOVE
    while True:
        try:
            move = int(input("Enter your move (0-8): "))
            if move < 0 or move > 8 or board[move] != EMPTY:
                print("Invalid move! Try again.")
                continue
            break
        except:
            print("Enter a valid number.")

    board[move] = O
    move_count += 1

    print("\n--- TREE AFTER YOUR MOVE ---")
    print_tree(board)

    if terminal(board):
        break

    # AI MOVE
    nodes = calls = prunes = 0
    ai_move, val = alphabeta(board)

    board[ai_move] = X
    move_count += 1

    print(f"\nAI plays: {ai_move} (value={val})")

    print("\n--- PERFORMANCE ---")
    print(f"Nodes: {nodes}, Calls: {calls}, Prunes: {prunes}")

    print("\n--- TREE AFTER AI MOVE ---")
    print_tree(board)


# ---------------- RESULT ---------------- #

print_board(board)

w = winner(board)
if w:
    print("Winner:", w)
else:
    print("Draw!")

print(f"Total moves: {move_count}")