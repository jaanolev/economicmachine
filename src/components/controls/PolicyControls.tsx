/**
 * Policy Controls
 *
 * Controls for central bank and government policy interventions.
 * Dalio: Interest rates are the key lever for the central bank.
 */

import React from 'react';

interface PolicyControlsProps {
  interestRate: number;
  atZeroLowerBound: boolean;
  isDeleveraging: boolean;
  deleveragingLevers: {
    austerity: number;
    debtRestructuring: number;
    wealthTransfer: number;
    moneyPrinting: number;
  };
  onInterestRateChange: (rate: number) => void;
  onTriggerQE: (amount: number) => void;
  onDeleveragingLeverChange: (levers: {
    austerity?: number;
    debtRestructuring?: number;
    wealthTransfer?: number;
    moneyPrinting?: number;
  }) => void;
}

export const PolicyControls: React.FC<PolicyControlsProps> = ({
  interestRate,
  atZeroLowerBound,
  isDeleveraging,
  deleveragingLevers,
  onInterestRateChange,
  onTriggerQE,
  onDeleveragingLeverChange
}) => {
  return (
    <div className="p-4 space-y-6">
      {/* Interest Rate Control */}
      <div>
        <div className="flex justify-between items-center mb-2">
          <label className="text-slate-200 font-medium">
            Central Bank Rate (MP1)
          </label>
          <span className="text-lg font-mono text-blue-400">
            {(interestRate * 100).toFixed(2)}%
          </span>
        </div>
        <input
          type="range"
          min="0"
          max="0.15"
          step="0.0025"
          value={interestRate}
          onChange={(e) => onInterestRateChange(parseFloat(e.target.value))}
          className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
        />
        <div className="flex justify-between text-xs text-slate-500 mt-1">
          <span>0%</span>
          <span>7.5%</span>
          <span>15%</span>
        </div>
        {atZeroLowerBound && (
          <p className="text-yellow-400 text-sm mt-2">
            At zero lower bound - MP1 ineffective
          </p>
        )}
      </div>

      {/* QE Control */}
      <div>
        <label className="text-slate-200 font-medium block mb-2">
          Quantitative Easing (MP2)
        </label>
        <div className="flex gap-2">
          {[100, 500, 1000].map((amount) => (
            <button
              key={amount}
              onClick={() => onTriggerQE(amount)}
              className="px-3 py-2 bg-purple-600 hover:bg-purple-700 rounded text-white text-sm"
            >
              QE ${amount}
            </button>
          ))}
        </div>
        <p className="text-xs text-slate-500 mt-1">
          Print money to buy assets (use when rates near zero)
        </p>
      </div>

      {/* Deleveraging Levers */}
      {isDeleveraging && (
        <div className="border-t border-slate-700 pt-4">
          <h3 className="text-slate-200 font-medium mb-3">
            Deleveraging Levers
          </h3>
          <p className="text-xs text-slate-400 mb-4">
            Balance deflationary (austerity, defaults) with inflationary (printing) forces
          </p>

          {/* Austerity */}
          <LeverSlider
            label="Austerity"
            value={deleveragingLevers.austerity}
            onChange={(v) => onDeleveragingLeverChange({ austerity: v })}
            color="red"
            description="Cut spending (deflationary)"
          />

          {/* Debt Restructuring */}
          <LeverSlider
            label="Debt Restructuring"
            value={deleveragingLevers.debtRestructuring}
            onChange={(v) => onDeleveragingLeverChange({ debtRestructuring: v })}
            color="orange"
            description="Write down debts (deflationary)"
          />

          {/* Wealth Transfer */}
          <LeverSlider
            label="Wealth Transfer"
            value={deleveragingLevers.wealthTransfer}
            onChange={(v) => onDeleveragingLeverChange({ wealthTransfer: v })}
            color="yellow"
            description="Tax wealthy, redistribute"
          />

          {/* Money Printing */}
          <LeverSlider
            label="Money Printing"
            value={deleveragingLevers.moneyPrinting}
            onChange={(v) => onDeleveragingLeverChange({ moneyPrinting: v })}
            color="green"
            description="Monetize debt (inflationary)"
          />

          {/* Balance Indicator */}
          <div className="mt-4 p-3 bg-slate-800 rounded-lg">
            <div className="text-sm text-slate-400 mb-2">Force Balance:</div>
            <div className="flex items-center gap-2">
              <span className="text-red-400 text-sm">Deflationary</span>
              <div className="flex-1 h-4 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-red-500 to-green-500"
                  style={{
                    width: '100%',
                    clipPath: `inset(0 ${100 - ((deleveragingLevers.moneyPrinting - (deleveragingLevers.austerity + deleveragingLevers.debtRestructuring) / 2) + 0.5) * 100}% 0 0)`
                  }}
                />
              </div>
              <span className="text-green-400 text-sm">Inflationary</span>
            </div>
          </div>
        </div>
      )}

      {/* Dalio Quote */}
      <div className="p-3 bg-slate-800/50 rounded-lg border border-slate-700">
        <p className="text-sm text-slate-400 italic">
          "The way to manage a debt crisis well is to balance the deflationary forces with the inflationary ones."
        </p>
        <p className="text-xs text-slate-500 mt-1">— Ray Dalio</p>
      </div>
    </div>
  );
};

interface LeverSliderProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  color: 'red' | 'orange' | 'yellow' | 'green';
  description: string;
}

const LeverSlider: React.FC<LeverSliderProps> = ({
  label,
  value,
  onChange,
  color,
  description
}) => {
  const colorClasses = {
    red: 'text-red-400',
    orange: 'text-orange-400',
    yellow: 'text-yellow-400',
    green: 'text-green-400'
  };

  return (
    <div className="mb-4">
      <div className="flex justify-between items-center mb-1">
        <label className={`text-sm font-medium ${colorClasses[color]}`}>
          {label}
        </label>
        <span className="text-sm font-mono text-slate-300">
          {(value * 100).toFixed(0)}%
        </span>
      </div>
      <input
        type="range"
        min="0"
        max="1"
        step="0.05"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer"
      />
      <p className="text-xs text-slate-500">{description}</p>
    </div>
  );
};
