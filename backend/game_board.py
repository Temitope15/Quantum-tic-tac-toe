from typing import List

class GameBoard:
    """
    This class manages the Tic-Tac-Toe board.
    It tells us what is in each square and how to draw the board on the screen.
    """

    def __init__(self) -> None:
        """
        This is the 'setup' method. It runs when we first create a GameBoard.
        """
        # The board is a list of 9 squares (index 0 to 8).
        # We start with 9 empty lists. An empty list [ ] means the square is empty.
        # We use lists because one square might have multiple marks later (Quantum rules!).
        self.board: List[List[str]] = [[], [], [], [], [], [], [], [], []]

    def make_move(self, player_mark: str, cell_index: int) -> None:
        """
        This method adds a mark (like 'X1' or 'O2') to a square.
        """
        # First, check if the index is valid (must be between 0 and 8).
        if 0 <= cell_index < 9:
            if isinstance(self.board[cell_index], list):
                self.board[cell_index].append(player_mark)
            else:
                print(f"Note: Square {cell_index} is fixed.")
        else:
            # If the index is wrong, print an error message.
            print(f"Error: {cell_index} is not a valid square. Use 0 to 8.")

    def is_full(self) -> bool:
        """
        This checks if every square has at least one mark.
        """
        # We check every cell in the board.
        # If every cell has a length greater than 0, the board is 'full'.
        for cell in self.board:
            if len(cell) == 0:
                # If we find even one empty cell, the board is NOT full.
                return False
        return True

    def display_board(self) -> None:
        """
        This method draws the board in the terminal.
        We want the squares to line up perfectly even if they have lots of text.
        """
        
        # --- STEP 1: Prepare the text for each square ---
        # We want to turn each list of marks into a single string.
        # Example: ['X1', 'O2'] becomes "X1, O2".
        cell_strings = []
        for cell in self.board:
            if len(cell) == 0:
                # If the square is empty, we just use a space " "
                cell_strings.append(" ")
            else:
                # If it has marks, we join them together with a comma and space.
                marks_as_string = ", ".join(cell)
                cell_strings.append(marks_as_string)
        
        # --- STEP 2: Figure out how wide each square should be ---
        # We look at all 9 squares and find the one with the most text.
        # This helps us keep the borders straight.
        max_length = 0
        for s in cell_strings:
            if len(s) > max_length:
                max_length = len(s)
        
        # We want at least 3 spaces of width so it doesn't look too squished.
        if max_length < 3:
            max_length = 3
            
        # --- STEP 3: Draw the board row by row ---
        
        # A helper 'function' to format one row of 3 squares.
        def get_formatted_row(index1, index2, index3):
            # .center(max_length) adds spaces to the left and right to center the text.
            s1 = cell_strings[index1].center(max_length)
            s2 = cell_strings[index2].center(max_length)
            s3 = cell_strings[index3].center(max_length)
            # We use | to separate the squares.
            return f" {s1} | {s2} | {s3} "

        # Create a line of dashes to separate the rows.
        # The number of dashes depends on how wide our squares are.
        divider_line = "-" * (max_length * 3 + 8)

        # Print everything to the screen.
        print(f"\n{get_formatted_row(0, 1, 2)}") # Top row (squares 0, 1, 2)
        print(divider_line)
        print(f"{get_formatted_row(3, 4, 5)}") # Middle row (squares 3, 4, 5)
        print(divider_line)
        print(f"{get_formatted_row(6, 7, 8)}") # Bottom row (squares 6, 7, 8)
        print()

# This part only runs if we run this file directly (not if we import it).
if __name__ == "__main__":
    # 1. Create a new board object
    my_game = GameBoard()

    # 2. Add some test marks
    print("--- Adding some marks to the board ---")
    my_game.make_move("X1", 0)  # Put X1 in the top-left (index 0)
    my_game.make_move("O2", 4)  # Put O2 in the center (index 4)
    my_game.make_move("X3", 8)  # Put X3 in the bottom-right (index 8)
    my_game.make_move("O4", 8)  # Also put O4 in the bottom-right (index 8)
    
    # 3. Show the board!
    my_game.display_board()

    # 4. Check if the board is full
    if my_game.is_full():
        print("Result: All squares have at least one mark.")
    else:
        print("Result: There are still some empty squares.")
