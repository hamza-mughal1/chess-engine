from logic import GameLogic
from search import SearchEngine
from ui import ChessUI
import chess
import pygame

def main():
    game = GameLogic()
    engine = SearchEngine(depth=4)
    ui = ChessUI()

    # Select Color
    while True:
        choice = input("Play as (w)hite or (b)lack? ").lower()
        if choice in ['w', 'b']:
            player_color = chess.WHITE if choice == 'w' else chess.BLACK
            break
            
    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and game.get_board().turn == player_color:
                move = ui.update_selection(game.get_board(), player_color)
                if move:
                    game.make_move(move)

        # 2. AI Turn logic
        # Check for AI Result FIRST
        if hasattr(ui, 'ai_result') and ui.ai_result:
            move_uci, nodes, duration = ui.ai_result
            ui.ai_result = None # Reset
            
            if move_uci:
                # Re-create move object bound to the current board state
                ai_move = chess.Move.from_uci(move_uci)
                if ai_move in game.get_board().legal_moves:
                    game.make_move(ai_move)
                print(f"AI Move: {ai_move} | Nodes: {nodes} | Time: {duration:.3f}s | NPS: {int(nodes/duration) if duration > 0 else 0}")
       
        # Check if we need to start AI thread
        if not game.is_game_over() and game.get_board().turn != player_color:
            if not getattr(ui, 'thinking', False):
                ui.thinking = True
                
                # Start AI in a separate thread
                import threading
                def ai_task():
                    import time
                    start_time = time.perf_counter()
                    # Copy board for thread safety
                    board_copy = game.get_board().copy()
                    best_move, nodes = engine.get_best_move(board_copy)
                    duration = time.perf_counter() - start_time
                    
                    # Convert move to UCI string to pass safely between threads/contexts
                    move_uci = best_move.uci() if best_move else None
                    ui.ai_result = (move_uci, nodes, duration)
                    ui.thinking = False

                threading.Thread(target=ai_task, daemon=True).start()
                    
        # 3. Drawing
        ui.draw_board(game.get_board(), player_color)
        
        if getattr(ui, 'thinking', False):
            font = pygame.font.Font(None, 40)
            text = font.render("AI is thinking...", True, (50, 50, 50))
            rect = text.get_rect(center=(300, 300))
            ui.screen.blit(text, rect)
        
        # Check Winner
        if game.is_game_over():
             font = pygame.font.Font(None, 60)
             if game.get_board().is_checkmate():
                 winner = "Black" if game.get_board().turn == chess.WHITE else "White"
                 text = font.render(f"Checkmate! {winner} Wins!", True, (200, 50, 50))
             else:
                 text = font.render("Draw / Stalemate", True, (50, 50, 200))
             
             rect = text.get_rect(center=(400, 400))
             ui.screen.blit(text, rect)

             # Print FEN once
             if not getattr(game, 'fen_printed', False):
                 print("\nGame Over!")
                 print(f"Final FEN: {game.get_board().fen()}")
                 game.fen_printed = True

        pygame.display.flip()
        ui.clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
