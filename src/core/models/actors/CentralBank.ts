/**
 * Central Bank Actor Model
 *
 * Dalio's framework heavily emphasizes the central bank's role:
 * - MP1: Interest rate policy (primary tool in normal times)
 * - MP2: Quantitative Easing (when rates hit zero)
 * - MP3: Fiscal-monetary coordination (direct funding of spending)
 *
 * The central bank controls credit conditions through interest rates,
 * which is the key driver of short-term debt cycles.
 */

import { Entity, EntityId, Money, Percentage } from '../../types';

export type MonetaryPolicyType = 'MP1' | 'MP2' | 'MP3';

export interface CentralBank extends Entity {
  type: 'centralBank';

  // MP1: Interest Rate Policy
  policyRate: Percentage;         // The key lever
  inflationTarget: Percentage;    // Usually 2%

  // MP2: Quantitative Easing
  balanceSheet: Money;            // Central bank's assets
  qeActive: boolean;
  qePurchases: Money;             // Cumulative QE

  // MP3: Fiscal-Monetary Coordination
  fiscalMonetization: boolean;    // Directly funding government
  monetizedAmount: Money;

  // Reserve requirements
  reserveRequirement: Percentage;

  // State
  atZeroLowerBound: boolean;      // Dalio's critical constraint
  currentPolicy: MonetaryPolicyType;

  // Inflation tracking
  currentInflation: Percentage;
  inflationHistory: Percentage[];
}

/**
 * Create a new central bank
 */
export function createCentralBank(id: EntityId, name: string, gdp: Money): CentralBank {
  return {
    id,
    type: 'centralBank',
    name,
    policyRate: 0.03,           // 3% starting rate
    inflationTarget: 0.02,       // 2% target
    balanceSheet: gdp * 0.2,     // 20% of GDP
    qeActive: false,
    qePurchases: 0,
    fiscalMonetization: false,
    monetizedAmount: 0,
    reserveRequirement: 0.1,     // 10%
    atZeroLowerBound: false,
    currentPolicy: 'MP1',
    currentInflation: 0.02,
    inflationHistory: []
  };
}

/**
 * Taylor Rule for interest rate setting
 * Dalio: Central bank raises rates when inflation rises,
 * lowers rates when economy contracts
 */
export function calculateTaylorRate(
  centralBank: CentralBank,
  outputGap: Percentage  // (actual - potential) / potential
): Percentage {
  const naturalRate = 0.02;  // 2% neutral rate
  const inflationGap = centralBank.currentInflation - centralBank.inflationTarget;

  // Taylor Rule: r = r* + 1.5*(π - π*) + 0.5*(y - y*)
  const targetRate = naturalRate +
    1.5 * inflationGap +
    0.5 * outputGap;

  // Zero lower bound
  return Math.max(0, targetRate);
}

/**
 * Apply MP1: Interest Rate Policy
 * The primary tool in normal times
 */
export function applyMP1(
  centralBank: CentralBank,
  outputGap: Percentage
): void {
  const targetRate = calculateTaylorRate(centralBank, outputGap);

  // Gradually move toward target (25 bps at a time)
  const rateChange = Math.sign(targetRate - centralBank.policyRate) * 0.0025;
  centralBank.policyRate = Math.max(0, centralBank.policyRate + rateChange);

  // Check if we've hit zero lower bound
  centralBank.atZeroLowerBound = centralBank.policyRate < 0.005;

  // If at ZLB and need more stimulus, switch to MP2
  if (centralBank.atZeroLowerBound && outputGap < -0.02) {
    centralBank.currentPolicy = 'MP2';
  }
}

/**
 * Apply MP2: Quantitative Easing
 * Dalio: "When rates hit 0%, central banks print money and buy assets"
 */
export function applyMP2(
  centralBank: CentralBank,
  gdp: Money,
  outputGap: Percentage
): void {
  centralBank.qeActive = true;

  // QE amount based on how far below target
  // Dalio: "Each 1% of rate = roughly 2% of GDP in QE"
  const desiredRate = calculateTaylorRate(centralBank, outputGap);
  const rateShortfall = Math.abs(Math.min(0, desiredRate));

  const qeThisMonth = gdp * rateShortfall * 2 / 12;
  centralBank.qePurchases += qeThisMonth;
  centralBank.balanceSheet += qeThisMonth;

  // MP2 pushes investors into riskier assets
  // This is modeled in the market price effects elsewhere
}

/**
 * Apply MP3: Fiscal-Monetary Coordination
 * Dalio: When MP1 and MP2 are exhausted, coordinate with fiscal policy
 * Central bank directly funds government spending
 */
export function applyMP3(
  centralBank: CentralBank,
  governmentDeficit: Money
): void {
  centralBank.fiscalMonetization = true;
  centralBank.currentPolicy = 'MP3';

  // Print money to fund government deficit
  centralBank.monetizedAmount += governmentDeficit;
  centralBank.balanceSheet += governmentDeficit;

  // This money goes directly into the real economy
  // (Unlike QE which mainly inflates asset prices)
}

/**
 * Determine which monetary policy to use
 * Dalio's framework for policy selection
 */
export function determineMonetaryPolicy(
  centralBank: CentralBank,
  outputGap: Percentage,
  isDeleveraging: boolean,
  creditGrowth: Percentage
): MonetaryPolicyType {
  // Normal times: MP1 (interest rates)
  if (!centralBank.atZeroLowerBound) {
    return 'MP1';
  }

  // At zero bound but economy still weak: MP2 (QE)
  if (centralBank.atZeroLowerBound && outputGap < -0.01) {
    return 'MP2';
  }

  // Deleveraging with credit contraction: MP3 (fiscal coordination)
  if (isDeleveraging && creditGrowth < 0) {
    return 'MP3';
  }

  return centralBank.currentPolicy;
}

/**
 * Calculate effective monetary stimulus
 * Dalio: "The Fed only has room to cut about 2%, which isn't much
 * because past recessions needed about 5% of cuts"
 */
export function calculateEffectiveStimulus(
  centralBank: CentralBank,
  gdp: Money
): Money {
  let stimulus = 0;

  // MP1: Rate cuts translate to credit expansion
  if (centralBank.policyRate < 0.05) {
    const rateCutEffect = (0.05 - centralBank.policyRate) * gdp * 0.5;
    stimulus += rateCutEffect;
  }

  // MP2: QE effect (diminishing returns)
  if (centralBank.qeActive) {
    const qeEffect = centralBank.qePurchases * 0.3;  // QE has ~30% effectiveness
    stimulus += qeEffect;
  }

  // MP3: Direct monetization (most effective at getting money into economy)
  if (centralBank.fiscalMonetization) {
    stimulus += centralBank.monetizedAmount * 0.8;  // 80% effective
  }

  return stimulus;
}

/**
 * Update inflation tracking
 */
export function updateInflation(
  centralBank: CentralBank,
  spendingGrowth: Percentage,
  productivityGrowth: Percentage
): void {
  // Dalio: Inflation = Spending Growth - Productivity Growth
  centralBank.currentInflation = spendingGrowth - productivityGrowth;

  // Track history
  centralBank.inflationHistory.push(centralBank.currentInflation);
  if (centralBank.inflationHistory.length > 120) {  // Keep 10 years
    centralBank.inflationHistory.shift();
  }
}
