/**
 * Three Forces Chart
 *
 * The main visualization showing Dalio's three driving forces:
 * 1. Productivity trend (steady upward line)
 * 2. Short-term debt cycle (5-8 year oscillation)
 * 3. Long-term debt cycle (slow 75-100 year wave)
 * 4. Actual GDP (combination of all three)
 */

import React, { useMemo } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { EconomicState } from '../../core/models/EconomicState';

interface ThreeForcesChartProps {
  history: EconomicState[];
  showProductivity?: boolean;
  showShortCycle?: boolean;
  showLongCycle?: boolean;
  showActualGDP?: boolean;
}

export const ThreeForcesChart: React.FC<ThreeForcesChartProps> = ({
  history,
  showProductivity = true,
  showShortCycle = true,
  showLongCycle = true,
  showActualGDP = true
}) => {
  const data = useMemo(() => {
    return history.map((state, index) => {
      // Calculate short-term cycle effect
      const shortCyclePosition = state.shortTermCycle.positionInCycle;
      const shortCycleAmplitude = 0.05;
      const shortCycleEffect = 1 + shortCycleAmplitude * Math.sin(2 * Math.PI * shortCyclePosition);

      // Calculate long-term cycle effect (debt burden)
      const debtEffect = 1 + (state.debtToGDPRatio - 0.5) * 0.15;

      return {
        time: index,
        year: state.year + (state.month - 1) / 12,
        yearLabel: state.month === 1 ? state.year.toString() : '',

        // Productivity: steady growth line
        productivity: state.potentialGDP,

        // Short-term: oscillation around productivity
        shortTermCycle: state.potentialGDP * shortCycleEffect,

        // Long-term: slow drift based on debt
        longTermCycle: state.potentialGDP * debtEffect,

        // Actual GDP
        actualGDP: state.realGDP,

        // For tooltip
        phase: state.shortTermCycle.phase,
        inflation: (state.inflation * 100).toFixed(1),
        debtToGDP: (state.debtToGDPRatio * 100).toFixed(0),
        isDeleveraging: state.deleveraging.isDeleveraging
      };
    });
  }, [history]);

  // Find recession periods for highlighting
  const recessionPeriods = useMemo(() => {
    const periods: { start: number; end: number }[] = [];
    let currentStart: number | null = null;

    history.forEach((state, index) => {
      if (state.shortTermCycle.phase === 'contraction') {
        if (currentStart === null) currentStart = index;
      } else {
        if (currentStart !== null) {
          periods.push({ start: currentStart, end: index - 1 });
          currentStart = null;
        }
      }
    });

    return periods;
  }, [history]);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-800 p-3 rounded shadow-lg border border-slate-600">
          <p className="text-white font-bold">Year: {data.year.toFixed(1)}</p>
          <p className="text-green-400">Phase: {data.phase}</p>
          <p className="text-blue-400">Inflation: {data.inflation}%</p>
          <p className="text-yellow-400">Debt/GDP: {data.debtToGDP}%</p>
          {data.isDeleveraging && (
            <p className="text-red-400 font-bold">DELEVERAGING</p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />

          <XAxis
            dataKey="year"
            tick={{ fill: '#9CA3AF', fontSize: 12 }}
            tickFormatter={(value) => Math.floor(value).toString()}
            interval="preserveStartEnd"
          />

          <YAxis
            tick={{ fill: '#9CA3AF', fontSize: 12 }}
            tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
            domain={['auto', 'auto']}
          />

          <Tooltip content={<CustomTooltip />} />

          <Legend
            wrapperStyle={{ color: '#9CA3AF' }}
          />

          {/* Productivity Trend - Dalio's baseline */}
          {showProductivity && (
            <Line
              type="monotone"
              dataKey="productivity"
              stroke="#22C55E"
              strokeWidth={2}
              dot={false}
              name="Productivity Trend"
              strokeDasharray="5 5"
            />
          )}

          {/* Short-Term Cycle */}
          {showShortCycle && (
            <Line
              type="monotone"
              dataKey="shortTermCycle"
              stroke="#3B82F6"
              strokeWidth={1.5}
              dot={false}
              name="Short-Term Cycle"
              opacity={0.7}
            />
          )}

          {/* Long-Term Cycle */}
          {showLongCycle && (
            <Line
              type="monotone"
              dataKey="longTermCycle"
              stroke="#F59E0B"
              strokeWidth={1.5}
              dot={false}
              name="Long-Term Debt Effect"
              opacity={0.7}
            />
          )}

          {/* Actual GDP */}
          {showActualGDP && (
            <Line
              type="monotone"
              dataKey="actualGDP"
              stroke="#EF4444"
              strokeWidth={2.5}
              dot={false}
              name="Actual GDP"
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
