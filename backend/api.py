from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional

from state_manager import GameManager

app = FastAPI(
    title="Quantum Tic-Tac-Toe API",
    description="Backend API for the Quantum Tic-Tac-Toe game engine.",
    version="1.0.0"
)

# Global exception handler for industrial stability
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Quantum Anomaly: " + str(exc)},
    )

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global game instance (initialized lazily)
_game_instance: Optional[GameManager] = None

def get_game() -> GameManager:
    """Provides a thread-safe singleton-like instance of the GameManager."""
    global _game_instance
    if _game_instance is None:
        try:
            _game_instance = GameManager()
        except Exception as e:
            # Prevent the server from hanging if initialization fails
            raise HTTPException(
                status_code=503,
                detail=f"Engine initialization failed: {str(e)}"
            )
    return _game_instance

# --- Data Models ---

class MoveRequest(BaseModel):
    square_1: int
    square_2: int

class ResetRequest(BaseModel):
    mode: str = "PvE"
    player_mark: str = "X"

# --- Endpoints ---

@app.get("/state")
async def get_state():
    """Returns the current state of the game."""
    game = get_game()
    return {
        "board": game.board.board,
        "current_player": game.current_player,
        "status": game.status,
        "mode": game.game_mode,
        "player_mark": game.player_mark
    }

@app.post("/reset")
async def reset_game(request: ResetRequest):
    """Resets the game session with new parameters."""
    game = get_game()
    game.reset(mode=request.mode, player_mark=request.player_mark)
    return await get_state()

@app.post("/move")
async def make_move(request: MoveRequest):
    """Processes a player's move and triggers the AI if necessary."""
    game = get_game()
    
    if game.status != "ongoing":
        raise HTTPException(status_code=400, detail="Game already finished")

    # 1. Player Move
    game.process_move(request.square_1, request.square_2, game.current_player)

    # 2. Sequential AI Move (PvE Mode)
    if game.game_mode == "PvE" and game.status == "ongoing" and game.current_player == game.bot_mark:
        game.execute_bot_move()

    return await get_state()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    # Only reload if DEBUG is explicitly set to "True"
    is_debug = os.environ.get("DEBUG", "False").lower() == "true"
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=is_debug)
