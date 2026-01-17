/**
 * Playback Controls
 *
 * Controls for simulation playback: play, pause, speed, reset.
 */

import React from 'react';
import { SimulationSpeed } from '../../engine/SimulationEngine';

interface PlaybackControlsProps {
  isRunning: boolean;
  speed: SimulationSpeed;
  currentYear: number;
  currentMonth: number;
  onPlay: () => void;
  onPause: () => void;
  onReset: () => void;
  onSpeedChange: (speed: SimulationSpeed) => void;
  onTick: () => void;
  onRunYears: (years: number) => void;
}

export const PlaybackControls: React.FC<PlaybackControlsProps> = ({
  isRunning,
  speed,
  currentYear,
  currentMonth,
  onPlay,
  onPause,
  onReset,
  onSpeedChange,
  onTick,
  onRunYears
}) => {
  const speeds: SimulationSpeed[] = ['slow', 'normal', 'fast', 'max'];

  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  return (
    <div className="flex items-center gap-4 p-4 bg-slate-800 rounded-lg">
      {/* Date Display */}
      <div className="text-xl font-mono text-white min-w-32">
        {monthNames[currentMonth - 1]} {currentYear}
      </div>

      {/* Play/Pause Button */}
      <button
        onClick={isRunning ? onPause : onPlay}
        className={`px-4 py-2 rounded-lg font-medium transition-colors ${
          isRunning
            ? 'bg-yellow-600 hover:bg-yellow-700 text-white'
            : 'bg-green-600 hover:bg-green-700 text-white'
        }`}
      >
        {isRunning ? (
          <span className="flex items-center gap-2">
            <PauseIcon /> Pause
          </span>
        ) : (
          <span className="flex items-center gap-2">
            <PlayIcon /> Play
          </span>
        )}
      </button>

      {/* Step Forward */}
      <button
        onClick={onTick}
        disabled={isRunning}
        className="px-3 py-2 bg-slate-700 hover:bg-slate-600 disabled:opacity-50 rounded-lg text-white"
        title="Advance 1 month"
      >
        <StepIcon />
      </button>

      {/* Speed Control */}
      <div className="flex items-center gap-2">
        <span className="text-slate-400 text-sm">Speed:</span>
        <div className="flex gap-1">
          {speeds.map((s) => (
            <button
              key={s}
              onClick={() => onSpeedChange(s)}
              className={`px-2 py-1 text-sm rounded transition-colors ${
                speed === s
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              {s === 'max' ? 'Max' : s.charAt(0).toUpperCase() + s.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Quick Jump */}
      <div className="flex items-center gap-2">
        <span className="text-slate-400 text-sm">Jump:</span>
        {[1, 5, 10, 25].map((years) => (
          <button
            key={years}
            onClick={() => onRunYears(years)}
            disabled={isRunning}
            className="px-2 py-1 text-sm bg-slate-700 hover:bg-slate-600 disabled:opacity-50 rounded text-white"
          >
            +{years}y
          </button>
        ))}
      </div>

      {/* Reset */}
      <button
        onClick={onReset}
        className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg text-white font-medium ml-auto"
      >
        Reset
      </button>
    </div>
  );
};

// Simple SVG Icons
const PlayIcon = () => (
  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
    <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
  </svg>
);

const PauseIcon = () => (
  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
    <path d="M5.75 3a.75.75 0 00-.75.75v12.5c0 .414.336.75.75.75h1.5a.75.75 0 00.75-.75V3.75A.75.75 0 007.25 3h-1.5zM12.75 3a.75.75 0 00-.75.75v12.5c0 .414.336.75.75.75h1.5a.75.75 0 00.75-.75V3.75a.75.75 0 00-.75-.75h-1.5z" />
  </svg>
);

const StepIcon = () => (
  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
    <path d="M3 4.25a.75.75 0 011.28-.53l5.47 5.47 5.47-5.47a.75.75 0 011.06 1.06l-6 6a.75.75 0 01-1.06 0l-6-6A.75.75 0 013 4.25zM3 14.25a.75.75 0 011.28-.53l5.47 5.47 5.47-5.47a.75.75 0 011.06 1.06l-6 6a.75.75 0 01-1.06 0l-6-6a.75.75 0 01-.28-.53z" />
  </svg>
);
