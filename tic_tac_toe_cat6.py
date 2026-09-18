import math

def print_board(board):
    symbols = {1: 'X', -1: 'O', 0: ' '}
    for i in range(3):
        row = [symbols[board[i * 3 + j]] for j in range(3)]
        print(' | '.join(row))
        if i < 2:
            print('-' * 9)

def check_winner(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]
    for a, b, c in lines:
        if board[a] != 0 and board[a] == board[b] == board[c]:
            return board[a]
    return 0

def is_full(board):
    return 0 not in board

def available_moves(board):
    return [i for i, v in enumerate(board) if v == 0]

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner != 0:
        return winner
    if is_full(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for m in available_moves(board):
            board[m] = 1
            best = max(best, minimax(board, False))
            board[m] = 0
        return best
    else:
        best = math.inf
        for m in available_moves(board):
            board[m] = -1
            best = min(best, minimax(board, True))
            board[m] = 0
        return best

def best_move(board, player):
    best_score = -math.inf if player == 1 else math.inf
    move = None
    for m in available_moves(board):
        board[m] = player
        score = minimax(board, player == -1)
        board[m] = 0
        if player == 1 and score > best_score:
            best_score, move = score, m
        elif player == -1 and score < best_score:
            best_score, move = score, m
    return move

def play():
    board = [0] * 9
    human, ai = 1, -1
    print("You are X, the computer is O.")
    print("Squares are numbered 0-8, left to right, top to bottom.\n")
    print_board(board)

    current = human
    while True:
        if current == human:
            move = int(input("\nYour move (0-8): "))
            while move not in available_moves(board):
                move = int(input("Invalid, try again (0-8): "))
        else:
            move = best_move(board, ai)
            print(f"\nComputer plays {move}")
        board[move] = current

        print_board(board)
        winner = check_winner(board)
        if winner != 0:
            print("\nYou win!" if winner == human else "\nComputer wins!")
            break
        if is_full(board):
            print("\nIt's a draw!")
            break
        current = -current

if __name__ == "__main__":
    play()