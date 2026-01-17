/**
 * Short-Term Debt Cycle System
 *
 * Dalio's Second Force: The Short-Term Debt Cycle (5-8 years)
 *
 * "In short-term debt cycles, spending is constrained only by the
 * willingness of lenders and borrowers to provide and receive credit.
 * When credit is easily available, there's economic expansion.
 * When credit isn't easily available, there's a recession."
 *
 * The cycle:
 * EXPANSION: Credit grows → Spending grows → Incomes rise → Asset prices rise
 * PEAK: Inflation rises → Central bank raises rates
 * CONTRACTION: Credit shrinks → Spending falls → Recession
 * TROUGH: Central bank lowers rates → Credit starts growing again
 */

import { System } from './System';
import { WorldState } from '../WorldState';
import { ShortTermCyclePhase } from '../../core/types';
import { applyMP1, updateInflation } from '../../core/models/actors/CentralBank';
import { updateLendingStandards } from '../../core/models/actors/Bank';

export class ShortTermCycleSystem implements System {
  name = 'ShortTermCycleSystem';

  private cyclePeriodMonths: number;

  constructor(cyclePeriodMonths: number = 72) {  // 6 years default
    this.cyclePeriodMonths = cyclePeriodMonths;
  }

  process(state: WorldState, deltaMonths: number): void {
    const cycle = state.economy.shortTermCycle;

    // Advance cycle position
    cycle.positionInCycle += deltaMonths / cycle.cycleLengthMonths;

    // Wrap around to new cycle
    if (cycle.positionInCycle >= 1) {
      cycle.positionInCycle -= 1;
      cycle.cycleNumber += 1;

      // Each cycle can have slightly different length (randomness)
      cycle.cycleLengthMonths = this.cyclePeriodMonths * (0.85 + Math.random() * 0.3);
    }

    // Determine phase based on position
    const prevPhase = cycle.phase;
    cycle.phase = this.determinePhase(cycle.positionInCycle);

    // Apply phase-specific effects
    this.applyPhaseEffects(state, cycle.phase, prevPhase);

    // Central bank responds to cycle
    this.centralBankResponse(state);

    // Banks adjust lending standards
    this.updateBankBehavior(state);
  }

  private determinePhase(position: number): ShortTermCyclePhase {
    // Expansion is longest phase
    if (position < 0.45) return 'expansion';
    if (position < 0.55) return 'peak';
    if (position < 0.90) return 'contraction';
    return 'trough';
  }

  private applyPhaseEffects(
    state: WorldState,
    phase: ShortTermCyclePhase,
    prevPhase: ShortTermCyclePhase
  ): void {
    const eco = state.economy;

    // Credit growth multiplier based on phase
    // Dalio: Credit is the key driver of short-term cycles
    let creditMultiplier = 1;
    let spendingMultiplier = 1;

    switch (phase) {
      case 'expansion':
        // Credit expands, spending grows, incomes rise
        creditMultiplier = 1.005;  // 0.5% monthly = ~6% annual
        spendingMultiplier = 1.003;

        // Asset prices rise (wealth effect)
        eco.assetPriceInflation = 0.005;

        // Unemployment falls
        eco.unemployment = Math.max(0.03, eco.unemployment - 0.001);
        break;

      case 'peak':
        // Credit growth slows, inflation high
        creditMultiplier = 1.001;
        spendingMultiplier = 1.001;

        // Inflation peaks
        eco.inflation = Math.min(0.05, eco.inflation + 0.001);
        break;

      case 'contraction':
        // Credit contracts, spending falls
        creditMultiplier = 0.998;  // Credit shrinking
        spendingMultiplier = 0.997;

        // Asset prices fall
        eco.assetPriceInflation = -0.003;

        // Unemployment rises
        eco.unemployment = Math.min(0.12, eco.unemployment + 0.002);

        // Inflation falls
        eco.inflation = Math.max(-0.01, eco.inflation - 0.002);
        break;

      case 'trough':
        // Bottom of cycle, credit stabilizes
        creditMultiplier = 1.0;
        spendingMultiplier = 0.999;

        // Unemployment peaks
        eco.unemployment = Math.min(0.10, eco.unemployment + 0.001);
        break;
    }

    // Apply multipliers
    eco.spendingFromCredit *= creditMultiplier;
    eco.totalSpending = eco.spendingFromMoney + eco.spendingFromCredit;
    eco.creditAsPercentOfSpending = eco.spendingFromCredit / eco.totalSpending;

    // GDP follows spending (Dalio: spending = income)
    const prevGDP = eco.nominalGDP;
    eco.nominalGDP *= spendingMultiplier;

    // Real GDP accounts for inflation
    eco.realGDP = eco.nominalGDP / (eco.priceLevel / 100);

    // Update output gap
    eco.outputGap = (eco.realGDP - eco.potentialGDP) / eco.potentialGDP;

    // Credit growth (year-over-year approximation)
    eco.creditGrowth = (creditMultiplier - 1) * 12;

    // Update price level
    eco.priceLevel *= (1 + eco.inflation / 12);

    // Log phase transitions
    if (phase !== prevPhase) {
      console.log(`Short-term cycle: ${prevPhase} → ${phase} (cycle #${eco.shortTermCycle.cycleNumber})`);
    }
  }

