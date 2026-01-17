/**
 * Core type definitions for the Dalio Economic Machine Simulator
 * Based on Ray Dalio's "How The Economic Machine Works"
 */

// Basic numeric types with semantic meaning
export type Money = number;           // Currency units
export type Percentage = number;      // 0.0 to 1.0 (or higher for >100%)
export type TimeStep = number;        // Simulation tick (1 tick = 1 month)

// Entity identification
export type EntityId = string;
export type EntityType = 'household' | 'business' | 'bank' | 'government' | 'centralBank';

// Base entity interface
export interface Entity {
  id: EntityId;
  type: EntityType;
  name: string;
}

// Cycle phases
export type ShortTermCyclePhase = 'expansion' | 'peak' | 'contraction' | 'trough';
export type LongTermCyclePhase = 'leveraging' | 'peak' | 'deleveraging' | 'reflation';
export type DeleveragingType = 'beautiful' | 'ugly' | null;

// Credit quality (Dalio's good vs bad credit)
export type CreditPurpose = 'productive' | 'consumptive' | 'speculative';
export type CreditStatus = 'active' | 'defaulted' | 'repaid';

// Lending standards
export type LendingStandards = 'loose' | 'normal' | 'tight';

// Fiscal policy stance
export type FiscalStance = 'austerity' | 'neutral' | 'stimulus';

// Asset types for transactions
export type AssetType = 'goods' | 'services' | 'labor' | 'financialAsset' | 'realAsset';
