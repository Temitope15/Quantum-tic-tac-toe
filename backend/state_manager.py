from typing import List, Optional, Union, Tuple
from game_board import GameBoard
from q_backend import QuantumGameBackend
from collapse_manager import GraphState, trigger_collapse
from scoring import evaluate_board
from bot_player import QuantumBot

class GameManager:
    """Orchestrates the Quantum Tic-Tac-Toe game mechanics.

    This class serves as the 'Controller' in the MVC pattern, unifying 
    the board state, quantum engine, graph logic, and AI interactions.

    Attributes:
        board (GameBoard): The 3x3 grid state.
        q_backend (QuantumGameBackend): The quantum circuit engine.
        graph (GraphState): Entanglement relationship tracker.
        current_player (str): Either 'X' or 'O'.
        move_index (int): total moves made.
        status (str): Current game status message.
        game_mode (str): 'PvP' or 'PvE'.
        player_mark (str): The human's chosen mark.
        bot_mark (str): The AI's mark.
        bot (Optional[QuantumBot]): The AI agent if in PvE mode.
    """

    def __init__(self, mode: str = "PvE", player_mark: str = "X") -> None:
        """Initializes a new game session."""
        self.reset(mode, player_mark)

    def reset(self, mode: str = "PvE", player_mark: str = "X") -> None:
        """Resets the game to a fresh state.

        Args:
            mode: 'PvP' or 'PvE'.
            player_mark: The humans mark ('X' or 'O').
        """
        self.board = GameBoard()
        self.q_backend = QuantumGameBackend()
        self.graph = GraphState()
        self.current_player = 'X'
        self.move_index = 0
        self.status = "ongoing"
        self.game_mode = mode
        self.player_mark = player_mark
        self.bot_mark = 'O' if player_mark == 'X' else 'X'
        self.bot = QuantumBot(mark=self.bot_mark) if mode == "PvE" else None
        
        # If Bot is 'X' and PvE, it should move first
        if self.bot and self.bot_mark == "X":
            self.execute_bot_move()

    def execute_bot_move(self) -> None:
        """Triggers the AI agent to calculate and perform a move."""
        if not self.bot:
            return

        valid_squares = [i for i, cell in enumerate(self.board.board) if isinstance(cell, list)]
        if len(valid_squares) >= 2:
            move = self.bot.get_move(self.board.board, self.graph, valid_squares)
            if move:
                self.process_move(move[0], move[1], self.bot_mark)
            else:
                self.status = "Stalemate!"
        else:
            self.status = "Draw!"

    def process_move(self, s1: int, s2: int, player: str) -> None:
        """Processes a single quantum move (entangling two squares).

        Args:
            s1: Index of first square.
            s2: Index of second square.
            player: Mark of the player making the move.
        """
        if self.status != "ongoing":
            return

        # 1. Apply Move
        spooky_mark = f"{player}{self.move_index}"
        self.board.make_move(spooky_mark, s1)
        self.board.make_move(spooky_mark, s2)
        self.q_backend.make_spooky_move(self.move_index, s1, s2)
        self.graph.add_edge(s1, s2, self.move_index)

        # 2. Check for Collapses
        cycle_moves = self.graph.detect_cycle()
        if cycle_moves:
            resolution = trigger_collapse(self.q_backend, cycle_moves)
            self._resolve_collapse(resolution, cycle_moves)

        # 3. Update State
        winner = evaluate_board(self.board.board)
        if winner:
            self.status = f"Player {winner} wins!"
        elif all(isinstance(c, str) for c in self.board.board):
            self.status = "Draw!"
        
        self.move_index += 1
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def _resolve_collapse(self, resolution: dict, cycle_moves: list) -> None:
        """Internal helper to apply quantum measurement results to the board.

        Args:
            resolution: Move ID -> Square Index mapping.
            cycle_moves: List of (u, v, move_id) tuples in the cycle.
        """
        for m_id, chosen_square in resolution.items():
            target_mark = None
            # Find the mark prefix ('X' or 'O') for this move
            for cell in self.board.board:
                if isinstance(cell, list):
                    for m in cell:
                        if m.endswith(str(m_id)):
                            target_mark = m[0]
                            break
                if target_mark: break
            
            if not target_mark: continue

            # Apply solid mark
            self.board.board[chosen_square] = target_mark
            
            # Remove ghost marks of resolved move from elsewhere
            for i in range(9):
                cell = self.board.board[i]
                if isinstance(cell, list):
                    self.board.board[i] = [m for m in cell if not m.endswith(str(m_id))]

        # Clear cycle from graph
        for u, v, m_id in cycle_moves:
            self.graph.remove_edge(u, v)
