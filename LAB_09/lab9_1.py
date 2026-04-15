# Tic Tac Toe using Minimax (No library imports)

EMPTY = " "
X = "X"
O = "O"

nodes = 0   # count nodes explored
call_count = 0  # count function calls


# Create board
def create_board():
    return [EMPTY, EMPTY, EMPTY,
            EMPTY, EMPTY, EMPTY,
            EMPTY, EMPTY, EMPTY]


# Print board with coordinates
def print_board(board):
    print("\n     0   1   2")
    print("   -----------")
    for i in range(3):
        row = i * 3
        print(f" {i} | {board[row]} | {board[row+1]} | {board[row+2]} |")
        print("   -----------")
    print()


# Check winner
def winner(board):
    win_positions = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b,c in win_positions:
        if board[a] == board[b] == board[c] and board[a] != EMPTY:
            return board[a]

    return None


# Check terminal state
def terminal(board):
    if winner(board) != None:
        return True

    for i in board:
        if i == EMPTY:
            return False

    return True


# Utility function
def utility(board):

    w = winner(board)

    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0


# Available moves
def actions(board):
    moves = []

    for i in range(9):
        if board[i] == EMPTY:
            moves.append(i)

    return moves


# Result after move
def result(board, move, player):

    new_board = board.copy()
    new_board[move] = player
    return new_board


# MAX player
def max_value(board, depth=0):

    global nodes
    global call_count
    nodes += 1
    call_count += 1

    if terminal(board):
        return utility(board), None

    v = -999
    best_move = None

    for a in actions(board):

        val, _ = min_value(result(board, a, X), depth+1)

        if val > v:
            v = val
            best_move = a

    return v, best_move


# MIN player
def min_value(board, depth=0):

    global nodes
    global call_count
    nodes += 1
    call_count += 1

    if terminal(board):
        return utility(board), None

    v = 999
    best_move = None

    for a in actions(board):

        val, _ = max_value(result(board, a, O), depth+1)

        if val < v:
            v = val
            best_move = a

    return v, best_move


# Minimax search
def minimax(board):

    value, move = max_value(board)

    return move, value


# Print comprehensive search tree with board states
def print_tree_detailed(board, depth=0, max_depth=2):
    """Print search tree with board states and minimax values"""
    if terminal(board):
        util = utility(board)
        print("  " * depth + f"`-- [TERMINAL] Utility: {util}")
        return

    if depth >= max_depth:
        return

    possible_moves = actions(board)
    player = "X (MAX)" if depth % 2 == 0 else "O (MIN)"
    
    print("  " * depth + f"+-- Depth {depth} | Player: {player} | Moves: {len(possible_moves)}")
    
    for i, move in enumerate(possible_moves):
        is_last = (i == len(possible_moves) - 1)
        prefix = "`-- " if is_last else "|-- "
        
        new_board = result(board, move, X if depth % 2 == 0 else O)
        
        print("  " * depth + prefix + f"Move {move}")
        print_tree_detailed(new_board, depth + 1, max_depth)

# Print performance and game statistics
def print_game_stats():
    print("\n" + "="*50)
    print("MINIMAX ALGORITHM PERFORMANCE STATISTICS")
    print("="*50)
    print(f"Total nodes explored: {nodes}")
    print(f"Total function calls: {call_count}")
    if call_count > 0:
        print(f"Nodes per call: {nodes/call_count:.2f}")
    print("="*50 + "\n")


# Main game loop
print("\n" + "="*50)
print("TIC-TAC-TOE WITH MINIMAX ALGORITHM")
print("="*50)
print("YOU are O | AI is X")
print("AI will evaluate all possible moves using Minimax\n")

board = create_board()
move_count = 0
last_tree_board = None
previous_board = None

while not terminal(board):

    print_board(board)

    # Player move
    while True:
        try:
            move = int(input("Enter your move (0-8): "))
            if move < 0 or move > 8:
                print("Invalid! Please enter a number between 0-8")
                continue
            if board[move] != EMPTY:
                print("Invalid! That position is already taken")
                continue
            break
        except ValueError:
            print("Invalid! Please enter a valid number")
    
    previous_board = board.copy()
    board[move] = O
    move_count += 1
    print(f"\nYour move: {move}")
    
    # Show tree after human's move
    print("\n" + "="*50)
    print("SEARCH TREE AFTER YOUR MOVE")
    print("="*50)
    print_board(board)
    print("Tree of possible continuations:\n")
    print_tree_detailed(board, max_depth=2)
    last_tree_board = board.copy()

    if terminal(board):
        break

    print("\nAI is thinking (evaluating all possible game outcomes)...")
    nodes = 0
    call_count = 0
    ai_move, minimax_value = minimax(board)
    
    previous_board = board.copy()
    board[ai_move] = X
    move_count += 1
    print(f"AI Move: {ai_move} (Minimax value: {minimax_value})")
    print_game_stats()
    
    # Show tree after AI's move
    print("="*50)
    print("SEARCH TREE AFTER AI MOVE")
    print("="*50)
    print_board(board)
    print("Tree of possible continuations:\n")
    print_tree_detailed(board, max_depth=2)
    last_tree_board = board.copy()

print("\n" + "="*50)
print("GAME OVER!")
print("="*50)
print_board(board)

w = winner(board)

if w:
    print(f" WINNER: {w}\n")
else:
    print("It's a DRAW!\n")

print(f"Total moves played: {move_count}")
print("="*50 + "\n")

# Show final search tree from end-game position
print("="*50)
print("FINAL SEARCH TREE (Last Tree Before Game Ended)")
print("="*50)
if previous_board:
    print_board(previous_board)
    print("Tree of possible continuations:\n")
    print_tree_detailed(previous_board, max_depth=2)
print("\n" + "="*50)    