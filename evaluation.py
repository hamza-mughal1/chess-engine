import chess

# Material weights
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Piece-Square Tables (PST)
# Values are for WHITE. For BLACK, we mirror the square index (flip rank).

pawntable = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,-20,-20, 10, 10,  5,
    5, -5,-10,  0,  0,-10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0]

knighttable = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50]

bishoptable = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20]

rooktable = [
    0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0]

queentable = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,   0,  5,  5,  5,  5,  0, -5,
    0,    0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20]

kingtable = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30]

def evaluate_board(board):
    """
    Returns a score from White's perspective.
    Positive = White advantage, Negative = Black advantage.
    """
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -99999
        else:
            return 99999
    
    if board.is_game_over():
        return 0

    score = 0
    piece_map = board.piece_map()
    
    for square, piece in piece_map.items():
        # Material
        val = PIECE_VALUES.get(piece.piece_type, 0)
        
        # Position
        pst_val = 0
        
        # White Piece
        if piece.color == chess.WHITE:
            if piece.piece_type == chess.PAWN: pst_val = pawntable[square]
            elif piece.piece_type == chess.KNIGHT: pst_val = knighttable[square]
            elif piece.piece_type == chess.BISHOP: pst_val = bishoptable[square]
            elif piece.piece_type == chess.ROOK: pst_val = rooktable[square]
            elif piece.piece_type == chess.QUEEN: pst_val = queentable[square]
            elif piece.piece_type == chess.KING: pst_val = kingtable[square]
            
            score += val + pst_val
            
        # Black Piece
        else:
            # Mirror the square for Black to use the same table
            mirror_square = chess.square_mirror(square)
            
            if piece.piece_type == chess.PAWN: pst_val = pawntable[mirror_square]
            elif piece.piece_type == chess.KNIGHT: pst_val = knighttable[mirror_square]
            elif piece.piece_type == chess.BISHOP: pst_val = bishoptable[mirror_square]
            elif piece.piece_type == chess.ROOK: pst_val = rooktable[mirror_square]
            elif piece.piece_type == chess.QUEEN: pst_val = queentable[mirror_square]
            elif piece.piece_type == chess.KING: pst_val = kingtable[mirror_square]
            
            score -= (val + pst_val)
            
    return score
