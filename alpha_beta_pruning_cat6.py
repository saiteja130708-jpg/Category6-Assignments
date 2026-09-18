import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}
CHECKMATE_SCORE = 100000

nodes_visited = 0  

def evaluate_board(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -CHECKMATE_SCORE
        else:
            return CHECKMATE_SCORE
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score

def ordered_moves(board):
    def move_score(move):
        if board.is_capture(move):
            captured_square = move.to_square
            captured_piece = board.piece_at(captured_square)
            if captured_piece is None:
                return PIECE_VALUES[chess.PAWN]
            attacker = board.piece_at(move.from_square)
            captured_value = PIECE_VALUES[captured_piece.piece_type]
            attacker_value = PIECE_VALUES[attacker.piece_type] if attacker else 0
            return captured_value * 10 - attacker_value
        return 0
    return sorted(board.legal_moves, key=move_score, reverse=True)

def minimax(board, depth, alpha, beta, maximizing_player):
    global nodes_visited
    nodes_visited += 1

    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        best_score = float("-inf")
        for move in ordered_moves(board):
            board.push(move)
            score = minimax(
                board,
                depth - 1,
                alpha,
                beta,
                False
            )
            board.pop()
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  
        return best_score
    else:
        best_score = float("inf")
        for move in ordered_moves(board):
            board.push(move)
            score = minimax(
                board,
                depth - 1,
                alpha,
                beta,
                True
            )
            board.pop()
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break  
        return best_score

def find_best_move(board, depth):
    global nodes_visited
    nodes_visited = 0
    best_move = None

    if board.turn == chess.WHITE:
        best_score = float("-inf")
        for move in ordered_moves(board):
            board.push(move)
            score = minimax(
                board,
                depth - 1,
                float("-inf"),
                float("inf"),
                False
            )
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = float("inf")
        for move in ordered_moves(board):
            board.push(move)
            score = minimax(
                board,
                depth - 1,
                float("-inf"),
                float("inf"),
                True
            )
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move

    return best_move, best_score

def print_game_status(board):
    print()
    if board.is_check():
        print("CHECK!")
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            print("Checkmate! Black wins.")
        else:
            print("Checkmate! White wins.")
    elif board.is_stalemate():
        print("Draw by stalemate.")
    elif board.is_insufficient_material():
        print("Draw by insufficient material.")
    elif board.is_fivefold_repetition():
        print("Draw by fivefold repetition.")
    elif board.is_seventyfive_moves():
        print("Draw by 75-move rule.")

def main():
    board = chess.Board()
    AI_COLOR = chess.BLACK
    AI_DEPTH = 3
    print("       PYTHON CHESS AI (ALPHA-BETA)")
    print()
    print("You are White.")
    print("AI is Black.")
    print(f"AI search depth: {AI_DEPTH}")
    print()
    print("Enter moves in chess notation.")
    print("Examples: e4, Nf3, Bc4, O-O, Qxd5")
    print("Type 'quit' to exit.")
    print()
    while not board.is_game_over():
        print(board)
        print()
        print("FEN:", board.fen())
        print()
        if board.turn != AI_COLOR:
            while True:
                user_move = input("Your move: ").strip()
                if user_move.lower() == "quit":
                    print("Game ended.")
                    return
                try:
                    move = board.parse_san(user_move)
                    if move in board.legal_moves:
                        board.push(move)
                        break
                    else:
                        print("Illegal move.")
                except ValueError:
                    try:
                        move = chess.Move.from_uci(user_move)
                        if move in board.legal_moves:
                            board.push(move)
                            break
                        else:
                            print("Illegal move.")
                    except ValueError:
                        print("Invalid move. Try again.")
        else:
            print("AI is thinking...")
            best_move, score = find_best_move(
                board,
                AI_DEPTH
            )
            if best_move is None:
                break
            print("AI move:", board.san(best_move))
            print("Engine score:", score)
            print("Nodes visited (with alpha-beta pruning):", nodes_visited)
            board.push(best_move)
        print()
        print_game_status(board)
        print()
    print(board)
    print()
    print("           GAME OVER")
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            print("Black wins by checkmate!")
        else:
            print("White wins by checkmate!")
    elif board.is_stalemate():
        print("Draw by stalemate.")
    elif board.is_insufficient_material():
        print("Draw by insufficient material.")
    elif board.is_fivefold_repetition():
        print("Draw by repetition.")
    elif board.is_seventyfive_moves():
        print("Draw by 75-move rule.")

if __name__ == "__main__":
    main()