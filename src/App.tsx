/**
 * Dalio Economic Machine Simulator
 *
 * An interactive simulation of Ray Dalio's economic framework.
 * Based on "How The Economic Machine Works"
 */

import React, { useEffect } from 'react';
import { useSimulationStore } from './store/simulationStore';
import { ThreeForcesChart, DebtGauge, SpendingChart, CycleIndicator } from './components/visualizations';
import { PlaybackControls, PolicyControls, MetricsBar } from './components/controls';

function App() {
  const {
    engine,
    economicState,
    history,
    isRunning,
    speed,
    initialize,
    start,
    pause,
    reset,
    setSpeed,
    tick,
    runYears,
    setInterestRate,
    triggerQE,
    setDeleveragingLevers
  } = useSimulationStore();

  // Initialize engine on mount
  useEffect(() => {
    if (!engine) {
      initialize();
    }
  }, [engine, initialize]);

  if (!economicState) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading simulation...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* Header */}
      <header className="bg-slate-800 border-b border-slate-700 p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">
              The Economic Machine
            </h1>
            <p className="text-slate-400 text-sm">
              Based on Ray Dalio's Framework
            </p>
          </div>
          <div className="text-right">
            <div className="text-slate-400 text-sm">
              Spending = Money + Credit
            </div>
            <div className="text-slate-500 text-xs">
              One person's spending is another's income
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-4 space-y-4">
        {/* Playback Controls */}
        <PlaybackControls
          isRunning={isRunning}
          speed={speed}
          currentYear={economicState.year}
          currentMonth={economicState.month}
          onPlay={start}
          onPause={pause}
          onReset={reset}
          onSpeedChange={setSpeed}
          onTick={tick}
          onRunYears={runYears}
        />

        {/* Metrics Bar */}
        <MetricsBar state={economicState} />

        {/* Main Content Grid */}
        <div className="grid grid-cols-12 gap-4">
          {/* Left Sidebar - Controls */}
          <div className="col-span-3 space-y-4">
            {/* Cycle Indicator */}
            <div className="bg-slate-800 rounded-lg">
              <CycleIndicator
                shortTermPhase={economicState.shortTermCycle.phase}
                shortTermPosition={economicState.shortTermCycle.positionInCycle}
                shortTermCycleNumber={economicState.shortTermCycle.cycleNumber}
                longTermPhase={economicState.longTermCycle.phase}
                longTermYears={economicState.longTermCycle.yearsIntoCycle}
              />
            </div>

            {/* Debt Gauge */}
            <div className="bg-slate-800 rounded-lg">
              <DebtGauge
                debtToGDP={economicState.debtToGDPRatio}
                debtServiceToIncome={economicState.debtServiceToIncome}
                isDeleveraging={economicState.deleveraging.isDeleveraging}
              />
            </div>
          </div>

          {/* Main Charts Area */}
          <div className="col-span-6 space-y-4">
            {/* Three Forces Chart */}
            <div className="bg-slate-800 rounded-lg p-4">
              <h2 className="text-lg font-semibold mb-2">
                The Three Forces
                <span className="text-sm font-normal text-slate-400 ml-2">
                  Productivity + Short-term Cycle + Long-term Cycle = GDP
                </span>
              </h2>
              <div className="h-64">
                <ThreeForcesChart history={history} />
              </div>
            </div>

            {/* Spending Composition */}
            <div className="bg-slate-800 rounded-lg p-4">
              <h2 className="text-lg font-semibold mb-2">
                Spending Composition
                <span className="text-sm font-normal text-slate-400 ml-2">
                  Total Spending = Money + Credit
                </span>
              </h2>
              <div className="h-48">
                <SpendingChart history={history} />
              </div>
            </div>
          </div>

          {/* Right Sidebar - Policy Controls */}
          <div className="col-span-3">
            <div className="bg-slate-800 rounded-lg">
              <h2 className="text-lg font-semibold p-4 border-b border-slate-700">
                Policy Levers
              </h2>
              <PolicyControls
                interestRate={economicState.centralBankRate}
                atZeroLowerBound={economicState.atZeroLowerBound}
                isDeleveraging={economicState.deleveraging.isDeleveraging}
                deleveragingLevers={economicState.deleveraging.levers}
                onInterestRateChange={setInterestRate}
                onTriggerQE={triggerQE}
                onDeleveragingLeverChange={setDeleveragingLevers}
              />
            </div>
          </div>
        </div>

        {/* Dalio's Rules */}
        <div className="bg-slate-800 rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-3">Dalio's Three Rules of Thumb</h2>
          <div className="grid grid-cols-3 gap-4">
            <RuleCard
              number={1}
              title="Debt vs Income"
              description="Don't have debt rise faster than income"
              value={economicState.rules.debtVsIncomeGrowth}
              isGood={economicState.rules.debtVsIncomeGrowth <= 0}
            />
            <RuleCard
              number={2}
              title="Income vs Productivity"
              description="Don't have income rise faster than productivity"
              value={economicState.rules.incomeVsProductivityGrowth}
              isGood={economicState.rules.incomeVsProductivityGrowth <= 0.01}
            />
            <RuleCard
              number={3}
              title="Productivity Growth"
              description="Do all you can to raise productivity"
              value={economicState.rules.productivityGrowth}
              isGood={economicState.rules.productivityGrowth >= 0.02}
              format="percent"
            />
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center text-slate-500 text-sm py-4">
          Based on Ray Dalio's "How The Economic Machine Works"
          <span className="mx-2">|</span>
          Educational simulation - not financial advice
        </footer>
      </main>
    </div>
  );
}

interface RuleCardProps {
  number: number;
  title: string;
  description: string;
  value: number;
  isGood: boolean;
  format?: 'delta' | 'percent';
}

const RuleCard: React.FC<RuleCardProps> = ({
  number,
  title,
  description,
  value,
  isGood,
  format = 'delta'
}) => {
  const displayValue = format === 'percent'
    ? `${(value * 100).toFixed(1)}%`
    : `${value >= 0 ? '+' : ''}${(value * 100).toFixed(2)}%`;

  return (
    <div className={`p-4 rounded-lg border ${
      isGood ? 'border-green-600 bg-green-900/20' : 'border-red-600 bg-red-900/20'
    }`}>
      <div className="flex items-start justify-between">
        <div className={`text-2xl font-bold ${isGood ? 'text-green-400' : 'text-red-400'}`}>
          #{number}
        </div>
        <div className={`text-lg font-mono ${isGood ? 'text-green-400' : 'text-red-400'}`}>
          {displayValue}
        </div>
      </div>
      <h3 className="font-semibold text-white mt-2">{title}</h3>
      <p className="text-sm text-slate-400">{description}</p>
      <div className="mt-2">
        {isGood ? (
          <span className="text-xs text-green-400">Following rule</span>
        ) : (
          <span className="text-xs text-red-400">Rule violated</span>
        )}
      </div>
    </div>
  );
};

export default App;
