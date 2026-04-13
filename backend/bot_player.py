import random
import time

class QuantumBot:
    """
    Fearless AI for Quantum Tic-Tac-Toe using the 'Parasite Strategy'.
    Avoids heavy simulations in favor of heuristic graph analysis.
    """

    def __init__(self, mark='O', mistake_chance=0.10):
        self.mark = mark
        self.opponent_mark = 'X' if mark == 'O' else 'O'
        self.mistake_chance = mistake_chance
        # Define winning combinations
        self.winning_lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Cols
            (0, 4, 8), (2, 4, 6)             # Diagonals
        ]

    def simulate_thinking(self):
        """Simulate the computer 'calculating' its move."""
        print("Computer is calculating quantum probabilities...")
        time.sleep(1.5)

    def _has_mark(self, square_content, player_mark):
        """Check if a square contains a mark for a specific player."""
        # Fixed mark
        if isinstance(square_content, str):
            return square_content == player_mark
        # Spooky marks
        if isinstance(square_content, list):
            return any(mark.startswith(player_mark) for mark in square_content)
        return False

    def get_move(self, classical_board, graph_state, valid_squares):
        """
        Determines the best two squares to entangle based on the Parasite Strategy.
        """
        # Step 1: Human Error Check
        if random.random() < self.mistake_chance:
            print("🤖 AI blundered! Making a random move...")
            return tuple(random.sample(valid_squares, 2))

        # Helper to get squares in a line that have marks for a player
        def get_player_marks_in_line(line, player_mark):
            return [s for s in line if self._has_mark(classical_board[s], player_mark)]

        # --- Priority 1: Kill (Win/Collapse) ---
        # Look for a line where 'O' already has 2 squares marked.
        for line in self.winning_lines:
            my_marks = get_player_marks_in_line(line, self.mark)
            if len(my_marks) == 2:
                # Entangle the two squares that have marks to potentially trigger a cycle/collapse
                s1, s2 = my_marks
                # Ensure they are valid (not collapsed)
                if s1 in valid_squares and s2 in valid_squares:
                    return (s1, s2)

        # --- Priority 2: Disrupt (Block) ---
        # Look for a line where 'X' has 2 squares marked.
        for line in self.winning_lines:
            opponent_marks = get_player_marks_in_line(line, self.opponent_mark)
            if len(opponent_marks) == 2:
                # Poison one of these squares by entangling it with a random empty square (preferably a corner)
                target = random.choice(opponent_marks)
                if target in valid_squares:
                    corners = [0, 2, 6, 8]
                    valid_corners = [c for c in corners if c in valid_squares and c != target]
                    if valid_corners:
                        return (target, random.choice(valid_corners))
                    else:
                        # Fallback to any random square if no corners available
                        others = [s for s in valid_squares if s != target]
                        if others:
                            return (target, random.choice(others))

        # --- Priority 3: Parasite (Chaos) ---
        # Entangle the most connected node in the graph state.
        degrees = {node: len(graph_state.adj[node]) for node in valid_squares}
        if degrees:
            # Get node(s) with max degree
            max_deg = max(degrees.values())
            best_nodes = [node for node, deg in degrees.items() if deg == max_deg]
            target = random.choice(best_nodes)
            
            # Entangle it with another random valid square
            others = [s for s in valid_squares if s != target]
            if others:
                return (target, random.choice(others))

        # --- Fallback: Random ---
        if len(valid_squares) >= 2:
            return tuple(random.sample(valid_squares, 2))
        return None
