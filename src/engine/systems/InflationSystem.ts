/**
 * Inflation System
 *
 * Dalio: "Inflation = Spending Growth - Productivity Growth"
 *
 * When spending grows faster than output, prices rise.
 * When output grows faster than spending, prices fall.
 */

import { System } from './System';
import { WorldState } from '../WorldState';

export class InflationSystem implements System {
  name = 'InflationSystem';

  private spendingHistory: number[] = [];

  process(state: WorldState, deltaMonths: number): void {
    const eco = state.economy;

    // Track spending history
    this.spendingHistory.push(eco.totalSpending);
    if (this.spendingHistory.length > 12) {
      this.spendingHistory.shift();
    }

    // Calculate spending growth (year-over-year approximation)
    let spendingGrowth = 0;
    if (this.spendingHistory.length >= 12) {
      const currentSpending = eco.totalSpending;
      const yearAgoSpending = this.spendingHistory[0];
      spendingGrowth = (currentSpending - yearAgoSpending) / yearAgoSpending;
    }

    // Dalio's inflation formula
    const productivityGrowth = eco.productivityGrowthRate;
    const calculatedInflation = spendingGrowth - productivityGrowth;

    // Smooth the inflation (doesn't change instantly)
    eco.inflation = eco.inflation * 0.9 + calculatedInflation * 0.1;

    // Update price level
    eco.priceLevel *= (1 + eco.inflation / 12);

    // Update real GDP
    eco.realGDP = eco.nominalGDP / (eco.priceLevel / 100);

    // Update Dalio's second rule tracking
    eco.rules.incomeVsProductivityGrowth = eco.wageGrowth - productivityGrowth;

    // Wage growth follows inflation with lag
    eco.wageGrowth = eco.wageGrowth * 0.8 + (eco.inflation + productivityGrowth) * 0.2;
  }
}
