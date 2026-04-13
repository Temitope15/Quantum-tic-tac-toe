from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time

from game_board import GameBoard
from q_backend import QuantumGameBackend
from collapse_manager import GraphState, trigger_collapse
from scoring import evaluate_board
from bot_player import QuantumBot

app = FastAPI(title="Quantum Tic-Tac-Toe API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game State Management
class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = GameBoard()
        self.q_backend = QuantumGameBackend()
        self.graph = GraphState()
        self.current_player = 'X'
        self.move_index = 0
        self.status = "ongoing"
        self.bot = QuantumBot(mark='O', mistake_chance=0.10)

game = GameState()

class MoveRequest(BaseModel):
    square_1: int
    square_2: int

@app.get("/state")
async def get_state():
    return {
        "board": game.board.board,
        "current_player": game.current_player,
        "status": game.status
    }

@app.post("/reset")
async def reset_game():
    game.reset()
    return await get_state()

def process_move(s1: int, s2: int, player: str):
    if not (0 <= s1 <= 8 and 0 <= s2 <= 8) or s1 == s2:
        raise HTTPException(status_code=400, detail="Invalid squares")
    
    if isinstance(game.board.board[s1], str) or isinstance(game.board.board[s2], str):
        raise HTTPException(status_code=400, detail="Square already collapsed")

    spooky_mark = f"{player}{game.move_index}"
    game.board.make_move(spooky_mark, s1)
    game.board.make_move(spooky_mark, s2)
    game.q_backend.make_spooky_move(game.move_index, s1, s2)
    game.graph.add_edge(s1, s2, game.move_index)

    cycle = game.graph.detect_cycle()
    if cycle:
        results = trigger_collapse(game.q_backend, cycle)
        for square in cycle:
            bit = results[square]
            if bit == 1:
                game.board.board[square] = player
            else:
                game.board.board[square] = []
        
        # Remove cycle edges
        for i in range(len(cycle)):
            u, v = cycle[i], cycle[(i+1)%len(cycle)]
            game.graph.remove_edge(u, v)

    # Check winner
    winner = evaluate_board(game.board.board)
    if winner:
        game.status = f"Player {winner} wins!"
    elif all(isinstance(c, str) for c in game.board.board):
        game.status = "Draw!"
    
    game.move_index += 1
    game.current_player = 'O' if game.current_player == 'X' else 'X'

@app.post("/move")
async def make_move(request: MoveRequest):
    if game.status != "ongoing":
        raise HTTPException(status_code=400, detail="Game already finished")

    # Human Move (X)
    process_move(request.square_1, request.square_2, 'X')

    # AI Turn (O) if game still ongoing
    if game.status == "ongoing":
        valid_squares = [i for i, cell in enumerate(game.board.board) if isinstance(cell, list)]
        if len(valid_squares) >= 2:
            ai_move = game.bot.get_move(game.board.board, game.graph, valid_squares)
            if ai_move:
                s1, s2 = ai_move
                process_move(s1, s2, 'O')
            else:
                game.status = "Stalemate!"
        else:
            game.status = "Draw/Stalemate!"

    return await get_state()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
