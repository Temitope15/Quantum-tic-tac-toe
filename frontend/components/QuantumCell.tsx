"use client";

import React from "react";

interface QuantumCellProps {
  index: number;
  content: string | string[];
  isSelected: boolean;
  isTutorialHighlight: boolean;
  onClick: () => void;
  disabled: boolean;
}

export const QuantumCell: React.FC<QuantumCellProps> = ({
  index,
  content,
  isSelected,
  isTutorialHighlight,
  onClick,
  disabled
}) => {
  const isSolid = typeof content === "string";
  const isX = isSolid ? content === "X" : false;
  const isO = isSolid ? content === "O" : false;

  return (
    <div
      onClick={!disabled ? onClick : undefined}
      className={`
        relative aspect-square rounded-xl flex items-center justify-center transition-all duration-300
        ${isSolid 
          ? "bg-white/5 shadow-inner cursor-default" 
          : "bg-white/10 hover:bg-white/20 cursor-pointer active:scale-95 shadow-lg border border-white/5"}
        ${isSelected ? "ring-2 ring-[#00f2fe] scale-[1.02] bg-white/20" : ""}
        ${isTutorialHighlight ? "ring-4 ring-blue-500 animate-pulse border-blue-400" : ""}
      `}
    >
      {/* Background Index Number (Subtle) */}
      <span className="absolute top-2 left-2 text-[10px] text-white/10 font-mono select-none">
        0{index}
      </span>

      {isSolid ? (
        <span className={`text-6xl font-black transition-all duration-500 scale-100 opacity-100 ${
          isX ? "text-[#00f2fe] drop-shadow-[0_0_15px_rgba(0,242,254,0.5)]" 
              : "text-[#4facfe] drop-shadow-[0_0_15px_rgba(79,172,254,0.5)]"
        }`}>
          {content}
        </span>
      ) : (
        <div className="flex flex-wrap gap-1 p-2 justify-center items-center">
          {(content as string[]).map((mark, i) => {
            const isMarkX = mark.startsWith("X");
            return (
              <span
                key={i}
                className={`text-xs font-bold px-1.5 py-0.5 rounded backdrop-blur-sm border 
                           transition-all hover:scale-110 ${
                  isMarkX 
                    ? "text-[#00f2fe] border-[#00f2fe]/30 bg-[#00f2fe]/10" 
                    : "text-[#4facfe] border-[#4facfe]/30 bg-[#4facfe]/10"
                }`}
              >
                {mark}
              </span>
            );
          })}
        </div>
      )}

      {/* Interactive Hover Feedback */}
      {!isSolid && !disabled && (
        <div className="absolute inset-0 rounded-xl opacity-0 hover:opacity-100 transition-opacity
                        bg-gradient-to-br from-white/5 to-transparent pointer-events-none" />
      )}
    </div>
  );
};
