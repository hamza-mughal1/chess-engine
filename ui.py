import pygame
import chess

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
COLORS = [(240, 217, 181), (181, 136, 99)] # Light, Dark
HIGHLIGHT_COLOR = (130, 151, 105) # Modern green highlight

# Piece Unicode
PIECE_SYMBOLS = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
}

class ChessUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Chess")
        self.clock = pygame.time.Clock()
        
        # Try to find a font that supports chess symbols
        self.font = None
        fonts = ["segoeuisymbol", "dejavusans", "freeserif", "arial"]
        for f in fonts:
            if f in pygame.font.get_fonts():
                self.font = pygame.font.SysFont(f, 60)
                break
        if not self.font:
            self.font = pygame.font.Font(None, 60)

        self.selected_square = None
        self.valid_moves = []
        
        # Threading state
        self.thinking = False
        self.ai_result = None

    def draw_board(self, board, player_color=chess.WHITE):
        for row in range(8):
            for col in range(8):               
                display_row = row
                display_col = col
                
                if player_color == chess.BLACK:
                    rank = row 
                    file = 7 - col
                    # Calculate square 0-63
                    square = chess.square(file, rank)
                else: 
                    # Default: White at bottom
                    rank = 7 - row
                    file = col
                    square = chess.square(file, rank)
                
                # Color
                color = COLORS[(display_row + display_col) % 2]
                pygame.draw.rect(self.screen, color, (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # Selection Highlight
                if self.selected_square == square:
                    pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # Move Highlights
                if any(m.to_square == square for m in self.valid_moves):
                    center = (display_col * SQUARE_SIZE + SQUARE_SIZE // 2, display_row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.circle(self.screen, (0, 0, 0, 30), center, 10)

                # Piece
                piece = board.piece_at(square)
                if piece:
                    symbol = PIECE_SYMBOLS.get(piece.symbol())
                    text = self.font.render(symbol, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(display_col * SQUARE_SIZE + SQUARE_SIZE // 2, display_row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    self.screen.blit(text, text_rect)

    def get_square_under_mouse(self, player_color=chess.WHITE):
        mouse_pos = pygame.mouse.get_pos()
        col = mouse_pos[0] // SQUARE_SIZE
        row = mouse_pos[1] // SQUARE_SIZE
        
        if 0 <= col < 8 and 0 <= row < 8:
            if player_color == chess.BLACK:
                return chess.square(7 - col, row)
            else:
                return chess.square(col, 7 - row)
        return None

    def update_selection(self, board, player_color=chess.WHITE):
        clicked_square = self.get_square_under_mouse(player_color)
        if clicked_square is None:
            return None

        # If already selected, try to move
        if self.selected_square is not None:
            move = chess.Move(self.selected_square, clicked_square)
            # Handle promotion automatically for now
            promotion_move = chess.Move(self.selected_square, clicked_square, promotion=chess.QUEEN)
            
            if move in board.legal_moves:
                self.selected_square = None
                self.valid_moves = []
                return move
            elif promotion_move in board.legal_moves:
                self.selected_square = None
                self.valid_moves = []
                return promotion_move

        # Otherwise, select the new square if it's our piece
        piece = board.piece_at(clicked_square)
        if piece and piece.color == board.turn:
            self.selected_square = clicked_square
            self.valid_moves = [m for m in board.legal_moves if m.from_square == clicked_square]
        else:
            self.selected_square = None
            self.valid_moves = []
        
        return None
