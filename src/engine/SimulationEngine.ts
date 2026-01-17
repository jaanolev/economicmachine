/**
 * Simulation Engine
 *
 * The main engine that runs the Dalio Economic Machine simulation.
 * It orchestrates all systems and manages the simulation loop.
 */

import { WorldState, SimulationConfig, createWorldState, updateAggregateMetrics, DEFAULT_CONFIG } from './WorldState';
import { System } from './systems/System';
import { ProductivitySystem } from './systems/ProductivitySystem';
import { ShortTermCycleSystem } from './systems/ShortTermCycleSystem';
import { LongTermCycleSystem } from './systems/LongTermCycleSystem';
import { InflationSystem } from './systems/InflationSystem';
import { EconomicState } from '../core/models/EconomicState';

export type SimulationSpeed = 'paused' | 'slow' | 'normal' | 'fast' | 'max';

export interface SimulationEvents {
  onTick?: (state: EconomicState) => void;
  onPhaseChange?: (cycleType: 'short' | 'long', oldPhase: string, newPhase: string) => void;
  onDeleveragingStart?: () => void;
  onDeleveragingEnd?: () => void;
  onRecession?: () => void;
}

export class SimulationEngine {
  private config: SimulationConfig;
  private state: WorldState;
  private systems: System[];

  private isRunning: boolean = false;
  private speed: SimulationSpeed = 'paused';
  private tickInterval: number | null = null;

  private events: SimulationEvents = {};
  private previousState: EconomicState | null = null;

  constructor(config: Partial<SimulationConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.state = createWorldState(this.config);

    // Initialize systems in order (Dalio's three forces)
    this.systems = [
      new ProductivitySystem(this.config.productivityGrowthRate),
      new ShortTermCycleSystem(this.config.shortTermCyclePeriod),
      new LongTermCycleSystem(this.config.longTermCyclePeriod / 12),  // Convert to years
      new InflationSystem()
    ];
  }

  /**
   * Subscribe to simulation events
   */
  subscribe(events: SimulationEvents): () => void {
    this.events = { ...this.events, ...events };
    return () => {
      // Unsubscribe
      Object.keys(events).forEach(key => {
        delete this.events[key as keyof SimulationEvents];
      });
    };
  }

  /**
   * Start the simulation
   */
  start(): void {
    if (this.isRunning) return;
    this.isRunning = true;
    this.setSpeed(this.speed === 'paused' ? 'normal' : this.speed);
  }

  /**
   * Pause the simulation
   */
  pause(): void {
    this.isRunning = false;
    if (this.tickInterval !== null) {
      clearInterval(this.tickInterval);
      this.tickInterval = null;
    }
    this.speed = 'paused';
  }

  /**
   * Reset to initial state
   */
  reset(): void {
    this.pause();
    this.state = createWorldState(this.config);
    this.previousState = null;
  }

  /**
   * Set simulation speed
   */
  setSpeed(speed: SimulationSpeed): void {
    this.speed = speed;

    if (this.tickInterval !== null) {
      clearInterval(this.tickInterval);
      this.tickInterval = null;
    }

    if (speed === 'paused') {
      this.isRunning = false;
      return;
    }

    const intervalMs = {
      slow: 500,    // 2 ticks/sec
      normal: 100,  // 10 ticks/sec
      fast: 20,     // 50 ticks/sec
      max: 1        // As fast as possible
    }[speed];

    this.tickInterval = window.setInterval(() => this.tick(), intervalMs);
  }

  /**
   * Run a single tick (1 month of simulation)
   */
  tick(): void {
    this.previousState = { ...this.state.economy };

    // Run all systems
    for (const system of this.systems) {
      system.process(this.state, 1);  // 1 month delta
    }

    // Update aggregate metrics
    updateAggregateMetrics(this.state);

    // Advance time
    this.state.economy.timestamp += 1;
    this.state.economy.month += 1;
    if (this.state.economy.month > 12) {
      this.state.economy.month = 1;
      this.state.economy.year += 1;
    }

    // Store in history
    this.state.economicHistory.push({ ...this.state.economy });

    // Keep history manageable (last 50 years)
    if (this.state.economicHistory.length > 600) {
      this.state.economicHistory.shift();
    }

    // Emit events
    this.emitEvents();

    // Notify listeners
    this.events.onTick?.(this.state.economy);
  }

