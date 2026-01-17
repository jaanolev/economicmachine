/**
 * Long-Term Debt Cycle System
 *
 * Dalio's Third Force: The Long-Term Debt Cycle (75-100 years)
 *
 * "Over decades, debts rise faster than incomes, creating the long-term debt cycle"
 * "At the end, there's a deleveraging - a very different animal from a recession"
 *
 * The long-term cycle phases:
 * LEVERAGING: Debt accumulates over decades (50-75 years)
 * PEAK: Debt burden becomes unsustainable, rates hit zero
 * DELEVERAGING: Debt must come down relative to income (10+ years)
 * REFLATION: Economy recovers, new cycle begins
 */

import { System } from './System';
import { WorldState } from '../WorldState';
import { LongTermCyclePhase } from '../../core/types';
import { shouldTriggerDeleveraging, isBeautifulDeleveraging } from '../../core/models/EconomicState';
import { applyMP2, applyMP3 } from '../../core/models/actors/CentralBank';

export class LongTermCycleSystem implements System {
  name = 'LongTermCycleSystem';

  private cyclePeriodYears: number;
  private debtToGDPHistory: number[] = [];

  constructor(cyclePeriodYears: number = 75) {
    this.cyclePeriodYears = cyclePeriodYears;
  }

  process(state: WorldState, deltaMonths: number): void {
    const eco = state.economy;
    const longCycle = eco.longTermCycle;

    // Track debt to GDP history
    this.debtToGDPHistory.push(eco.debtToGDPRatio);
    if (this.debtToGDPHistory.length > 1200) {  // Keep 100 years
      this.debtToGDPHistory.shift();
    }

    // Advance time in cycle
    longCycle.yearsIntoCycle += deltaMonths / 12;

    // Track peak debt
    if (eco.debtToGDPRatio > longCycle.peakDebtToGDP) {
      longCycle.peakDebtToGDP = eco.debtToGDPRatio;
    }

    // Determine and apply phase
    const prevPhase = longCycle.phase;
    longCycle.phase = this.determinePhase(state);

    this.applyPhaseEffects(state, longCycle.phase, prevPhase);

    // Track Dalio's first rule: debt vs income growth
    this.trackDebtRule(state);
  }

  private determinePhase(state: WorldState): LongTermCyclePhase {
    const eco = state.economy;
    const delev = eco.deleveraging;

    // If already deleveraging, check if done
    if (delev.isDeleveraging) {
      // Deleveraging ends when debt/GDP back to sustainable levels
      if (eco.debtToGDPRatio < 0.5 && eco.creditGrowth > 0.02) {
        return 'reflation';
      }
      return 'deleveraging';
    }

    // Check if deleveraging should trigger
    if (shouldTriggerDeleveraging(eco)) {
      return 'deleveraging';
    }

    // Check if at peak
    if (eco.debtToGDPRatio > 0.8 && eco.atZeroLowerBound) {
      return 'peak';
    }

    // Normal leveraging phase
    return 'leveraging';
  }

  private applyPhaseEffects(
    state: WorldState,
    phase: LongTermCyclePhase,
    prevPhase: LongTermCyclePhase
  ): void {
    const eco = state.economy;
    const delev = eco.deleveraging;

    switch (phase) {
      case 'leveraging':
        // Normal debt accumulation
        // Dalio: Debt tends to rise faster than income over time
        this.applyLeveragingPhase(state);
        break;

      case 'peak':
        // Debt burden maxed out, economy straining
        this.applyPeakPhase(state);
        break;

      case 'deleveraging':
        // Must reduce debt burden
        if (!delev.isDeleveraging) {
          this.startDeleveraging(state);
        }
        this.applyDeleveragingPhase(state);
        break;

      case 'reflation':
        // Recovery after deleveraging
        this.applyReflationPhase(state);
        break;
    }

    // Log phase transitions
    if (phase !== prevPhase) {
      console.log(`Long-term cycle: ${prevPhase} → ${phase} (Year ${Math.floor(eco.longTermCycle.yearsIntoCycle)})`);
    }
  }

