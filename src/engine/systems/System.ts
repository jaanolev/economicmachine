/**
 * Base System Interface
 *
 * Systems are processors that update the world state each tick.
 * They implement Dalio's economic mechanics.
 */

import type { WorldState } from '../WorldState';

export interface System {
  name: string;

  /**
   * Process one tick of simulation
   * @param state The current world state (mutable)
   * @param deltaMonths Time elapsed (usually 1 month)
   */
  process(state: WorldState, deltaMonths: number): void;
}

/**
 * Priority order for system processing
 * Order matters for economic causality
 */
export const SystemPriority = {
  PRODUCTIVITY: 0,       // First: productivity sets the baseline
  CENTRAL_BANK: 1,       // Second: central bank sets interest rates
  CREDIT: 2,             // Third: credit conditions determined
  TRANSACTIONS: 3,       // Fourth: transactions occur
  SHORT_TERM_CYCLE: 4,   // Fifth: short-term cycle updates
  LONG_TERM_CYCLE: 5,    // Sixth: long-term cycle updates
  DELEVERAGING: 6,       // Seventh: deleveraging if active
  INFLATION: 7,          // Last: inflation calculated from all activity
} as const;

export type SystemPriority = typeof SystemPriority[keyof typeof SystemPriority];
