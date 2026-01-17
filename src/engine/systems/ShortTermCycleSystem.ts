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
    // Expansion is longest phase (realistic business cycle)
    // Typical cycle: ~5 years expansion, ~1 year contraction
    if (position < 0.55) return 'expansion';   // 55% of cycle
    if (position < 0.65) return 'peak';        // 10% of cycle
    if (position < 0.85) return 'contraction'; // 20% of cycle
    return 'trough';                            // 15% of cycle
  }

  private applyPhaseEffects(
    state: WorldState,
    phase: ShortTermCyclePhase,
    prevPhase: ShortTermCyclePhase
  ): void {
    const eco = state.economy;

    // Base growth from productivity (always positive)
    const monthlyProductivityGrowth = eco.productivityGrowthRate / 12;

    // Credit growth multiplier based on phase
    // Dalio: Credit is the key driver of short-term cycles
    let creditMultiplier = 1;
    let inflationAdjustment = 0;

    switch (phase) {
      case 'expansion':
        // Credit expands faster than productivity - creates boom
        creditMultiplier = 1.006;  // ~7% annual credit growth
        inflationAdjustment = 0.002;  // Inflation rises

        // Asset prices rise (wealth effect)
        eco.assetPriceInflation = 0.005;

        // Unemployment falls
        eco.unemployment = Math.max(0.03, eco.unemployment - 0.002);
        break;

      case 'peak':
        // Credit growth slows, inflation high
        creditMultiplier = 1.002;
        inflationAdjustment = 0.001;  // Inflation still rising but slower

        // Unemployment stabilizes
        eco.unemployment = Math.max(0.03, eco.unemployment - 0.0005);
        break;

      case 'contraction':
        // Credit contracts, but not as severely
        creditMultiplier = 0.9985;  // Mild credit contraction
        inflationAdjustment = -0.001;  // Inflation falls

        // Asset prices fall
        eco.assetPriceInflation = -0.002;

        // Unemployment rises
        eco.unemployment = Math.min(0.10, eco.unemployment + 0.002);
        break;

      case 'trough':
        // Bottom of cycle, credit stabilizes, recovery begins
        creditMultiplier = 1.001;  // Credit starts growing again
        inflationAdjustment = -0.0005;  // Inflation bottoms

        // Unemployment peaks then stabilizes
        eco.unemployment = Math.min(0.08, eco.unemployment + 0.0005);
        break;
    }

    // Apply credit growth
    eco.spendingFromCredit *= creditMultiplier;

    // Money supply grows with productivity (base money)
    eco.spendingFromMoney *= (1 + monthlyProductivityGrowth);

    // Total spending = money + credit (Dalio's key equation)
    eco.totalSpending = eco.spendingFromMoney + eco.spendingFromCredit;
    eco.creditAsPercentOfSpending = eco.spendingFromCredit / eco.totalSpending;

    // GDP follows spending (Dalio: one person's spending = another's income)
    // Nominal GDP grows with total spending
    const spendingGrowth = (creditMultiplier - 1) + monthlyProductivityGrowth;
    eco.nominalGDP *= (1 + spendingGrowth);

    // Inflation = spending growth - productivity growth (Dalio's formula)
    const impliedInflation = spendingGrowth * 12 - eco.productivityGrowthRate;
    eco.inflation = eco.inflation * 0.9 + (impliedInflation + inflationAdjustment) * 0.1;

    // Clamp inflation to reasonable bounds
    eco.inflation = Math.max(-0.03, Math.min(0.08, eco.inflation));

    // Update price level
    eco.priceLevel *= (1 + eco.inflation / 12);

    // Real GDP = Nominal GDP / Price Level
    eco.realGDP = eco.nominalGDP / (eco.priceLevel / 100);

    // Output gap (how far from potential)
    eco.outputGap = (eco.realGDP - eco.potentialGDP) / eco.potentialGDP;

    // Credit growth (annualized)
    eco.creditGrowth = (creditMultiplier - 1) * 12;

    // Wage growth follows productivity + some inflation pass-through
    eco.wageGrowth = eco.productivityGrowthRate + eco.inflation * 0.5;

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
