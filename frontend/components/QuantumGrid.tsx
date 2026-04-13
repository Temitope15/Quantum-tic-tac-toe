"use client";

import React from "react";
import { QuantumCell } from "./QuantumCell";

interface QuantumGridProps {
  board: (string | string[])[];
  selectedSquares: number[];
  tutorialHighlights: number[];
  onSquareClick: (index: number) => void;
  disabled: boolean;
}

export const QuantumGrid: React.FC<QuantumGridProps> = ({
  board,
  selectedSquares,
  tutorialHighlights,
  onSquareClick,
  disabled
}) => {
  return (
    <div className="grid grid-cols-3 gap-4 w-full max-w-[500px] aspect-square p-6 bg-white/5 
                    rounded-[2rem] border border-white/10 shadow-2xl backdrop-blur-sm self-center">
      {board.map((content, index) => (
        <QuantumCell
          key={index}
          index={index}
          content={content}
          isSelected={selectedSquares.includes(index)}
          isTutorialHighlight={tutorialHighlights.includes(index)}
          onClick={() => onSquareClick(index)}
          disabled={disabled}
        />
      ))}
    </div>
  );
};
