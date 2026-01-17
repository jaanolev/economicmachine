/**
 * Household Actor Model
 *
 * Households are the primary consumers and workers in the economy.
 * They earn income (wages + investments), spend, save, and borrow.
 */

import { Entity, EntityId, Money, Percentage } from '../../types';
import { CreditAgreement, Creditworthiness, calculateCreditworthiness, calculateDebtBurden } from '../Credit';

export interface Household extends Entity {
  type: 'household';

  // Income (one person's spending is another's income!)
  wages: Money;
  investmentIncome: Money;

  // Assets
  cash: Money;
  savings: Money;
  financialAssets: Money;  // Stocks, bonds
  realAssets: Money;       // Property (collateral)

  // Liabilities
  debts: CreditAgreement[];

  // Behavioral parameters
  propensityToConsume: Percentage;  // How much of income goes to spending
  propensityToSave: Percentage;     // How much goes to savings
  propensityToBorrow: Percentage;   // Willingness to take on debt
}

/**
 * Create a new household
 */
export function createHousehold(
  id: EntityId,
  name: string,
  initialCash: Money,
  initialWages: Money
): Household {
  return {
    id,
    type: 'household',
    name,
    wages: initialWages,
    investmentIncome: 0,
    cash: initialCash,
    savings: initialCash * 0.5,
    financialAssets: initialCash * 0.3,
    realAssets: initialCash * 2,  // Home value
    debts: [],
    propensityToConsume: 0.7,
    propensityToSave: 0.2,
    propensityToBorrow: 0.3
  };
}

/**
 * Get total income
 */
export function getHouseholdIncome(household: Household): Money {
  return household.wages + household.investmentIncome;
}

/**
 * Get total assets (for collateral)
 */
export function getHouseholdAssets(household: Household): Money {
  return household.cash + household.savings + household.financialAssets + household.realAssets;
}

/**
 * Get household creditworthiness
 */
export function getHouseholdCreditworthiness(household: Household): Creditworthiness {
  const income = getHouseholdIncome(household);
  const debtBurden = calculateDebtBurden(household.debts, income);
  const collateral = getHouseholdAssets(household);

  return calculateCreditworthiness(
    income,
    debtBurden.totalDebt,
    debtBurden.annualDebtService,
    collateral
  );
}

/**
 * Calculate how much household will spend this period
 * Based on income, wealth effect, and credit availability
 */
export function calculateHouseholdSpending(
  household: Household,
  creditAvailable: Money,
  wealthEffect: number  // How much asset prices changed
): { fromMoney: Money; fromCredit: Money } {
  const income = getHouseholdIncome(household);

  // Base spending from income
  let baseSpending = income * household.propensityToConsume;

  // Wealth effect: when assets rise, people spend more
  const wealthBonus = (household.financialAssets + household.realAssets) * wealthEffect * 0.05;
  baseSpending += wealthBonus;

  // How much from cash vs credit?
  const fromMoney = Math.min(baseSpending, household.cash * 0.3);
  const desiredCredit = (baseSpending - fromMoney) * household.propensityToBorrow;
  const fromCredit = Math.min(desiredCredit, creditAvailable);

  return { fromMoney, fromCredit };
}