  private centralBankResponse(state: WorldState): void {
    const eco = state.economy;
    const cb = state.centralBank;

    // Update inflation tracking
    const spendingGrowth = eco.creditGrowth + 0.02;  // Approximate
    updateInflation(cb, spendingGrowth, eco.productivityGrowthRate);

    // Apply monetary policy (MP1 in normal times)
    if (!cb.atZeroLowerBound) {
      applyMP1(cb, eco.outputGap);
    }

    // Update market rates based on policy rate
    eco.centralBankRate = cb.policyRate;
    eco.marketRates.shortTerm = cb.policyRate + 0.005;
    eco.marketRates.longTerm = cb.policyRate + 0.015;
    eco.marketRates.mortgage = cb.policyRate + 0.02;
    eco.marketRates.corporate = cb.policyRate + 0.025;

    eco.atZeroLowerBound = cb.atZeroLowerBound;
  }

  private updateBankBehavior(state: WorldState): void {
    const eco = state.economy;

    // Get average default rate
    const totalLoans = state.banks.reduce((sum, b) => sum + b.loans.length, 0);
    const defaultedLoans = state.banks.reduce((sum, b) =>
      sum + b.loans.filter(l => l.status === 'defaulted').length, 0);
    const defaultRate = totalLoans > 0 ? defaultedLoans / totalLoans : 0;

    // Banks adjust lending standards
    state.banks.forEach(bank => {
      updateLendingStandards(
        bank,
        defaultRate,
        eco.outputGap,  // Using output gap as growth proxy
        eco.centralBankRate
      );
    });

    // Update aggregate credit availability
    eco.creditAvailability = state.banks.reduce((sum, b) =>
      sum + b.creditAvailability, 0) / state.banks.length;
    eco.lendingStandards = state.banks[0]?.lendingStandards || 'normal';
  }

  /**
   * Get cycle wave for charting
   * Returns the short-term cycle oscillation around productivity trend
   */
  getCycleWave(
    startMonth: number,
    endMonth: number,
    baseLevel: number,
    amplitude: number = 0.03
  ): number[] {
    const wave: number[] = [];

    for (let m = startMonth; m <= endMonth; m++) {
      const position = (m % this.cyclePeriodMonths) / this.cyclePeriodMonths;
      // Sinusoidal wave
      const cycleEffect = amplitude * Math.sin(2 * Math.PI * position);
      wave.push(baseLevel * (1 + cycleEffect));
    }

    return wave;
  }
}
