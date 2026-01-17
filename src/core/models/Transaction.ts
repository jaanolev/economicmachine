/**
 * Transaction Model
 *
 * Dalio's fundamental insight: "An economy is simply the sum of all transactions."
 *
 * A transaction occurs when a buyer exchanges MONEY or CREDIT with a seller
 * for goods, services, or financial assets.
 *
 * Key equation: Total Spending = Money + Credit
 */

import { EntityId, Money, TimeStep, AssetType } from '../types';

export interface Transaction {
  id: string;
  timestamp: TimeStep;

  // Participants
  buyerId: EntityId;
  sellerId: EntityId;

  // Dalio's key equation: Spending = Money + Credit
  moneyAmount: Money;
  creditAmount: Money;

  // What was exchanged
  assetType: AssetType;
  quantity: number;
  pricePerUnit: Money;
}

export interface TransactionSummary {
  // Dalio: Total Spending = Money + Credit
  totalSpending: Money;
  spendingFromMoney: Money;
  spendingFromCredit: Money;

  // Credit as percentage of spending (key indicator)
  creditPercentage: number;

  transactionCount: number;
}

/**
 * Create a new transaction
 */
export function createTransaction(
  buyerId: EntityId,
  sellerId: EntityId,
  moneyAmount: Money,
  creditAmount: Money,
  assetType: AssetType,
  quantity: number,
  pricePerUnit: Money,
  timestamp: TimeStep
): Transaction {
  return {
    id: `tx-${timestamp}-${Math.random().toString(36).substr(2, 9)}`,
    timestamp,
    buyerId,
    sellerId,
    moneyAmount,
    creditAmount,
    assetType,
    quantity,
    pricePerUnit
  };
}

/**
 * Calculate total spending from a transaction
 * Dalio: Spending = Money + Credit
 */
export function getTransactionSpending(tx: Transaction): Money {
  return tx.moneyAmount + tx.creditAmount;
}

/**
 * Summarize multiple transactions
 */
export function summarizeTransactions(transactions: Transaction[]): TransactionSummary {
  const summary = transactions.reduce(
    (acc, tx) => ({
      totalSpending: acc.totalSpending + tx.moneyAmount + tx.creditAmount,
      spendingFromMoney: acc.spendingFromMoney + tx.moneyAmount,
      spendingFromCredit: acc.spendingFromCredit + tx.creditAmount,
      transactionCount: acc.transactionCount + 1
    }),
    { totalSpending: 0, spendingFromMoney: 0, spendingFromCredit: 0, transactionCount: 0 }
  );

  return {
    ...summary,
    creditPercentage: summary.totalSpending > 0
      ? summary.spendingFromCredit / summary.totalSpending
      : 0
  };
}
