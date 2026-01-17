/**
 * Cycle Phase Indicator
 *
 * Shows current position in both short-term and long-term cycles.
 * Dalio's framework: understanding where you are in the cycle is crucial.
 */

import React from 'react';
import { ShortTermCyclePhase, LongTermCyclePhase } from '../../core/types';

interface CycleIndicatorProps {
  shortTermPhase: ShortTermCyclePhase;
  shortTermPosition: number;  // 0-1
  shortTermCycleNumber: number;
  longTermPhase: LongTermCyclePhase;
  longTermYears: number;
}

const shortTermPhases: ShortTermCyclePhase[] = ['expansion', 'peak', 'contraction', 'trough'];
const longTermPhases: LongTermCyclePhase[] = ['leveraging', 'peak', 'deleveraging', 'reflation'];

const phaseColors: Record<string, string> = {
  expansion: 'bg-green-500',
  peak: 'bg-yellow-500',
  contraction: 'bg-red-500',
  trough: 'bg-blue-500',
  leveraging: 'bg-green-600',
  deleveraging: 'bg-red-600',
  reflation: 'bg-blue-600'
};

const phaseDescriptions: Record<string, string> = {
  expansion: 'Credit growing, economy expanding',
  peak: 'Inflation rising, rates increasing',
  contraction: 'Credit tightening, recession',
  trough: 'Rates falling, recovery starting',
  leveraging: 'Debt accumulating over decades',
  'long-peak': 'Debt burden at maximum',
  deleveraging: 'Debt being reduced (10+ years)',
  reflation: 'New cycle beginning'
};

export const CycleIndicator: React.FC<CycleIndicatorProps> = ({
  shortTermPhase,
  shortTermPosition,
  shortTermCycleNumber,
  longTermPhase,
  longTermYears
}) => {
  return (
    <div className="p-4 space-y-6">
      {/* Short-Term Cycle */}
      <div>
        <h3 className="text-lg font-semibold text-slate-200 mb-3">
          Short-Term Debt Cycle
          <span className="text-sm font-normal text-slate-400 ml-2">
            (5-8 years)
          </span>
        </h3>

        {/* Phase indicator bar */}
        <div className="relative mb-2">
          <div className="flex h-8 rounded-lg overflow-hidden">
            {shortTermPhases.map((phase, index) => {
              const isActive = phase === shortTermPhase;
              const widths = [45, 10, 35, 10];  // Expansion is longest
              return (
                <div
                  key={phase}
                  className={`flex items-center justify-center text-xs font-medium transition-all
                    ${phaseColors[phase]} ${isActive ? 'ring-2 ring-white ring-offset-2 ring-offset-slate-900' : 'opacity-50'}`}
                  style={{ width: `${widths[index]}%` }}
                >
                  {phase.charAt(0).toUpperCase() + phase.slice(1)}
                </div>
              );
            })}
          </div>

          {/* Position marker */}
          <div
            className="absolute top-0 w-1 h-8 bg-white shadow-lg transition-all duration-300"
            style={{ left: `${shortTermPosition * 100}%` }}
          />
        </div>

        {/* Current phase info */}
        <div className="flex justify-between text-sm">
          <span className="text-slate-400">
            Cycle #{shortTermCycleNumber}
          </span>
          <span className={`font-medium ${
            shortTermPhase === 'expansion' ? 'text-green-400' :
            shortTermPhase === 'peak' ? 'text-yellow-400' :
            shortTermPhase === 'contraction' ? 'text-red-400' :
            'text-blue-400'
          }`}>
            {phaseDescriptions[shortTermPhase]}
          </span>
        </div>
      </div>

      {/* Long-Term Cycle */}
      <div>
        <h3 className="text-lg font-semibold text-slate-200 mb-3">
          Long-Term Debt Cycle
          <span className="text-sm font-normal text-slate-400 ml-2">
            (75-100 years)
          </span>
        </h3>

        {/* Phase indicator */}
        <div className="flex h-8 rounded-lg overflow-hidden mb-2">
          {longTermPhases.map((phase) => {
            const isActive = phase === longTermPhase;
            const widths: Record<LongTermCyclePhase, number> = {
              leveraging: 70,
              peak: 5,
              deleveraging: 15,
              reflation: 10
            };
            return (
              <div
                key={phase}
                className={`flex items-center justify-center text-xs font-medium transition-all
                  ${phaseColors[phase]} ${isActive ? 'ring-2 ring-white ring-offset-2 ring-offset-slate-900' : 'opacity-50'}`}
                style={{ width: `${widths[phase]}%` }}
              >
                {phase.charAt(0).toUpperCase() + phase.slice(1)}
              </div>
            );
          })}
        </div>

        {/* Current phase info */}
        <div className="flex justify-between text-sm">
          <span className="text-slate-400">
            Year {Math.floor(longTermYears)} of cycle
          </span>
          <span className={`font-medium ${
            longTermPhase === 'leveraging' ? 'text-green-400' :
            longTermPhase === 'peak' ? 'text-yellow-400' :
            longTermPhase === 'deleveraging' ? 'text-red-400' :
            'text-blue-400'
          }`}>
            {phaseDescriptions[longTermPhase] || phaseDescriptions[`long-${longTermPhase}`]}
          </span>
        </div>
      </div>

      {/* Dalio Quote */}
      <div className="mt-4 p-3 bg-slate-800/50 rounded-lg border border-slate-700">
        <p className="text-sm text-slate-400 italic">
          "Understanding where you are in the cycle is crucial for knowing what's likely to happen next."
        </p>
        <p className="text-xs text-slate-500 mt-1">— Ray Dalio</p>
      </div>
    </div>
  );
};
