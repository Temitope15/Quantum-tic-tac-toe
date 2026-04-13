import sys
import time
from typing import Optional
from state_manager import GameManager

def main() -> None:
    """Main entry point for the CLI version of Quantum Tic-Tac-Toe."""
    print("\n" + "="*40)
    print("      QUANTUM TIC-TAC-TOE (CLI)      ")
    print("="*40)
    
    print("\nSelect Game Mode:")
    print("1. Playing with a friend (PvP)")
    print("2. Challenge the Quantum AI (PvE)")
    choice = input("\nEnter choice (1/2): ").strip()
    
    mode = "PvE" if choice == '2' else "PvP"
    game = GameManager(mode=mode)
    
    print(f"\nGame Initialized: {mode} Mode")
    if mode == "PvE":
        print(f"You are '{game.player_mark}', AI is '{game.bot_mark}'.")

    while game.status == "ongoing":
        game.board.display_board()
        
        valid_squares = [i for i, cell in enumerate(game.board.board) if isinstance(cell, list)]
        if len(valid_squares) < 2:
            print("\n🤝 Stalemate: Not enough squares for entanglement!")
            break

        print(f"\n>>> Player {game.current_player}'s Turn")
        
        try:
            line = input("Enter two squares to entangle (0-8, e.g. '0 4'): ").strip()
            parts = line.split()
            if len(parts) != 2: raise ValueError()
            s1, s2 = map(int, parts)
            
            if not (0 <= s1 <= 8 and 0 <= s2 <= 8) or s1 == s2:
                print("❌ Points must be unique and between 0-8.")
                continue
                
            if isinstance(game.board.board[s1], str) or isinstance(game.board.board[s2], str):
                print("❌ One of those squares is already collapsed!")
                continue
        except (ValueError, IndexError):
            print("❌ Invalid input. Please enter two numbers separated by a space.")
            continue

        # Process move
        game.process_move(s1, s2, game.current_player)
        
        # If PvE, bot move is handled automatically by GameManager but we can add simulation delay
        if game.game_mode == "PvE" and game.status == "ongoing" and game.current_player == game.bot_mark:
            print("\n🤖 AI is analyzing quantum wavefunctions...")
            time.sleep(1)
            game.execute_bot_move()

    game.board.display_board()
    print(f"\n*** GAME OVER: {game.status} ***\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting... See you in another reality.")
        sys.exit(0)