  private applyLeveragingPhase(state: WorldState): void {
    const eco = state.economy;

    // Debt grows slightly faster than income (the key dynamic)
    // This is subtle but accumulates over decades
    const debtGrowthPremium = 0.0002;  // 0.02% per month extra

    // Only during expansion phases of short-term cycle
    if (eco.shortTermCycle.phase === 'expansion') {
      eco.totalDebt *= (1 + debtGrowthPremium);
      eco.debtToGDPRatio = eco.totalDebt / eco.nominalGDP;
    }

    // Debt service burden creeps up
    eco.debtServiceToIncome = eco.debtToGDPRatio * eco.marketRates.longTerm * 1.2;
  }

  private applyPeakPhase(state: WorldState): void {
    const eco = state.economy;

    // At peak, growth stalls because debt burden is too high
    // Credit growth slows despite low rates
    eco.creditGrowth = Math.max(0, eco.creditGrowth - 0.001);

    // Debt service consuming more income
    eco.debtServiceToIncome = Math.min(0.5, eco.debtServiceToIncome + 0.001);

    // Central bank tries QE (MP2)
    if (eco.atZeroLowerBound) {
      applyMP2(state.centralBank, eco.nominalGDP, eco.outputGap);
    }
  }

  private startDeleveraging(state: WorldState): void {
    const eco = state.economy;
    const delev = eco.deleveraging;

    console.log('=== DELEVERAGING BEGINS ===');
    console.log(`Debt/GDP: ${(eco.debtToGDPRatio * 100).toFixed(1)}%`);
    console.log(`Debt Service/Income: ${(eco.debtServiceToIncome * 100).toFixed(1)}%`);

    delev.isDeleveraging = true;
    delev.yearsInDeleveraging = 0;

    // Start with balanced lever settings
    // Dalio: The mix of levers determines if deleveraging is beautiful or ugly
    delev.levers = {
      austerity: 0.2,
      debtRestructuring: 0.2,
      wealthTransfer: 0.1,
      moneyPrinting: 0.5  // Crucial for beautiful deleveraging
    };
  }

  private applyDeleveragingPhase(state: WorldState): void {
    const eco = state.economy;
    const delev = eco.deleveraging;

    delev.yearsInDeleveraging += 1 / 12;

    // Calculate forces
    delev.deflationaryForce = delev.levers.austerity + delev.levers.debtRestructuring;
    delev.inflationaryForce = delev.levers.moneyPrinting;

    // Apply the four levers

    // 1. Austerity - reduces spending (deflationary)
    if (delev.levers.austerity > 0) {
      const austerityEffect = delev.levers.austerity * 0.002;
      eco.totalSpending *= (1 - austerityEffect);
      state.government.spending *= (1 - austerityEffect * 0.5);
    }

    // 2. Debt restructuring - reduces debt (deflationary)
    if (delev.levers.debtRestructuring > 0) {
      const writedownRate = delev.levers.debtRestructuring * 0.001;
      eco.totalDebt *= (1 - writedownRate);
    }

    // 3. Wealth transfers - redistribution
    if (delev.levers.wealthTransfer > 0) {
      // Increase taxes on wealthy, increase transfers
      state.government.taxRate += delev.levers.wealthTransfer * 0.0001;
      state.government.transferPayments *= (1 + delev.levers.wealthTransfer * 0.002);
    }

    // 4. Money printing - monetize debt (inflationary)
    if (delev.levers.moneyPrinting > 0) {
      const monetization = eco.nominalGDP * delev.levers.moneyPrinting * 0.002;
      applyMP3(state.centralBank, monetization);

      // This puts money into economy, supporting spending
      eco.spendingFromMoney += monetization * 0.5;
      eco.totalSpending = eco.spendingFromMoney + eco.spendingFromCredit;

      // Reduces effective government debt
      state.government.debt -= monetization * 0.3;
    }

    // Net effect on inflation
    const netInflationaryEffect = delev.inflationaryForce - delev.deflationaryForce;
    eco.inflation += netInflationaryEffect * 0.002;

    // Update debt ratios
    eco.debtToGDPRatio = eco.totalDebt / eco.nominalGDP;
    eco.debtServiceToIncome = eco.debtToGDPRatio * eco.marketRates.longTerm * 1.2;

    // Determine if beautiful or ugly
    // Need to look at state vs previous state
    const balance = Math.abs(delev.inflationaryForce - delev.deflationaryForce);
    if (balance < 0.2 && eco.inflation > 0 && eco.inflation < 0.04) {
      delev.type = 'beautiful';
    } else {
      delev.type = 'ugly';
    }
  }

