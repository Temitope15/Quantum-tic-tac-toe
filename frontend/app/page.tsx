"use client";

import React, { useState, useEffect } from "react";

/**
 * Quantum Tic-Tac-Toe Web UI
 * A modern, dark-themed frontend for the Quantum Tic-Tac-Toe engine.
 */

export default function QuantumTicTacToe() {
  const [board, setBoard] = useState<string[]>(Array(9).fill(""));
  const [currentPlayer, setCurrentPlayer] = useState<string>("X");
  const [status, setStatus] = useState<string>("ongoing");
  const [selectedSquares, setSelectedSquares] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  // Fetch initial state on mount
  useEffect(() => {
    fetchState();
  }, []);

  const fetchState = async () => {
    try {
      const response = await fetch(`${API_URL}/state`);
      const data = await response.json();
      setBoard(data.board);
      setCurrentPlayer(data.current_player);
      setStatus(data.status);
    } catch (error) {
      console.error("Failed to fetch state:", error);
    }
  };

  const handleSquareClick = (index: number) => {
    if (status !== "ongoing" || loading) return;
    
    // Check if square is already collapsed (fixed 'X' or 'O')
    // In our backend, collapsed squares are just "X" or "O"
    if (board[index] === "X" || board[index] === "O") return;

    // Toggle selection
    if (selectedSquares.includes(index)) {
      setSelectedSquares(selectedSquares.filter((i) => i !== index));
    } else if (selectedSquares.length < 2) {
      const newSelection = [...selectedSquares, index];
      setSelectedSquares(newSelection);

      // Automatically submit if 2 squares are selected
      if (newSelection.length === 2) {
        submitMove(newSelection[0], newSelection[1]);
      }
    }
  };

  const submitMove = async (s1: number, s2: number) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/move`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ square_1: s1, square_2: s2 }),
      });
      const data = await response.json();
      setBoard(data.board);
      setCurrentPlayer(data.current_player);
      setStatus(data.status);
    } catch (error) {
      console.error("Move failed:", error);
    } finally {
      setSelectedSquares([]);
      setLoading(false);
    }
  };

  const resetGame = async () => {
    try {
      const response = await fetch(`${API_URL}/reset`, { method: "POST" });
      const data = await response.json();
      setBoard(data.board);
      setCurrentPlayer(data.current_player);
      setStatus(data.status);
      setSelectedSquares([]);
    } catch (error) {
      console.error("Reset failed:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4 font-sans">
      <h1 className="text-5xl font-extrabold mb-8 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent drop-shadow-sm">
        Quantum Tic-Tac-Toe
      </h1>

      <div className="bg-gray-800 p-8 rounded-3xl shadow-2xl border border-gray-700 backdrop-blur-sm">
        <div className="grid grid-cols-3 gap-4">
          {board.map((cell, idx) => {
            const isSelected = selectedSquares.includes(idx);
            const isFinished = status !== "ongoing";
            const isCollapsed = cell === "X" || cell === "O";

            return (
              <button
                key={idx}
                id={`square-${idx}`}
                onClick={() => handleSquareClick(idx)}
                disabled={isFinished || isCollapsed}
                className={`
                  h-32 w-32 flex items-center justify-center p-2 rounded-2xl transition-all duration-300 transform
                  ${isCollapsed ? "bg-gray-700 cursor-default" : "bg-gray-750 hover:bg-gray-600 active:scale-95 cursor-pointer"}
                  ${isSelected ? "ring-4 ring-blue-500 bg-blue-900/40" : "border border-gray-700 shadow-inner"}
                  ${isFinished && !isCollapsed ? "opacity-50" : ""}
                `}
              >
                <div className="text-center break-words w-full">
                  {isCollapsed ? (
                    <span className={`text-6xl font-black ${cell === 'X' ? 'text-blue-400' : 'text-purple-400'}`}>
                      {cell}
                    </span>
                  ) : (
                    <span className="text-xs font-mono text-gray-400 tracking-tighter leading-tight">
                      {cell}
                    </span>
                  )}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      <div className="mt-8 flex flex-col items-center gap-4">
        <div className={`text-2xl font-bold px-6 py-2 rounded-full border-2 ${
          status.includes('wins') ? 'bg-green-900/30 border-green-500 text-green-400 animate-bounce' :
          status.includes('Draw') ? 'bg-yellow-900/30 border-yellow-500 text-yellow-400' :
          'bg-blue-900/20 border-blue-500/50 text-blue-300'
        }`}>
          {status === "ongoing" ? (
            <span>Player <span className="text-blue-400 font-extrabold">{currentPlayer}</span>'s Turn</span>
          ) : (
            status.toUpperCase()
          )}
        </div>

        <button
          onClick={resetGame}
          className="px-6 py-2 bg-gray-750 hover:bg-gray-700 border border-gray-600 rounded-xl transition-colors text-sm font-semibold tracking-wide"
        >
          Reset Game
        </button>
      </div>

      <style jsx global>{`
        .bg-gray-750 { background-color: #2d3748; }
      `}</style>
    </div>
  );
}
