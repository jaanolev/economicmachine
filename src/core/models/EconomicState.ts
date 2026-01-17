/**
 * Economic State Model
 *
 * This is the aggregate state of the economy at any point in time.
 * It captures all of Dalio's key metrics and the three driving forces.
 */

import {
  Money,
  Percentage,
  TimeStep,
  ShortTermCyclePhase,
  LongTermCyclePhase,
  DeleveragingType,
  LendingStandards
} from '../types';

/**
 * Short-term debt cycle state (5-8 years)
 */
export interface ShortTermCycleState {
  phase: ShortTermCyclePhase;
  positionInCycle: Percentage;  // 0-1
  cycleNumber: number;          // Which cycle we're in
  cycleLengthMonths: number;    // Current cycle length
}

/**
 * Long-term debt cycle state (75-100 years)
 */
export interface LongTermCycleState {
  phase: LongTermCyclePhase;
  yearsIntoCycle: number;
  peakDebtToGDP: Percentage;    // The high water mark
}

/**
 * Deleveraging state
 * Dalio's four levers for reducing debt burden
 */
export interface DeleveragingState {
  isDeleveraging: boolean;
  type: DeleveragingType;
  yearsInDeleveraging: number;

  // The four levers (0-1 intensity)
  levers: {
    austerity: Percentage;        // Spending cuts (deflationary)
    debtRestructuring: Percentage; // Defaults (deflationary)
    wealthTransfer: Percentage;    // Taxes on wealthy (redistributive)
    moneyPrinting: Percentage;     // Monetization (inflationary)
  };

  // Balance of forces
  deflationaryForce: Percentage;
  inflationaryForce: Percentage;
}

/**
 * Complete economic state at a point in time
 */
export interface EconomicState {
  timestamp: TimeStep;
  year: number;
  month: number;

  // === GDP Measures ===
  nominalGDP: Money;
  realGDP: Money;
  potentialGDP: Money;  // Based on productivity trend
  outputGap: Percentage; // (real - potential) / potential

  // === The Three Forces (Dalio's Core Model) ===
  productivityLevel: number;
  productivityGrowthRate: Percentage;

  shortTermCycle: ShortTermCycleState;
  longTermCycle: LongTermCycleState;

  // === Spending Breakdown ===
  // Dalio: Total Spending = Money + Credit
  totalSpending: Money;
  spendingFromMoney: Money;
  spendingFromCredit: Money;
  creditAsPercentOfSpending: Percentage;

  // === Debt Metrics ===
  totalDebt: Money;
  debtToGDPRatio: Percentage;
  debtServiceToIncome: Percentage;  // Critical for deleveraging trigger
  creditGrowth: Percentage;         // Year-over-year

  // === Price Levels ===
  priceLevel: number;
  inflation: Percentage;
  assetPriceInflation: Percentage;

  // === Employment ===
  employment: number;
  unemployment: Percentage;
  wageGrowth: Percentage;

  // === Interest Rates ===
  centralBankRate: Percentage;
  marketRates: {
    shortTerm: Percentage;
    longTerm: Percentage;
    mortgage: Percentage;
    corporate: Percentage;
  };
  atZeroLowerBound: boolean;

  // === Credit Conditions ===
  lendingStandards: LendingStandards;
  creditAvailability: Percentage;

  // === Deleveraging ===
  deleveraging: DeleveragingState;

  // === Dalio's Rules Tracking ===
  rules: {
    debtVsIncomeGrowth: Percentage;      // Should be < 0
    incomeVsProductivityGrowth: Percentage; // Should be ~0
    productivityGrowth: Percentage;       // Should be maximized
  };
}

/**
 * Create initial economic state
 */
