from evaluation import evaluate_board
import chess
import random

# Zobrist Initialization
ZOBRIST_TABLE = [[random.getrandbits(64) for _ in range(12)] for _ in range(64)]
ZOBRIST_BLACK_TURN = random.getrandbits(64)

class SearchEngine:
    def __init__(self, depth):
        self.depth = depth
        self.nodes_visited = 0
        self.transposition_table = {} # Key -> {depth, score, flag}
        self.used_cache_moves = 0

    def compute_hash(self, board):
        h = 0
        for square, piece in board.piece_map().items():
            idx = (piece.piece_type - 1) + (6 * int(piece.color))
            h ^= ZOBRIST_TABLE[square][idx]
        
        if board.turn == chess.BLACK:
            h ^= ZOBRIST_BLACK_TURN
            
        return h

    def get_best_move(self, board):
        self.used_cache_moves = 0
        self.nodes_visited = 0
        
        best_move = None
        
        # Iterative Deepening
        for current_depth in range(1, self.depth + 1):
            move = self.search_root(board, current_depth)
            if move:
                best_move = move
                
        print("Length of transposition table: ", len(self.transposition_table))
        print("Used cache moves: ", self.used_cache_moves)
        return best_move, self.nodes_visited

    def search_root(self, board, depth):
        best_move = None
        max_eval = -float('inf') if board.turn == chess.WHITE else float('inf')
        
        alpha = -float('inf')
        beta = float('inf')

        moves = self.order_moves(board)

        for move in moves:
            board.push(move)
            eval = self.minimax(board, depth - 1, alpha, beta, board.turn == chess.WHITE)
            board.pop()

            if board.turn == chess.WHITE:
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
            else: # Black's turn
                if eval < max_eval:
                    max_eval = eval
                    best_move = move
                beta = min(beta, eval)
        
        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        self.nodes_visited += 1
        
        # 1. Transposition Table Probe
        board_hash = self.compute_hash(board)
        tt_entry = self.transposition_table.get(board_hash)
        
        if tt_entry and tt_entry['depth'] >= depth:
             if tt_entry['flag'] == 'exact':
                 self.used_cache_moves += 1
                 return tt_entry['score']
             elif tt_entry['flag'] == 'lowerbound': # Alpha
                 alpha = max(alpha, tt_entry['score'])
             elif tt_entry['flag'] == 'upperbound': # Beta
                 beta = min(beta, tt_entry['score'])
             
             if alpha >= beta:
                 return tt_entry['score']

        if depth == 0 or board.is_game_over():
            return self.quiescence(board, alpha, beta)

        original_alpha = alpha
        moves = self.order_moves(board)
        
        if maximizing_player:
            max_eval = -float('inf')
            for move in moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            
            # Store in TT
            flag = 'exact'
            if max_eval <= original_alpha: flag = 'upperbound' # Fail low
            elif max_eval >= beta: flag = 'lowerbound' # Fail high
            
            self.transposition_table[board_hash] = {'depth': depth, 'score': max_eval, 'flag': flag}
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            
            # Store in TT
            flag = 'exact'
            if min_eval <= original_alpha: flag = 'upperbound'
            elif min_eval >= beta: flag = 'lowerbound'
            
            self.transposition_table[board_hash] = {'depth': depth, 'score': min_eval, 'flag': flag}
            return min_eval

    def quiescence(self, board, alpha, beta):
        self.nodes_visited += 1
        
        # Stand-pat score: What is the score if we just stop capturing?
        stand_pat = evaluate_board(board)
        
        if board.turn == chess.WHITE:
            if stand_pat >= beta:
                return beta
            if alpha < stand_pat:
                alpha = stand_pat
        else:
            if stand_pat <= alpha:
                return alpha
            if beta > stand_pat:
                beta = stand_pat

        # Generate ONLY captures
        moves = self.order_moves(board, only_captures=True)
        
        if board.turn == chess.WHITE:
            for move in moves:
                board.push(move)
                score = self.quiescence(board, alpha, beta)
                board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
            return alpha
        else:
            for move in moves:
                board.push(move)
                score = self.quiescence(board, alpha, beta)
                board.pop()

                if score <= alpha:
                    return alpha
                if score < beta:
                    beta = score
            return beta

    def order_moves(self, board, only_captures=False):
        """
        Orders moves to improve alpha-beta pruning.
        Prioritizes:
        1. Captures (MVV-LVA: Most Valuable Victim - Least Valuable Aggressor)
        2. Promotions
        """
        moves = list(board.legal_moves)
        scores = []
        
        final_moves = []
        final_scores = []
        
        for move in moves:
            if only_captures and not board.is_capture(move):
                continue
                
            score = 0
            
            # 1. Captures
            if board.is_capture(move):
                # MVV-LVA
                victim_piece = board.piece_at(move.to_square)
                aggressor_piece = board.piece_at(move.from_square)
                
                victim_value = 0
                if victim_piece:
                    # Use values from evaluation.py (need to import or redefine)
                    values = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9, 6: 100}
                    victim_value = values.get(victim_piece.piece_type, 0)
                
                aggressor_value = 0
                if aggressor_piece:
                    values = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9, 6: 100}
                    aggressor_value = values.get(aggressor_piece.piece_type, 0)
                
                score = 10 * victim_value - aggressor_value
            
            # 2. Promotions
            if move.promotion:
                score += 900
            
            final_moves.append(move)
            final_scores.append(score)
            
        # Zipping and sorting
        moves_with_scores = zip(final_moves, final_scores)
        sorted_moves = sorted(moves_with_scores, key=lambda x: x[1], reverse=True)
        return [m[0] for m in sorted_moves]
