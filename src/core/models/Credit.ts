/**
 * Credit and Debt Models
 *
 * Dalio's insights on credit:
 * - "Credit is the most important part of the economy"
 * - "As soon as credit is created, it immediately turns into debt"
 * - "Debt is an asset to the lender, and a liability to the borrower"
 * - Credit can be "good" (finances productive investment) or "bad" (excess consumption)
 */

import { EntityId, Money, Percentage, TimeStep, CreditPurpose, CreditStatus } from '../types';

/**
 * A credit agreement between lender and borrower
 * Dalio: "One person's debt is another person's asset"
 */
export interface CreditAgreement {
  id: string;
  createdAt: TimeStep;
  maturityDate: TimeStep;

  // Parties
  lenderId: EntityId;
  borrowerId: EntityId;

  // Terms
  principal: Money;
  interestRate: Percentage;  // Annual rate
  monthlyPayment: Money;

  // Current state
  remainingPrincipal: Money;
  totalInterestPaid: Money;
  status: CreditStatus;

  // Dalio's good vs bad credit
  purpose: CreditPurpose;
  expectedReturnRate: Percentage;  // For productive credit

  // Collateral (part of creditworthiness)
  collateralValue: Money;
  borrowerIncomeAtOrigination: Money;
}

/**
 * Creditworthiness assessment
 * Dalio: Two factors determine creditworthiness:
 * 1. Ability to repay (income relative to debt)
 * 2. Collateral (assets that can be seized)
 */
export interface Creditworthiness {
  // Dalio's two factors
  abilityToRepay: Percentage;     // Income / Debt service
  collateralCoverage: Percentage; // Collateral / Debt

  // Derived score
  overallScore: Percentage;
  maxBorrowingCapacity: Money;

  // Risk assessment
  debtToIncomeRatio: Percentage;
  debtServiceRatio: Percentage;
}

/**
 * Debt burden metrics
 * Key for determining when deleveraging triggers
 */
export interface DebtBurden {
  totalDebt: Money;
  annualDebtService: Money;  // Principal + Interest payments per year
  debtToIncomeRatio: Percentage;
  debtServiceToIncomeRatio: Percentage;  // Critical for deleveraging trigger
}

/**
 * Create a new credit agreement
 */
export function createCreditAgreement(
  lenderId: EntityId,
  borrowerId: EntityId,
  principal: Money,
  interestRate: Percentage,
  termMonths: number,
  purpose: CreditPurpose,
  collateralValue: Money,
  borrowerIncome: Money,
  currentTime: TimeStep
): CreditAgreement {
  // Calculate monthly payment (standard amortization)
  const monthlyRate = interestRate / 12;
  const monthlyPayment = principal *
    (monthlyRate * Math.pow(1 + monthlyRate, termMonths)) /
    (Math.pow(1 + monthlyRate, termMonths) - 1);

  return {
    id: `credit-${currentTime}-${Math.random().toString(36).substr(2, 9)}`,
    createdAt: currentTime,
    maturityDate: currentTime + termMonths,
    lenderId,
    borrowerId,
    principal,
    interestRate,
    monthlyPayment: isFinite(monthlyPayment) ? monthlyPayment : principal / termMonths,
    remainingPrincipal: principal,
    totalInterestPaid: 0,
    status: 'active',
    purpose,
    expectedReturnRate: purpose === 'productive' ? interestRate * 1.5 : 0,
    collateralValue,
    borrowerIncomeAtOrigination: borrowerIncome
  };
}

/**
 * Calculate creditworthiness
 * Dalio: Creditworthiness = Ability to Repay + Collateral
 */
export function calculateCreditworthiness(
  income: Money,
  totalDebt: Money,
  annualDebtService: Money,
  collateral: Money
): Creditworthiness {
  const debtToIncomeRatio = income > 0 ? totalDebt / income : Infinity;
  const debtServiceRatio = income > 0 ? annualDebtService / income : Infinity;

  // Ability to repay: can they service existing debt?
  // Score decreases as debt service approaches income
  const abilityToRepay = Math.max(0, Math.min(1, 1 - debtServiceRatio));

  // Collateral coverage: do assets cover debts?
  const collateralCoverage = totalDebt > 0
    ? Math.min(1, collateral / totalDebt)
    : 1;

  // Overall score: weighted average (Dalio emphasizes income more)
  const overallScore = (abilityToRepay * 0.6) + (collateralCoverage * 0.4);

  // Max borrowing: based on income and existing debt
  const maxDebtServiceRatio = 0.4;  // 40% of income
  const availableForDebtService = Math.max(0, income * maxDebtServiceRatio - annualDebtService);
  const maxBorrowingCapacity = availableForDebtService * 10;  // Rough approximation

  return {
    abilityToRepay,
    collateralCoverage,
    overallScore,
    maxBorrowingCapacity,
    debtToIncomeRatio,
    debtServiceRatio
  };
}

/**
 * Is this "good" credit? (Dalio's distinction)
 * Good credit: finances productive investment that generates income to repay
 * Bad credit: finances excess consumption that can't be paid back
 */
export function isGoodCredit(agreement: CreditAgreement): boolean {
  return (
    agreement.purpose === 'productive' &&
    agreement.expectedReturnRate > agreement.interestRate
  );
}

/**
 * Calculate debt burden
 */
export function calculateDebtBurden(
  debts: CreditAgreement[],
  annualIncome: Money
): DebtBurden {
  const activeDebts = debts.filter(d => d.status === 'active');

  const totalDebt = activeDebts.reduce((sum, d) => sum + d.remainingPrincipal, 0);
  const annualDebtService = activeDebts.reduce((sum, d) => sum + d.monthlyPayment * 12, 0);

  return {
    totalDebt,
    annualDebtService,
    debtToIncomeRatio: annualIncome > 0 ? totalDebt / annualIncome : Infinity,
    debtServiceToIncomeRatio: annualIncome > 0 ? annualDebtService / annualIncome : Infinity
  };
}
