/**
 * Metrics Bar
 *
 * Shows key economic metrics at a glance.
 */

import React from 'react';
import { EconomicState } from '../../core/models/EconomicState';

interface MetricsBarProps {
  state: EconomicState;
}

export const MetricsBar: React.FC<MetricsBarProps> = ({ state }) => {
  const metrics = [
    {
      label: 'GDP',
      value: `$${(state.nominalGDP / 1000).toFixed(1)}k`,
      subValue: `Real: $${(state.realGDP / 1000).toFixed(1)}k`,
      color: 'text-blue-400'
    },
    {
      label: 'Inflation',
      value: `${(state.inflation * 100).toFixed(1)}%`,
      subValue: state.inflation > 0.03 ? 'High' : state.inflation < 0.01 ? 'Low' : 'Normal',
      color: state.inflation > 0.04 ? 'text-red-400' : state.inflation < 0 ? 'text-blue-400' : 'text-green-400'
    },
    {
      label: 'Unemployment',
      value: `${(state.unemployment * 100).toFixed(1)}%`,
      subValue: state.unemployment > 0.07 ? 'High' : state.unemployment < 0.04 ? 'Low' : 'Normal',
      color: state.unemployment > 0.07 ? 'text-red-400' : 'text-green-400'
    },
    {
      label: 'Debt/GDP',
      value: `${(state.debtToGDPRatio * 100).toFixed(0)}%`,
      subValue: state.debtToGDPRatio > 0.8 ? 'Critical' : state.debtToGDPRatio > 0.6 ? 'Elevated' : 'Normal',
      color: state.debtToGDPRatio > 0.8 ? 'text-red-400' : state.debtToGDPRatio > 0.6 ? 'text-yellow-400' : 'text-green-400'
    },
    {
      label: 'Interest Rate',
      value: `${(state.centralBankRate * 100).toFixed(2)}%`,
      subValue: state.atZeroLowerBound ? 'Zero Bound!' : 'Normal',
      color: state.atZeroLowerBound ? 'text-yellow-400' : 'text-blue-400'
    },
    {
      label: 'Credit Growth',
      value: `${(state.creditGrowth * 100).toFixed(1)}%`,
      subValue: state.creditGrowth > 0.05 ? 'Expanding' : state.creditGrowth < 0 ? 'Contracting' : 'Stable',
      color: state.creditGrowth > 0.05 ? 'text-green-400' : state.creditGrowth < 0 ? 'text-red-400' : 'text-slate-400'
    },
    {
      label: 'Phase',
      value: state.shortTermCycle.phase.charAt(0).toUpperCase() + state.shortTermCycle.phase.slice(1),
      subValue: `Cycle #${state.shortTermCycle.cycleNumber}`,
      color: state.shortTermCycle.phase === 'expansion' ? 'text-green-400' :
             state.shortTermCycle.phase === 'contraction' ? 'text-red-400' :
             state.shortTermCycle.phase === 'peak' ? 'text-yellow-400' : 'text-blue-400'
    }
  ];

  return (
    <div className="grid grid-cols-7 gap-4 p-4 bg-slate-800 rounded-lg">
      {metrics.map((metric) => (
        <div key={metric.label} className="text-center">
          <div className="text-xs text-slate-500 uppercase tracking-wider">
            {metric.label}
          </div>
          <div className={`text-lg font-bold ${metric.color}`}>
            {metric.value}
          </div>
          <div className="text-xs text-slate-500">
            {metric.subValue}
          </div>
        </div>
      ))}
    </div>
  );
};
