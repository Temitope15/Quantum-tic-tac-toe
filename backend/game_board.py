from typing import List, Union

class GameBoard:
    """Manages the state and representation of the 3x3 Tic-Tac-Toe grid.

    This class handles the storage of both 'ghost' marks (lists) and 
    solid marks (strings) and provides a terminal-based visualization.

    Attributes:
        board (List[Union[List[str], str]]): The 3x3 grid stored as a flat list.
    """

    def __init__(self) -> None:
        """Initializes an empty 3x3 game board."""
        self.board: List[Union[List[str], str]] = [[] for _ in range(9)]

    def make_move(self, player_mark: str, cell_index: int) -> None:
        """Adds a mark to a specific square.

        Args:
            player_mark (str): The mark to add (e.g., 'X1', 'O2').
            cell_index (int): The square index (0-8).
        """
        if 0 <= cell_index < 9:
            cell = self.board[cell_index]
            if isinstance(cell, list):
                cell.append(player_mark)
            else:
                # Square is already collapsed/solid
                pass
        else:
            raise ValueError(f"Invalid cell index: {cell_index}")

    def is_full(self) -> bool:
        """Checks if all squares on the board contain at least one mark.

        Returns:
            bool: True if every square is occupied, False otherwise.
        """
        return all(len(cell) > 0 if isinstance(cell, list) else True for cell in self.board)

    def display_board(self) -> None:
        """Prints a formatted representation of the board to the console."""
        cell_strings = []
        for cell in self.board:
            if isinstance(cell, list):
                if not cell:
                    cell_strings.append(" ")
                else:
                    cell_strings.append(", ".join(cell))
            else:
                cell_strings.append(cell)
        
        max_length = max(len(s) for s in cell_strings)
        max_length = max(3, max_length)
            
        def get_formatted_row(i1: int, i2: int, i3: int) -> str:
            s1 = cell_strings[i1].center(max_length)
            s2 = cell_strings[i2].center(max_length)
            s3 = cell_strings[i3].center(max_length)
            return f" {s1} | {s2} | {s3} "

        divider = "-" * (max_length * 3 + 8)

        print(f"\n{get_formatted_row(0, 1, 2)}")
        print(divider)
        print(f"{get_formatted_row(3, 4, 5)}")
        print(divider)
        print(f"{get_formatted_row(6, 7, 8)}\n")

if __name__ == "__main__":
    test_board = GameBoard()
    test_board.make_move("X1", 0)
    test_board.make_move("O2", 4)
    test_board.display_board()
