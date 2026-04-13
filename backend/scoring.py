def evaluate_board(board):
    """
    Checks the classical board state for a winner.
    The board is a list of 9 elements. Each element is either a list (spooky)
    or a single string (collapsed/permanent mark).
    """
    # 1. Flatten the board to only consider permanent (collapsed) marks
    flat_board = []
    for cell in board:
        if isinstance(cell, str) and cell in ['X', 'O']:
            flat_board.append(cell)
        else:
            flat_board.append(None)

    # 2. Winning combinations
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]

    for a, b, c in wins:
        if flat_board[a] and flat_board[a] == flat_board[b] == flat_board[c]:
            return flat_board[a]
    return None
