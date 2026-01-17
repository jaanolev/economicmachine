/**
 * Government Actor Model
 *
 * The government plays a key role in Dalio's framework:
 * - Fiscal policy (spending, taxes) is one of the deleveraging levers
 * - Wealth transfers from rich to poor is another lever
 * - Government debt is part of total economy debt
 */

import { Entity, EntityId, Money, Percentage, FiscalStance } from '../../types';

export interface Government extends Entity {
  type: 'government';

  // Revenue
  taxRevenue: Money;
  taxRate: Percentage;  // Effective tax rate

  // Spending
  spending: Money;
  transferPayments: Money;  // Redistribution (welfare, social security)

  // Balance
  debt: Money;
  deficit: Money;  // Spending - Revenue (positive = deficit)
  debtToGDP: Percentage;

  // Policy stance
  fiscalStance: FiscalStance;

  // Deleveraging tools
  austerityLevel: Percentage;      // 0-1, how much spending cut
  wealthTransferLevel: Percentage; // 0-1, how much redistribution
}

/**
 * Create a new government
 */
export function createGovernment(
  id: EntityId,
  name: string,
  gdp: Money
): Government {
  const taxRate = 0.25;  // 25% effective tax rate
  const taxRevenue = gdp * taxRate;
  const spending = taxRevenue * 1.05;  // Small deficit

  return {
    id,
    type: 'government',
    name,
    taxRevenue,
    taxRate,
    spending,
    transferPayments: spending * 0.3,  // 30% of spending is transfers
    debt: gdp * 0.6,  // 60% debt to GDP
    deficit: spending - taxRevenue,
    debtToGDP: 0.6,
    fiscalStance: 'neutral',
    austerityLevel: 0,
    wealthTransferLevel: 0.3
  };
}

/**
 * Update government finances based on economic conditions
 */
export function updateGovernmentFinances(
  government: Government,
  gdp: Money,
  unemployment: Percentage
): void {
  // Tax revenue depends on GDP
  government.taxRevenue = gdp * government.taxRate;

  // Automatic stabilizers: transfers increase when unemployment rises
  const baseTransfers = government.spending * 0.25;
  const unemploymentBonus = unemployment * government.spending * 0.5;
  government.transferPayments = baseTransfers + unemploymentBonus;

  // Calculate deficit
  government.deficit = government.spending + government.transferPayments - government.taxRevenue;

  // Debt accumulates
  government.debt += government.deficit / 12;  // Monthly

  // Update debt to GDP
  government.debtToGDP = gdp > 0 ? government.debt / gdp : 0;
}

/**
 * Apply fiscal policy based on stance
 * Dalio: Fiscal policy is crucial during deleveraging
 */
export function applyFiscalPolicy(
  government: Government,
  gdp: Money,
  isDeleveraging: boolean
): void {
  if (isDeleveraging) {
    // During deleveraging, fiscal policy becomes critical
    switch (government.fiscalStance) {
      case 'austerity':
        // Cut spending (deflationary)
        government.spending *= (1 - government.austerityLevel * 0.1);
        government.transferPayments *= (1 - government.austerityLevel * 0.05);
        break;

      case 'stimulus':
        // Increase spending (inflationary if monetized)
        government.spending *= 1.1;
        government.transferPayments *= 1.2;
        break;

      case 'neutral':
        // Maintain current levels
        break;
    }
  } else {
    // Normal times: counter-cyclical policy
    // (This is simplified; real policy is more complex)
  }
}

/**
 * Apply wealth transfer (Dalio's 3rd deleveraging lever)
 * Transfer from wealthy to poor to support spending
 */
export function applyWealthTransfer(
  government: Government,
  wealthyAssets: Money,
  intensity: Percentage
): Money {
  // Additional tax on wealthy
  const additionalTax = wealthyAssets * intensity * 0.05;
  government.taxRevenue += additionalTax;

  // Increase transfer payments
  const additionalTransfers = additionalTax * 0.8;  // 80% goes to transfers
  government.transferPayments += additionalTransfers;

  return additionalTransfers;
}

/**
 * Calculate fiscal multiplier effect on GDP
 * Government spending has a multiplier effect
 */
export function calculateFiscalMultiplier(
  government: Government,
  marginalPropensityToConsume: Percentage
): number {
  // Simple Keynesian multiplier
  // Multiplier = 1 / (1 - MPC)
  const multiplier = 1 / (1 - marginalPropensityToConsume);

  // Tax leakage reduces multiplier
  const taxAdjustedMultiplier = multiplier * (1 - government.taxRate);

  return Math.min(3, taxAdjustedMultiplier);  // Cap at 3x
}