export function createInitialState(
  startYear: number = 2000,
  initialGDP: Money = 10000
): EconomicState {
  return {
    timestamp: 0,
    year: startYear,
    month: 1,

    nominalGDP: initialGDP,
    realGDP: initialGDP,
    potentialGDP: initialGDP,
    outputGap: 0,

    productivityLevel: 100,
    productivityGrowthRate: 0.025,  // 2.5% annual

    shortTermCycle: {
      phase: 'expansion',
      positionInCycle: 0.2,
      cycleNumber: 1,
      cycleLengthMonths: 72  // 6 years
    },

    longTermCycle: {
      phase: 'leveraging',
      yearsIntoCycle: 20,
      peakDebtToGDP: 0.6
    },

    totalSpending: initialGDP,
    spendingFromMoney: initialGDP * 0.4,
    spendingFromCredit: initialGDP * 0.6,
    creditAsPercentOfSpending: 0.6,

    totalDebt: initialGDP * 0.6,
    debtToGDPRatio: 0.6,
    debtServiceToIncome: 0.15,
    creditGrowth: 0.05,

    priceLevel: 100,
    inflation: 0.02,
    assetPriceInflation: 0.03,

    employment: 1000,
    unemployment: 0.05,
    wageGrowth: 0.03,

    centralBankRate: 0.03,
    marketRates: {
      shortTerm: 0.035,
      longTerm: 0.045,
      mortgage: 0.05,
      corporate: 0.055
    },
    atZeroLowerBound: false,

    lendingStandards: 'normal',
    creditAvailability: 0.7,

    deleveraging: {
      isDeleveraging: false,
      type: null,
      yearsInDeleveraging: 0,
      levers: {
        austerity: 0,
        debtRestructuring: 0,
        wealthTransfer: 0,
        moneyPrinting: 0
      },
      deflationaryForce: 0,
      inflationaryForce: 0
    },

    rules: {
      debtVsIncomeGrowth: 0,
      incomeVsProductivityGrowth: 0,
      productivityGrowth: 0.025
    }
  };
}

/**
 * Check Dalio's first rule: Is debt rising faster than income?
 */
export function checkDebtRule(state: EconomicState, prevState: EconomicState): boolean {
  const incomeGrowth = (state.nominalGDP - prevState.nominalGDP) / prevState.nominalGDP;
  const debtGrowth = (state.totalDebt - prevState.totalDebt) / prevState.totalDebt;
  return debtGrowth <= incomeGrowth;
}

/**
 * Check Dalio's second rule: Is income rising faster than productivity?
 */
export function checkIncomeProductivityRule(state: EconomicState): boolean {
  const incomeGrowth = state.wageGrowth;
  const productivityGrowth = state.productivityGrowthRate;
  // Small buffer allowed
  return incomeGrowth <= productivityGrowth + 0.01;
}

/**
 * Determine if economy is in recession
 */
export function isRecession(state: EconomicState): boolean {
  return state.outputGap < -0.02 && state.unemployment > 0.07;
}

/**
 * Determine if economy is in depression
 * Dalio: Real GDP decline > 3%
 */
export function isDepression(state: EconomicState, prevYearState: EconomicState): boolean {
  const realGDPChange = (state.realGDP - prevYearState.realGDP) / prevYearState.realGDP;
  return realGDPChange < -0.03;
}

/**
 * Should deleveraging begin?
 * Dalio's conditions:
 * 1. Debt burden too high (debt service > 40% of income)
 * 2. Interest rates at zero (can't stimulate more)
 * 3. Credit growth stalling despite low rates
 */
export function shouldTriggerDeleveraging(state: EconomicState): boolean {
  return (
    state.debtServiceToIncome > 0.35 &&
    state.atZeroLowerBound &&
    state.creditGrowth < 0.02
  );
}

/**
 * Is this a "beautiful" deleveraging?
 * Dalio: Nominal growth > nominal interest rate
 * while debt/income declines
 * and inflation is manageable
 */
export function isBeautifulDeleveraging(
  state: EconomicState,
  prevState: EconomicState
): boolean {
  if (!state.deleveraging.isDeleveraging) return false;

  const nominalGrowth = (state.nominalGDP - prevState.nominalGDP) / prevState.nominalGDP * 12; // Annualized
  const debtToIncomeChange = state.debtToGDPRatio - prevState.debtToGDPRatio;

  return (
    nominalGrowth > state.centralBankRate &&
    debtToIncomeChange < 0 &&
    state.inflation > 0 &&
    state.inflation < 0.05
  );
}
