import time
import sys
from game_board import GameBoard
from q_backend import QuantumGameBackend
from collapse_manager import GraphState, trigger_collapse
from scoring import evaluate_board
from bot_player import QuantumBot

def main():
    board = GameBoard()
    q_backend = QuantumGameBackend()
    graph = GraphState()
    current_player, move_index = 'X', 0

    # Store player for each move index
    move_to_player = {}

    print("\n=== QUANTUM TIC-TAC-TOE  ===")
    
    print("Select Mode:")
    print("1. Human vs. Human")
    print("2. Human vs. Computer")
    mode = input("Choice (1/2): ").strip()
    
    bot = None
    if mode == '2':
        bot = QuantumBot(mark='O', mistake_chance=0.10)
        print("Computer Agent Initialized. You are 'X', Computer is 'O'.")
    while True:
        board.display_board()
        valid_squares = [i for i, cell in enumerate(board.board) if isinstance(cell, list)]
        
        # Stalemate check: Need at least 2 uncollapsed squares for a spooky move
        if len(valid_squares) < 2:
            print("🤝 Stalemate! Not enough squares left for quantum entanglement.")
            break

        print(f"--- Player {current_player}'s Turn (Move {move_index+1}) ---")
        
        if bot and current_player == 'O':
            # AI's Turn
            bot.simulate_thinking()
            move = bot.get_move(board.board, graph, valid_squares)
            if not move:
                print("🤖 AI has no valid moves left!")
                break
            s1, s2 = move
            print(f"🤖 The AI entangled squares {s1} and {s2}!")
        else:
            # Human's Turn
            try:
                line = input("Enter two squares (0-8): ").strip()
                parts = line.split()
                if len(parts) != 2: raise ValueError()
                s1, s2 = map(int, parts)
                if not (0 <= s1 <= 8 and 0 <= s2 <= 8) or s1 == s2: raise ValueError()
                if isinstance(board.board[s1], str) or isinstance(board.board[s2], str):
                    print("❌ Square already collapsed!")
                    continue
            except:
                print("❌ Invalid input. Use '0 1'.")
                continue

        spooky_mark = f"{current_player}{move_index}"
        move_to_player[move_index] = current_player
        
        board.make_move(spooky_mark, s1)
        board.make_move(spooky_mark, s2)
        q_backend.make_spooky_move(move_index, s1, s2)
        graph.add_edge(s1, s2, move_index)

        cycle = graph.detect_cycle()
        if cycle:
            print(f"\n⚠️  CYCLE DETECTED: {cycle}. COLLAPSING...")
            time.sleep(1)
            results = trigger_collapse(q_backend, cycle)
            
            for square in cycle:
                bit = results[square]
                if bit == 1:
                    # Assign the mark of the player who triggered the collapse or most recent
                    # Standard rule: identify which move inside the cycle lands here.
                    # For simplicity, we use the current player's mark.
                    board.board[square] = current_player
                else:
                    # Clear square of marks involved in cycle.
                    # (In this simple version, we'll clear it and assume other marks 
                    # either moved elsewhere or were part of the cycle).
                    board.board[square] = []
                
            # --- FIX 1: Remove only cycle edges ---
            for i in range(len(cycle)):
                u, v = cycle[i], cycle[(i+1)%len(cycle)]
                graph.remove_edge(u, v)
            
            print("Collapse complete.\n")

        winner = evaluate_board(board.board)
        if winner:
            board.display_board()
            print(f"🏆 PLAYER {winner} WINS!")
            return

        current_player = 'O' if current_player == 'X' else 'X'
        move_index += 1

    print("Game Over.")

if __name__ == "__main__":
    main()
