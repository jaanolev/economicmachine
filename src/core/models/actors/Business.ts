/**
 * Business Actor Model
 *
 * Businesses produce goods/services, employ workers, invest, and borrow.
 * Their productivity is the key long-term driver of economic growth.
 */

import { Entity, EntityId, Money, Percentage, CreditPurpose } from '../../types';
import { CreditAgreement, calculateDebtBurden } from '../Credit';

export interface Business extends Entity {
  type: 'business';

  // Operations
  revenue: Money;
  costs: Money;
  employees: number;
  productivity: number;  // Output per worker (Dalio's key long-term factor)

  // Balance Sheet - Assets
  cash: Money;
  inventory: Money;
  equipment: Money;    // Productive capital

  // Balance Sheet - Liabilities
  debts: CreditAgreement[];

  // Investment tracking (good vs bad credit)
  productiveInvestment: Money;   // Investment that increases productivity
  speculativeInvestment: Money;  // Investment in financial assets

  // Behavioral parameters
  investmentRate: Percentage;    // How much profit goes to investment
  hiringThreshold: number;       // Revenue/employee ratio to trigger hiring
}

/**
 * Create a new business
 */
export function createBusiness(
  id: EntityId,
  name: string,
  initialCash: Money,
  employees: number,
  productivity: number
): Business {
  return {
    id,
    type: 'business',
    name,
    revenue: employees * productivity,
    costs: employees * productivity * 0.7,  // 70% costs
    employees,
    productivity,
    cash: initialCash,
    inventory: initialCash * 0.5,
    equipment: initialCash * 2,
    debts: [],
    productiveInvestment: 0,
    speculativeInvestment: 0,
    investmentRate: 0.3,
    hiringThreshold: productivity * 1.2
  };
}

/**
 * Get business profit
 */
export function getBusinessProfit(business: Business): Money {
  return business.revenue - business.costs;
}

/**
 * Get total business assets
 */
export function getBusinessAssets(business: Business): Money {
  return business.cash + business.inventory + business.equipment;
}

/**
 * Calculate business credit needs
 * Businesses borrow for productive investment (good credit) or speculation (bad credit)
 */
export function calculateBusinessCreditDemand(
  business: Business,
  interestRate: Percentage,
  economicOutlook: number  // -1 to 1
): { amount: Money; purpose: CreditPurpose } {
  const profit = getBusinessProfit(business);

  // Productive investment: when expected return > borrowing cost
  const expectedProductivityReturn = 0.08;  // 8% return on productive investment
  const wantsProductiveInvestment = expectedProductivityReturn > interestRate;

  // More investment when outlook is positive
  const outlookMultiplier = 1 + economicOutlook * 0.5;

  if (wantsProductiveInvestment && economicOutlook > -0.3) {
    // Borrow for productive investment
    const investmentDesired = profit * business.investmentRate * outlookMultiplier;
    return { amount: investmentDesired, purpose: 'productive' };
  } else if (economicOutlook > 0.3) {
    // In boom times, some speculative borrowing
    return { amount: profit * 0.1, purpose: 'speculative' };
  }

  return { amount: 0, purpose: 'productive' };
}

/**
 * Update business productivity
 * Dalio: Productivity is the most important long-term factor
 */
export function updateBusinessProductivity(
  business: Business,
  productivityGrowthRate: Percentage
): void {
  // Base productivity growth
  business.productivity *= (1 + productivityGrowthRate / 12);  // Monthly

  // Productive investment boosts productivity further
  if (business.productiveInvestment > 0) {
    const investmentBoost = (business.productiveInvestment / business.equipment) * 0.01;
    business.productivity *= (1 + investmentBoost);
  }
}

/**
 * Decide on hiring/firing based on demand
 */
export function calculateEmploymentChange(
  business: Business,
  demandChange: Percentage
): number {
  const revenuePerEmployee = business.revenue / business.employees;

  if (demandChange > 0.05 && revenuePerEmployee > business.hiringThreshold) {
    // Hire when demand is growing and employees are productive
    return Math.ceil(business.employees * demandChange * 0.5);
  } else if (demandChange < -0.05) {
    // Layoffs when demand falling
    return -Math.ceil(business.employees * Math.abs(demandChange) * 0.3);
  }

  return 0;
}
