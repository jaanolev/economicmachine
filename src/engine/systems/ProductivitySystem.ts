/**
 * Productivity System
 *
 * Dalio's First Force: Productivity Growth
 *
 * "Productivity matters most in the long run"
 * "It doesn't fluctuate much, so it's not a big driver of economic swings"
 *
 * This creates the steady upward trend that the economy oscillates around.
 * Growth rate: ~2-3% annually
 */

import { System } from './System';
import { WorldState } from '../WorldState';
import { updateBusinessProductivity } from '../../core/models/actors/Business';

export class ProductivitySystem implements System {
  name = 'ProductivitySystem';

  private baseProductivity: number = 100;
  private annualGrowthRate: number;

  constructor(annualGrowthRate: number = 0.025) {
    this.annualGrowthRate = annualGrowthRate;
  }

  process(state: WorldState, deltaMonths: number): void {
    const monthlyGrowthRate = this.annualGrowthRate / 12;

    // Update productivity level
    state.economy.productivityLevel *= (1 + monthlyGrowthRate * deltaMonths);
    state.economy.productivityGrowthRate = this.annualGrowthRate;

    // Update potential GDP based on productivity
    // Potential GDP = Productivity * Labor Force
    const laborForce = state.households.length;
    state.economy.potentialGDP = state.economy.productivityLevel * laborForce;

    // Update each business's productivity
    state.businesses.forEach(business => {
      updateBusinessProductivity(business, this.annualGrowthRate);
    });

    // Track Dalio's third rule: maximize productivity
    state.economy.rules.productivityGrowth = this.annualGrowthRate;
  }

  /**
   * Get productivity trend line for charting
   */
  getProductivityTrend(startMonth: number, endMonth: number, startLevel: number): number[] {
    const trend: number[] = [];
    const monthlyGrowth = this.annualGrowthRate / 12;

    for (let m = startMonth; m <= endMonth; m++) {
      const monthsElapsed = m - startMonth;
      trend.push(startLevel * Math.pow(1 + monthlyGrowth, monthsElapsed));
    }

    return trend;
  }

  /**
   * Set productivity growth rate (for scenarios)
   */
  setGrowthRate(rate: number): void {
    this.annualGrowthRate = rate;
  }
}
