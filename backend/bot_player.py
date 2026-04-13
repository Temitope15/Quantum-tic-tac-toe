import random
from typing import List, Optional, Tuple, Union
from collapse_manager import GraphState

class QuantumBot:
    """Heuristic AI agent for Quantum Tic-Tac-Toe.

    Uses the 'Parasite Strategy' to favor disruption and entanglement connectivity 
    over deep simulation, keeping the AI fast and strategically difficult to predict.

    Attributes:
        mark (str): The bot's mark ('X' or 'O').
        opponent_mark (str): The human player's mark.
        mistake_chance (float): Probability (0-1) that the AI will 'blunder' a random move.
    """

    def __init__(self, mark: str = 'O', mistake_chance: float = 0.10) -> None:
        """Initializes the AI agent with specific marks and difficulty."""
        self.mark = mark
        self.opponent_mark = 'X' if mark == 'O' else 'O'
        self.mistake_chance = mistake_chance
        self.win_lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]

    def _has_mark(self, square: Union[List[str], str], target: str) -> bool:
        """Determines if a square contains a mark for the target player.

        Args:
            square: The square content (list for spooky, str for solid).
            target: The player mark prefix ('X' or 'O').

        Returns:
            bool: True if the player has a presence in the square.
        """
        if isinstance(square, str):
            return square == target
        return any(m.startswith(target) for m in square)

    def get_move(self, board: List[Union[List[str], str]], 
                 graph: GraphState, 
                 valid_squares: List[int]) -> Optional[Tuple[int, int]]:
        """Calculates the best two squares to entangle using heuristic priorities.

        Priority order:
        1. Winning: Complete a cycle where the bot already has marks.
        2. Blocking: Disrupt an opponent's pending winning line.
        3. Complexity: Increase entanglement on high-degree nodes.

        Args:
            board: Current board state.
            graph: Current entanglement graph.
            valid_squares: List of indices for squares that haven't collapsed.

        Returns:
            Optional[Tuple[int, int]]: A pair of square indices, or None if no move possible.
        """
        if random.random() < self.mistake_chance:
            return tuple(random.sample(valid_squares, 2)) if len(valid_squares) >= 2 else None

        # --- Priority 1: Winning Path ---
        for line in self.win_lines:
            my_marks = [s for s in line if self._has_mark(board[s], self.mark)]
            valid_my_marks = [s for s in my_marks if s in valid_squares]
            if len(valid_my_marks) >= 2:
                return tuple(random.sample(valid_my_marks, 2))

        # --- Priority 2: Disruption (Blocking) ---
        for line in self.win_lines:
            op_marks = [s for s in line if self._has_mark(board[s], self.opponent_mark)]
            if len(op_marks) >= 2:
                target = random.choice([s for s in op_marks if s in valid_squares] or [None])
                if target is not None:
                    # Pair with a random square that isn't already part of this threat
                    others = [s for s in valid_squares if s != target]
                    if others:
                        return (target, random.choice(others))

        # --- Priority 3: Complexity (Graph Centrality) ---
        degrees = {s: len(graph.adj[s]) for s in valid_squares}
        if degrees:
            max_deg = max(degrees.values())
            candidates = [s for s, d in degrees.items() if d == max_deg]
            target = random.choice(candidates)
            others = [s for s in valid_squares if s != target]
            if others:
                return (target, random.choice(others))

        # --- Fallback ---
        return tuple(random.sample(valid_squares, 2)) if len(valid_squares) >= 2 else None
