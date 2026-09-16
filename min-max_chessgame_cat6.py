import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate_board(board: chess.Board) -> int:
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
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

def minimax(board: chess.Board, depth: int, is_maximizing: bool) -> int:
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if is_maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, evaluation)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            evaluation = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, evaluation)
        return min_eval

def find_best_move(board: chess.Board, depth: int) -> chess.Move:
    best_move = None
    is_maximizing = (board.turn == chess.WHITE)
    
    if is_maximizing:
        best_score = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, False)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = float('inf')
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, True)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move

    print(f"Engine evaluated position score: {best_score}")
    return best_move

if __name__ == "__main__":
    board = chess.Board()
    depth_level = 3
    print(f"Calculating best move for White at depth {depth_level}...")
    best_move = find_best_move(board, depth_level)
    print(f"Recommended Move: {best_move}")