/**
 * Bank Actor Model
 *
 * Banks are the critical intermediaries that CREATE credit.
 * Dalio: "Credit is the most important part of the economy"
 *
 * When a bank makes a loan, it creates credit (and debt) out of thin air.
 * This is how most "money" in the economy is actually created.
 */

import { Entity, EntityId, Money, Percentage, LendingStandards } from '../../types';
import { CreditAgreement, Creditworthiness } from '../Credit';

export interface Bank extends Entity {
  type: 'bank';

  // Assets (what the bank owns)
  loans: CreditAgreement[];      // Credit extended = bank's asset
  reserves: Money;               // Cash at central bank
  securities: Money;             // Government bonds, etc.

  // Liabilities (what the bank owes)
  deposits: Money;               // Customer deposits
  centralBankBorrowings: Money;  // Borrowed from central bank

  // Capital
  equity: Money;                 // Bank's own capital

  // Regulatory ratios
  reserveRatio: Percentage;      // Reserves / Deposits
  capitalRatio: Percentage;      // Equity / Assets

  // Credit conditions (Dalio's key variable)
  lendingStandards: LendingStandards;
  creditAvailability: Percentage;  // 0 = no credit, 1 = freely available

  // Risk metrics
  nonPerformingLoansRatio: Percentage;
}

/**
 * Create a new bank
 */
export function createBank(
  id: EntityId,
  name: string,
  initialDeposits: Money,
  initialReserves: Money
): Bank {
  const equity = initialDeposits * 0.1;  // 10% capital ratio

  return {
    id,
    type: 'bank',
    name,
    loans: [],
    reserves: initialReserves,
    securities: initialDeposits * 0.2,
    deposits: initialDeposits,
    centralBankBorrowings: 0,
    equity,
    reserveRatio: initialReserves / initialDeposits,
    capitalRatio: 0.1,
    lendingStandards: 'normal',
    creditAvailability: 0.7,
    nonPerformingLoansRatio: 0.02
  };
}

/**
 * Get total bank assets
 */
export function getBankAssets(bank: Bank): Money {
  const loanValue = bank.loans
    .filter(l => l.status === 'active')
    .reduce((sum, l) => sum + l.remainingPrincipal, 0);

  return loanValue + bank.reserves + bank.securities;
}

/**
 * Can the bank extend more credit?
 * Based on reserves, capital, and lending standards
 */
export function canExtendCredit(bank: Bank, amount: Money): boolean {
  const assets = getBankAssets(bank);
  const activeLoans = bank.loans
    .filter(l => l.status === 'active')
    .reduce((sum, l) => sum + l.remainingPrincipal, 0);

  // Capital constraint
  const newCapitalRatio = bank.equity / (assets + amount);
  if (newCapitalRatio < 0.08) return false;  // Minimum 8% capital

  // Reserve constraint
  const requiredReserves = bank.deposits * 0.1;  // 10% reserve requirement
  if (bank.reserves < requiredReserves) return false;

  // Lending standards constraint
  const lendingMultiplier = bank.lendingStandards === 'loose' ? 12
    : bank.lendingStandards === 'normal' ? 10
    : 8;

  if (activeLoans + amount > bank.equity * lendingMultiplier) return false;

  return true;
}

/**
 * Evaluate a loan application
 * Banks look at creditworthiness (income + collateral)
 */
export function evaluateLoanApplication(
  bank: Bank,
  borrowerCreditworthiness: Creditworthiness,
  requestedAmount: Money,
  purpose: string
): { approved: boolean; interestRate: Percentage; reason: string } {
  // Minimum creditworthiness based on lending standards
  const minScore = bank.lendingStandards === 'loose' ? 0.4
    : bank.lendingStandards === 'normal' ? 0.6
    : 0.8;

  if (borrowerCreditworthiness.overallScore < minScore) {
    return {
      approved: false,
      interestRate: 0,
      reason: 'Insufficient creditworthiness'
    };
  }

  if (requestedAmount > borrowerCreditworthiness.maxBorrowingCapacity) {
    return {
      approved: false,
      interestRate: 0,
      reason: 'Amount exceeds borrowing capacity'
    };
  }

  if (!canExtendCredit(bank, requestedAmount)) {
    return {
      approved: false,
      interestRate: 0,
      reason: 'Bank lending capacity exhausted'
    };
  }

  // Calculate interest rate based on risk
  const baseRate = 0.05;  // 5% base
  const riskPremium = (1 - borrowerCreditworthiness.overallScore) * 0.1;

  return {
    approved: true,
    interestRate: baseRate + riskPremium,
    reason: 'Approved'
  };
}

/**
 * Update bank's lending standards based on economic conditions
 * Dalio: Credit availability is key driver of cycles
 */
export function updateLendingStandards(
  bank: Bank,
  defaultRate: Percentage,
  economicGrowth: Percentage,
  centralBankRate: Percentage
): void {
  // Tighten when defaults rise or growth slows
  if (defaultRate > 0.05 || economicGrowth < -0.02) {
    bank.lendingStandards = 'tight';
    bank.creditAvailability = 0.4;
  }
  // Loosen when conditions are good
  else if (defaultRate < 0.02 && economicGrowth > 0.03 && centralBankRate < 0.03) {
    bank.lendingStandards = 'loose';
    bank.creditAvailability = 0.9;
  }
  // Normal otherwise
  else {
    bank.lendingStandards = 'normal';
    bank.creditAvailability = 0.7;
  }
}

/**
 * Process loan defaults
 * Dalio: "One person's debt is another's asset" - defaults destroy bank assets
 */
export function processDefaults(bank: Bank): Money {
  let totalDefaults = 0;

  bank.loans.forEach(loan => {
    if (loan.status === 'active') {
      // Simple default probability based on debt service ratio
      const defaultProbability = Math.min(0.1,
        loan.remainingPrincipal / loan.borrowerIncomeAtOrigination / 10);

      if (Math.random() < defaultProbability) {
        loan.status = 'defaulted';
        // Recover some from collateral
        const recovery = Math.min(loan.collateralValue, loan.remainingPrincipal) * 0.6;
        const loss = loan.remainingPrincipal - recovery;
        totalDefaults += loss;

        // Loss hits bank equity
        bank.equity -= loss;
      }
    }
  });

  // Update NPL ratio
  const activeLoans = bank.loans.filter(l => l.status === 'active');
  const defaultedLoans = bank.loans.filter(l => l.status === 'defaulted');
  const totalLoanValue = [...activeLoans, ...defaultedLoans]
    .reduce((sum, l) => sum + l.remainingPrincipal, 0);

  bank.nonPerformingLoansRatio = totalLoanValue > 0
    ? defaultedLoans.reduce((sum, l) => sum + l.remainingPrincipal, 0) / totalLoanValue
    : 0;

  return totalDefaults;
}
