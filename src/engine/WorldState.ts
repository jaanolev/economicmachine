/**
 * World State
 *
 * Contains all entities and the aggregate economic state.
 * This is the complete state of the simulated economy.
 */

import { EconomicState, createInitialState } from '../core/models/EconomicState';
import { Household, createHousehold } from '../core/models/actors/Household';
import { Business, createBusiness } from '../core/models/actors/Business';
import { Bank, createBank } from '../core/models/actors/Bank';
import { Government, createGovernment } from '../core/models/actors/Government';
import { CentralBank, createCentralBank } from '../core/models/actors/CentralBank';
import { Transaction } from '../core/models/Transaction';
import { Money } from '../core/types';

export interface WorldState {
  // Aggregate economic metrics
  economy: EconomicState;

  // Actors
  households: Household[];
  businesses: Business[];
  banks: Bank[];
  government: Government;
  centralBank: CentralBank;

  // Transaction history (recent)
  recentTransactions: Transaction[];

  // History for charts
  economicHistory: EconomicState[];
}

export interface SimulationConfig {
  // Initial conditions
  startYear: number;
  initialGDP: Money;
  initialDebtToGDP: number;

  // Population
  numHouseholds: number;
  numBusinesses: number;
  numBanks: number;

  // Cycle parameters (Dalio's model)
  productivityGrowthRate: number;      // ~2-3% annually
  shortTermCyclePeriod: number;        // 5-8 years in months
  longTermCyclePeriod: number;         // 75-100 years

  // Behavioral parameters
  baseInflationTarget: number;
}

export const DEFAULT_CONFIG: SimulationConfig = {
  startYear: 2000,
  initialGDP: 10000,
  initialDebtToGDP: 0.5,

  numHouseholds: 100,
  numBusinesses: 20,
  numBanks: 5,

  productivityGrowthRate: 0.025,    // 2.5% annual
  shortTermCyclePeriod: 72,         // 6 years
  longTermCyclePeriod: 900,         // 75 years

  baseInflationTarget: 0.02         // 2%
};

/**
 * Create initial world state
 */
export function createWorldState(config: SimulationConfig = DEFAULT_CONFIG): WorldState {
  const gdpPerCapita = config.initialGDP / config.numHouseholds;

  // Create households
  const households: Household[] = [];
  for (let i = 0; i < config.numHouseholds; i++) {
    // Some wealth inequality
    const wealthMultiplier = 0.5 + Math.random() * 1.5;
    households.push(createHousehold(
      `household-${i}`,
      `Household ${i}`,
      gdpPerCapita * 0.5 * wealthMultiplier,
      gdpPerCapita * 0.8 * wealthMultiplier
    ));
  }

  // Create businesses
  const businesses: Business[] = [];
  const employeesPerBusiness = config.numHouseholds / config.numBusinesses;
  for (let i = 0; i < config.numBusinesses; i++) {
    businesses.push(createBusiness(
      `business-${i}`,
      `Business ${i}`,
      config.initialGDP / config.numBusinesses * 0.3,
      Math.floor(employeesPerBusiness),
      100  // Base productivity
    ));
  }

  // Create banks
  const banks: Bank[] = [];
  const depositsPerBank = config.initialGDP * 0.8 / config.numBanks;
  for (let i = 0; i < config.numBanks; i++) {
    banks.push(createBank(
      `bank-${i}`,
      `Bank ${i}`,
      depositsPerBank,
      depositsPerBank * 0.1  // 10% reserves
    ));
  }

  // Create government
  const government = createGovernment('government', 'Federal Government', config.initialGDP);

  // Create central bank
  const centralBank = createCentralBank('central-bank', 'Central Bank', config.initialGDP);

  // Initial economic state
  const economy = createInitialState(config.startYear, config.initialGDP);
  economy.debtToGDPRatio = config.initialDebtToGDP;
  economy.totalDebt = config.initialGDP * config.initialDebtToGDP;
  economy.productivityGrowthRate = config.productivityGrowthRate;
  economy.shortTermCycle.cycleLengthMonths = config.shortTermCyclePeriod;

  return {
    economy,
    households,
    businesses,
    banks,
    government,
    centralBank,
    recentTransactions: [],
    economicHistory: [economy]
  };
}

/**
 * Calculate aggregate metrics from all actors
 */
export function updateAggregateMetrics(state: WorldState): void {
  const eco = state.economy;

  // Total household assets and debts
  const householdStats = state.households.reduce((acc, h) => ({
    totalIncome: acc.totalIncome + h.wages + h.investmentIncome,
    totalAssets: acc.totalAssets + h.cash + h.savings + h.financialAssets + h.realAssets,
    totalDebt: acc.totalDebt + h.debts.reduce((sum, d) => sum + d.remainingPrincipal, 0)
  }), { totalIncome: 0, totalAssets: 0, totalDebt: 0 });

  // Total business stats
  const businessStats = state.businesses.reduce((acc, b) => ({
    totalRevenue: acc.totalRevenue + b.revenue,
    totalEmployees: acc.totalEmployees + b.employees,
    totalDebt: acc.totalDebt + b.debts.reduce((sum, d) => sum + d.remainingPrincipal, 0)
  }), { totalRevenue: 0, totalEmployees: 0, totalDebt: 0 });

  // Total bank loans
  const totalBankLoans = state.banks.reduce((sum, b) =>
    sum + b.loans.filter(l => l.status === 'active')
      .reduce((s, l) => s + l.remainingPrincipal, 0), 0);

  // Update economic state
  eco.employment = businessStats.totalEmployees;
  eco.unemployment = Math.max(0, 1 - (businessStats.totalEmployees / state.households.length));

  // Total debt in economy
  eco.totalDebt = householdStats.totalDebt + businessStats.totalDebt + state.government.debt;
  eco.debtToGDPRatio = eco.nominalGDP > 0 ? eco.totalDebt / eco.nominalGDP : 0;

  // Credit metrics
  eco.lendingStandards = state.banks[0]?.lendingStandards || 'normal';
  eco.creditAvailability = state.banks.reduce((sum, b) => sum + b.creditAvailability, 0) / state.banks.length;

  // Central bank metrics
  eco.centralBankRate = state.centralBank.policyRate;
  eco.atZeroLowerBound = state.centralBank.atZeroLowerBound;
}
