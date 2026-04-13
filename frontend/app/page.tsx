"use client";

import React, { useState, useEffect, useCallback } from "react";
import { QuantumGrid } from "../components/QuantumGrid";
import { TutorialOverlay } from "../components/TutorialOverlay";
import { Toast } from "../components/Toast";

const API_URL = "http://127.0.0.1:8000";

interface GameState {
  board: (string | string[])[];
  current_player: string;
  status: string;
  mode: string;
  player_mark: string;
}

const TUTORIAL_STEPS = [
  {
    title: "Quantum Superposition",
    desc: "In this reality, you don't just pick one square. You pick TWO. Your mark exists in both places at once—this is Superposition. Try clicking squares 0 and 1.",
    highlightSquares: [0, 1],
  },
  {
    title: "Quantum Entanglement",
    desc: "Moves are linked. If one part of your move collapses, the other part must instantly react. This is 'Spooky Action at a Distance'. Click 1 and 2 to entangle them.",
    highlightSquares: [1, 2],
  },
  {
    title: "The Wavefunction Collapse",
    desc: "Reality only takes shape when the universe is forced to choose. Creating a closed loop of moves triggers a 'Collapse'. Click 2 and 0 to close the circuit!",
    highlightSquares: [2, 0],
  },
];

export default function QuantumTicTacToe() {
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [selectedSquares, setSelectedSquares] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" | "info" } | null>(null);
  
  // Simulation/Tutorial State
  const [isTutorial, setIsTutorial] = useState(false);
  const [tutorialStep, setTutorialStep] = useState(0);

  const fetchState = useCallback(async () => {
    try {
      const response = await fetch(`${API_URL}/state`);
      if (!response.ok) throw new Error("Faulty connection to the quantum engine.");
      const data = await response.json();
      setGameState(data);
    } catch (error) {
      console.error("Fetch failed:", error);
      showToast("Server unreachable. Please check if the backend is running.", "error");
    }
  }, []);

  useEffect(() => {
    fetchState();
  }, [fetchState]);

  const showToast = (message: string, type: "success" | "error" | "info" = "info") => {
    setToast({ message, type });
  };

  const handleSquareClick = (index: number) => {
    if (loading || (gameState && typeof gameState.board[index] === "string")) return;

    if (selectedSquares.includes(index)) {
      setSelectedSquares(prev => prev.filter(s => s !== index));
      return;
    }

    if (selectedSquares.length < 2) {
      const newSelected = [...selectedSquares, index];
      setSelectedSquares(newSelected);
      if (newSelected.length === 2) {
        submitMove(newSelected[0], newSelected[1]);
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
      if (!response.ok) throw new Error(data.detail || "Invalid Move");
      
      setGameState(data);
      if (isTutorial) setTutorialStep(prev => prev + 1);
    } catch (error: any) {
      showToast(error.message || "Quantum anomaly detected.", "error");
    } finally {
      setSelectedSquares([]);
      setLoading(false);
    }
  };

  const resetGame = async (mode: string = "PvE", mark: string = "X") => {
    setLoading(true);
    try {
      await fetch(`${API_URL}/reset`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode, player_mark: mark }),
      });
      await fetchState();
      showToast(`Game reset: ${mode} mode`, "success");
    } catch (error) {
      showToast("Reset failed.", "error");
    } finally {
      setLoading(false);
    }
  };

  const startTutorial = () => {
    setIsTutorial(true);
    setTutorialStep(0);
    resetGame("PvP", "X");
  };

  if (!gameState) {
    return (
      <div className="min-h-screen bg-[#0a0a1a] flex flex-col items-center justify-center p-4">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-[#00f2fe]" />
        <p className="mt-4 text-[#00f2fe] font-mono animate-pulse">Initializing Quantum Engine...</p>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-[#0a0a1a] text-white selection:bg-[#00f2fe]/30 font-sans overflow-hidden">
      {/* Dynamic Background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-600/10 blur-[120px] rounded-full" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-600/10 blur-[120px] rounded-full" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-12 flex flex-col items-center gap-12">
        
        {/* Header Section */}
        <header className="text-center space-y-4">
          <h1 className="text-5xl md:text-7xl font-black bg-clip-text text-transparent bg-gradient-to-r from-[#00f2fe] to-[#4facfe] tracking-tighter uppercase italic">
            Quantum Tic-Tac-Toe
          </h1>
          <div className="flex justify-center gap-3">
            <span className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] uppercase font-bold tracking-widest text-[#00f2fe]">
              Mode: {gameState.mode === "PvE" ? "vs Computer" : "PvP"}
            </span>
            <span className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] uppercase font-bold tracking-widest text-[#4facfe]">
              Locked As: {gameState.player_mark}
            </span>
          </div>
        </header>

        {/* The Grid Component */}
        <QuantumGrid
          board={gameState.board}
          selectedSquares={selectedSquares}
          tutorialHighlights={isTutorial ? TUTORIAL_STEPS[tutorialStep]?.highlightSquares || [] : []}
          onSquareClick={handleSquareClick}
          disabled={loading || gameState.status !== "ongoing"}
        />

        {/* Footer / Controls */}
        <footer className="flex flex-col items-center gap-8 w-full">
          <div className={`px-12 py-4 rounded-2xl border transition-all duration-500 ${
            gameState.status === "ongoing" 
              ? "bg-white/5 border-white/10 text-white/60" 
              : "bg-[#00f2fe]/20 border-[#00f2fe]/50 text-[#00f2fe] scale-110 shadow-[0_0_30px_rgba(0,242,254,0.2)]"
          }`}>
            <span className="text-xl font-black uppercase tracking-widest italic">
              {gameState.status === "ongoing" 
                ? `${gameState.current_player === 'X' ? 'Player X' : 'Player O'}'s Turn` 
                : gameState.status}
            </span>
          </div>

          <div className="flex gap-4">
            <button
              onClick={() => resetGame(gameState.mode, gameState.player_mark)}
              className="px-6 py-3 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all font-bold uppercase tracking-widest text-xs"
            >
              Reset Match
            </button>
            <button
              onClick={startTutorial}
              className="px-6 py-3 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all font-bold uppercase tracking-widest text-xs"
            >
              Simulation Mode
            </button>
            <button
              onClick={() => resetGame(gameState.mode === "PvE" ? "PvP" : "PvE", gameState.player_mark)}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500/20 to-blue-500/20 border border-white/10 hover:border-purple-500/50 transition-all font-bold uppercase tracking-widest text-xs"
            >
              Change Mode
            </button>
          </div>
        </footer>
      </div>

      {/* Overlays */}
      {isTutorial && tutorialStep < TUTORIAL_STEPS.length && (
        <TutorialOverlay
          currentStep={tutorialStep}
          totalSteps={TUTORIAL_STEPS.length}
          stepData={TUTORIAL_STEPS[tutorialStep]}
          onNext={() => {
            if (tutorialStep === TUTORIAL_STEPS.length - 1) setIsTutorial(false);
            else setTutorialStep(prev => prev + 1);
          }}
          onPrev={() => setTutorialStep(prev => Math.max(0, prev - 1))}
          onEnd={() => setIsTutorial(false)}
        />
      )}

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </main>
  );
}
