"use client";

import React from "react";

interface TutorialStep {
  title: string;
  desc: string;
  highlightSquares: number[];
}

interface TutorialOverlayProps {
  currentStep: number;
  totalSteps: number;
  stepData: TutorialStep;
  onNext: () => void;
  onPrev: () => void;
  onEnd: () => void;
}

export const TutorialOverlay: React.FC<TutorialOverlayProps> = ({
  currentStep,
  totalSteps,
  stepData,
  onNext,
  onPrev,
  onEnd
}) => {
  return (
    <div className="fixed bottom-10 left-1/2 -translate-x-1/2 z-50 w-full max-w-lg px-4 animate-bounce-subtle">
      <div className="bg-[#1a1a2e]/90 backdrop-blur-xl border border-white/20 p-8 rounded-3xl shadow-[0_0_50px_rgba(0,0,0,0.5)]">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-[#00f2fe] font-black text-2xl tracking-tight uppercase italic">
            {stepData.title}
          </h3>
          <span className="text-white/40 font-mono text-sm px-3 py-1 bg-white/5 rounded-full">
            {currentStep + 1} / {totalSteps}
          </span>
        </div>
        
        <p className="text-gray-200 leading-relaxed mb-8 text-lg">
          {stepData.desc}
        </p>
        
        <div className="flex justify-between items-center gap-4">
          <button
            onClick={onEnd}
            className="text-white/40 hover:text-white transition-colors text-sm font-medium"
          >
            Exit Tutorial
          </button>
          
          <div className="flex gap-2">
            <button
              onClick={onPrev}
              disabled={currentStep === 0}
              className="px-4 py-2 rounded-xl bg-white/5 hover:bg-white/10 disabled:opacity-30 
                         transition-all border border-white/10 active:scale-95"
            >
              Back
            </button>
            <button
              onClick={onNext}
              className="px-8 py-2 rounded-xl bg-gradient-to-r from-[#00f2fe] to-[#4facfe] 
                         text-black font-bold hover:shadow-[0_0_20px_rgba(0,242,254,0.4)] 
                         transition-all active:scale-95"
            >
              {currentStep === totalSteps - 1 ? "Finish" : "Next"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
