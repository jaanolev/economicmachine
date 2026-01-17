/**
 * Simulation Store
 *
 * Zustand store for managing simulation state and UI synchronization.
 */

import { create } from 'zustand';
import { SimulationEngine, SimulationSpeed } from '../engine/SimulationEngine';
import { EconomicState } from '../core/models/EconomicState';
import { SimulationConfig, DEFAULT_CONFIG } from '../engine/WorldState';

interface SimulationStore {
  // Engine instance
  engine: SimulationEngine | null;

  // Current state (for React reactivity)
  economicState: EconomicState | null;
  history: EconomicState[];

  // UI state
  isRunning: boolean;
  speed: SimulationSpeed;

  // Selected metrics for display
  selectedMetrics: string[];

  // Actions
  initialize: (config?: Partial<SimulationConfig>) => void;
  start: () => void;
  pause: () => void;
  reset: () => void;
  setSpeed: (speed: SimulationSpeed) => void;
  tick: () => void;
  runYears: (years: number) => void;

  // Interventions
  setInterestRate: (rate: number) => void;
  triggerQE: (amount: number) => void;
  setDeleveragingLevers: (levers: {
    austerity?: number;
    debtRestructuring?: number;
    wealthTransfer?: number;
    moneyPrinting?: number;
  }) => void;

  // UI
  setSelectedMetrics: (metrics: string[]) => void;
}

export const useSimulationStore = create<SimulationStore>((set, get) => ({
  engine: null,
  economicState: null,
  history: [],
  isRunning: false,
  speed: 'paused',
  selectedMetrics: ['gdp', 'debt', 'inflation', 'unemployment'],

  initialize: (config = {}) => {
    const engine = new SimulationEngine({ ...DEFAULT_CONFIG, ...config });

    // Subscribe to tick events
    engine.subscribe({
      onTick: (state) => {
        set({
          economicState: state,
          history: engine.getHistory(),
          isRunning: engine.isSimulationRunning()
        });
      },
      onPhaseChange: (cycleType, oldPhase, newPhase) => {
        console.log(`${cycleType} cycle: ${oldPhase} → ${newPhase}`);
      },
      onDeleveragingStart: () => {
        console.log('DELEVERAGING STARTED');
      },
      onDeleveragingEnd: () => {
        console.log('DELEVERAGING ENDED');
      }
    });

    set({
      engine,
      economicState: engine.getEconomicState(),
      history: engine.getHistory()
    });
  },

  start: () => {
    const { engine } = get();
    if (engine) {
      engine.start();
      set({ isRunning: true, speed: engine.getSpeed() });
    }
  },

  pause: () => {
    const { engine } = get();
    if (engine) {
      engine.pause();
      set({ isRunning: false, speed: 'paused' });
    }
  },

  reset: () => {
    const { engine } = get();
    if (engine) {
      engine.reset();
      set({
        economicState: engine.getEconomicState(),
        history: engine.getHistory(),
        isRunning: false,
        speed: 'paused'
      });
    }
  },

  setSpeed: (speed) => {
    const { engine } = get();
    if (engine) {
      engine.setSpeed(speed);
      set({ speed, isRunning: speed !== 'paused' });
    }
  },

  tick: () => {
    const { engine } = get();
    if (engine) {
      engine.tick();
      set({
        economicState: engine.getEconomicState(),
        history: engine.getHistory()
      });
    }
  },

  runYears: (years) => {
    const { engine } = get();
    if (engine) {
      engine.runYears(years);
      set({
        economicState: engine.getEconomicState(),
        history: engine.getHistory()
      });
    }
  },

  setInterestRate: (rate) => {
    const { engine } = get();
    if (engine) {
      engine.setInterestRate(rate);
      set({ economicState: engine.getEconomicState() });
    }
  },

  triggerQE: (amount) => {
    const { engine } = get();
    if (engine) {
      engine.triggerQE(amount);
      set({ economicState: engine.getEconomicState() });
    }
  },

  setDeleveragingLevers: (levers) => {
    const { engine } = get();
    if (engine) {
      engine.setDeleveragingLevers(levers);
      set({ economicState: engine.getEconomicState() });
    }
  },

  setSelectedMetrics: (metrics) => {
    set({ selectedMetrics: metrics });
  }
}));