  private applyReflationPhase(state: WorldState): void {
    const eco = state.economy;
    const delev = eco.deleveraging;

    // Deleveraging complete
    delev.isDeleveraging = false;
    delev.type = null;

    // Reset levers
    delev.levers = {
      austerity: 0,
      debtRestructuring: 0,
      wealthTransfer: 0,
      moneyPrinting: 0
    };

    // Economy can start fresh cycle
    // Credit starts growing again
    eco.creditGrowth = Math.max(0.02, eco.creditGrowth + 0.001);

    // Reset long-term cycle
    eco.longTermCycle.yearsIntoCycle = 0;
    eco.longTermCycle.peakDebtToGDP = eco.debtToGDPRatio;

    console.log('=== DELEVERAGING COMPLETE - NEW CYCLE BEGINS ===');
  }

  private trackDebtRule(state: WorldState): void {
    const eco = state.economy;

    // Dalio's first rule: Don't have debt rise faster than income
    // Calculate year-over-year growth rates
    if (this.debtToGDPHistory.length > 12) {
      const currentDebtGDP = eco.debtToGDPRatio;
      const yearAgoDebtGDP = this.debtToGDPHistory[this.debtToGDPHistory.length - 12];
      eco.rules.debtVsIncomeGrowth = currentDebtGDP - yearAgoDebtGDP;
    }
  }

  /**
   * Get the long-term debt cycle wave for charting
   */
  getLongTermWave(
    startMonth: number,
    endMonth: number,
    baseLevel: number
  ): number[] {
    const wave: number[] = [];
    const cycleMonths = this.cyclePeriodYears * 12;

    for (let m = startMonth; m <= endMonth; m++) {
      // Very slow wave - more like a gradual rise and fall
      const position = (m % cycleMonths) / cycleMonths;

      // Asymmetric: long rise, sharp fall during deleveraging
      let cycleEffect: number;
      if (position < 0.85) {
        // Leveraging phase: gradual rise
        cycleEffect = (position / 0.85) * 0.15;
      } else {
        // Deleveraging: sharper decline
        const delevPosition = (position - 0.85) / 0.15;
        cycleEffect = 0.15 - (delevPosition * 0.15 * 1.5);
      }

      wave.push(baseLevel * (1 + cycleEffect));
    }

    return wave;
  }

  /**
   * Manually adjust deleveraging levers (for user interaction)
   */
  setDeleveragingLevers(
    state: WorldState,
    levers: {
      austerity?: number;
      debtRestructuring?: number;
      wealthTransfer?: number;
      moneyPrinting?: number;
    }
  ): void {
    const delev = state.economy.deleveraging;

    if (levers.austerity !== undefined) {
      delev.levers.austerity = Math.max(0, Math.min(1, levers.austerity));
    }
    if (levers.debtRestructuring !== undefined) {
      delev.levers.debtRestructuring = Math.max(0, Math.min(1, levers.debtRestructuring));
    }
    if (levers.wealthTransfer !== undefined) {
      delev.levers.wealthTransfer = Math.max(0, Math.min(1, levers.wealthTransfer));
    }
    if (levers.moneyPrinting !== undefined) {
      delev.levers.moneyPrinting = Math.max(0, Math.min(1, levers.moneyPrinting));
    }
  }
}
