/**
 * Debt Gauge
 *
 * Visual gauge showing current debt burden.
 * Dalio: Debt burden is critical - when it gets too high, deleveraging triggers.
 *
 * Key thresholds:
 * - Green: < 50% debt/GDP (healthy)
 * - Yellow: 50-70% (elevated)
 * - Orange: 70-85% (dangerous)
 * - Red: > 85% (crisis/deleveraging likely)
 */

import React from 'react';

interface DebtGaugeProps {
  debtToGDP: number;
  debtServiceToIncome: number;
  isDeleveraging: boolean;
}

export const DebtGauge: React.FC<DebtGaugeProps> = ({
  debtToGDP,
  debtServiceToIncome,
  isDeleveraging
}) => {
  const percentage = Math.min(100, debtToGDP * 100);

  // Determine color based on debt level
  const getColor = (value: number): string => {
    if (value < 50) return '#22C55E';  // Green
    if (value < 70) return '#EAB308';  // Yellow
    if (value < 85) return '#F97316';  // Orange
    return '#EF4444';  // Red
  };

  const color = getColor(percentage);

  // SVG arc calculation
  const radius = 80;
  const circumference = Math.PI * radius;  // Half circle
  const progress = (percentage / 100) * circumference;

  return (
    <div className="flex flex-col items-center p-4">
      <h3 className="text-lg font-semibold text-slate-200 mb-2">Debt Burden</h3>

      {/* Gauge */}
      <div className="relative w-48 h-28">
        <svg viewBox="0 0 200 110" className="w-full h-full">
          {/* Background arc */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke="#374151"
            strokeWidth="16"
            strokeLinecap="round"
          />

          {/* Progress arc */}
          <path
            d="M 20 100 A 80 80 0 0 1 180 100"
            fill="none"
            stroke={color}
            strokeWidth="16"
            strokeLinecap="round"
            strokeDasharray={`${progress} ${circumference}`}
            className="transition-all duration-500"
          />

          {/* Threshold markers */}
          {[50, 70, 85].map((threshold) => {
            const angle = (threshold / 100) * 180 - 90;
            const rad = (angle * Math.PI) / 180;
            const x = 100 + radius * Math.cos(rad);
            const y = 100 + radius * Math.sin(rad);
            return (
              <circle
                key={threshold}
                cx={x}
                cy={y}
                r="3"
                fill="#6B7280"
              />
            );
          })}

          {/* Center text */}
          <text
            x="100"
            y="85"
            textAnchor="middle"
            className="text-3xl font-bold"
            fill={color}
          >
            {percentage.toFixed(0)}%
          </text>
          <text
            x="100"
            y="105"
            textAnchor="middle"
            className="text-sm"
            fill="#9CA3AF"
          >
            Debt/GDP
          </text>
        </svg>
      </div>

      {/* Debt Service Indicator */}
      <div className="mt-4 w-full">
        <div className="flex justify-between text-sm text-slate-400 mb-1">
          <span>Debt Service / Income</span>
          <span>{(debtServiceToIncome * 100).toFixed(1)}%</span>
        </div>
        <div className="w-full bg-slate-700 rounded-full h-2">
          <div
            className="h-2 rounded-full transition-all duration-500"
            style={{
              width: `${Math.min(100, debtServiceToIncome * 100 * 2)}%`,
              backgroundColor: debtServiceToIncome > 0.35 ? '#EF4444' : '#3B82F6'
            }}
          />
        </div>
        {debtServiceToIncome > 0.35 && (
          <p className="text-xs text-red-400 mt-1">
            Warning: Debt service exceeds 35% of income
          </p>
        )}
      </div>

      {/* Deleveraging Alert */}
      {isDeleveraging && (
        <div className="mt-4 px-4 py-2 bg-red-900/50 border border-red-500 rounded-lg">
          <p className="text-red-400 font-semibold text-center">
            DELEVERAGING IN PROGRESS
          </p>
        </div>
      )}

      {/* Legend */}
      <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
        <div className="flex items-center">
          <div className="w-3 h-3 rounded bg-green-500 mr-2" />
          <span className="text-slate-400">&lt; 50% Healthy</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 rounded bg-yellow-500 mr-2" />
          <span className="text-slate-400">50-70% Elevated</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 rounded bg-orange-500 mr-2" />
          <span className="text-slate-400">70-85% Dangerous</span>
        </div>
        <div className="flex items-center">
          <div className="w-3 h-3 rounded bg-red-500 mr-2" />
          <span className="text-slate-400">&gt; 85% Crisis</span>
        </div>
      </div>
    </div>
  );
};