  /**
   * Run multiple ticks at once
   */
  runTicks(count: number): void {
    for (let i = 0; i < count; i++) {
      this.tick();
    }
  }

  /**
   * Run for specified number of years
   */
  runYears(years: number): void {
    this.runTicks(years * 12);
  }

  private emitEvents(): void {
    if (!this.previousState) return;

    const current = this.state.economy;
    const prev = this.previousState;

    // Check for phase changes
    if (current.shortTermCycle.phase !== prev.shortTermCycle.phase) {
      this.events.onPhaseChange?.('short', prev.shortTermCycle.phase, current.shortTermCycle.phase);
    }

    if (current.longTermCycle.phase !== prev.longTermCycle.phase) {
      this.events.onPhaseChange?.('long', prev.longTermCycle.phase, current.longTermCycle.phase);
    }

    // Check for deleveraging
    if (current.deleveraging.isDeleveraging && !prev.deleveraging.isDeleveraging) {
      this.events.onDeleveragingStart?.();
    }

    if (!current.deleveraging.isDeleveraging && prev.deleveraging.isDeleveraging) {
      this.events.onDeleveragingEnd?.();
    }

    // Check for recession
    if (current.shortTermCycle.phase === 'contraction' &&
        prev.shortTermCycle.phase !== 'contraction') {
      this.events.onRecession?.();
    }
  }

  // === Getters ===

  getState(): WorldState {
    return this.state;
  }

  getEconomicState(): EconomicState {
    return this.state.economy;
  }

  getHistory(): EconomicState[] {
    return this.state.economicHistory;
  }

  isSimulationRunning(): boolean {
    return this.isRunning;
  }

  getSpeed(): SimulationSpeed {
    return this.speed;
  }

  getConfig(): SimulationConfig {
    return this.config;
  }

  // === User Interventions ===

  /**
   * Set central bank interest rate
   */
  setInterestRate(rate: number): void {
    this.state.centralBank.policyRate = Math.max(0, Math.min(0.2, rate));
    this.state.centralBank.atZeroLowerBound = rate < 0.005;
    this.state.economy.centralBankRate = rate;
  }

  /**
   * Trigger QE
   */
  triggerQE(amount: number): void {
    this.state.centralBank.qeActive = true;
    this.state.centralBank.qePurchases += amount;
    this.state.centralBank.balanceSheet += amount;
  }

  /**
   * Set government spending level
   */
  setGovernmentSpending(amount: number): void {
    this.state.government.spending = amount;
  }

  /**
   * Set deleveraging lever intensities
   */
  setDeleveragingLevers(levers: {
    austerity?: number;
    debtRestructuring?: number;
    wealthTransfer?: number;
    moneyPrinting?: number;
  }): void {
    const longTermSystem = this.systems.find(s => s.name === 'LongTermCycleSystem') as LongTermCycleSystem;
    if (longTermSystem) {
      longTermSystem.setDeleveragingLevers(this.state, levers);
    }
  }

  /**
   * Get the three forces data for visualization
   */
  getThreeForcesData(): {
    timestamps: number[];
    productivity: number[];
    shortTermCycle: number[];
    longTermCycle: number[];
    actualGDP: number[];
  } {
    const history = this.state.economicHistory;

    return {
      timestamps: history.map(h => h.timestamp),
      productivity: history.map(h => h.potentialGDP),
      shortTermCycle: history.map(h => {
        // Short-term oscillation around productivity
        const position = h.shortTermCycle.positionInCycle;
        const amplitude = 0.03;
        return h.potentialGDP * (1 + amplitude * Math.sin(2 * Math.PI * position));
      }),
      longTermCycle: history.map(h => {
        // Long-term debt effect
        const debtEffect = (h.debtToGDPRatio - 0.5) * 0.1;
        return h.potentialGDP * (1 + debtEffect);
      }),
      actualGDP: history.map(h => h.realGDP)
    };
  }
}
