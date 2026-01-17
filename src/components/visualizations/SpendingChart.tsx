/**
 * Spending Composition Chart
 *
 * Dalio's key insight: Total Spending = Money + Credit
 *
 * This chart shows the composition of spending over time,
 * highlighting how much comes from actual money vs credit.
 */

import React, { useMemo } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { EconomicState } from '../../core/models/EconomicState';

interface SpendingChartProps {
  history: EconomicState[];
}

export const SpendingChart: React.FC<SpendingChartProps> = ({ history }) => {
  const data = useMemo(() => {
    return history.map((state) => ({
      year: state.year + (state.month - 1) / 12,
      money: state.spendingFromMoney,
      credit: state.spendingFromCredit,
      total: state.totalSpending,
      creditPercent: (state.creditAsPercentOfSpending * 100).toFixed(0)
    }));
  }, [history]);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-slate-800 p-3 rounded shadow-lg border border-slate-600">
          <p className="text-white font-bold">Year: {data.year.toFixed(1)}</p>
          <p className="text-emerald-400">Money: {(data.money / 1000).toFixed(1)}k</p>
          <p className="text-purple-400">Credit: {(data.credit / 1000).toFixed(1)}k</p>
          <p className="text-slate-300">Total: {(data.total / 1000).toFixed(1)}k</p>
          <p className="text-yellow-400">Credit: {data.creditPercent}% of spending</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />

          <XAxis
            dataKey="year"
            tick={{ fill: '#9CA3AF', fontSize: 12 }}
            tickFormatter={(value) => Math.floor(value).toString()}
            interval="preserveStartEnd"
          />

          <YAxis
            tick={{ fill: '#9CA3AF', fontSize: 12 }}
            tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
          />

          <Tooltip content={<CustomTooltip />} />

          <Legend />

          {/* Money spending - base layer */}
          <Area
            type="monotone"
            dataKey="money"
            stackId="1"
            stroke="#10B981"
            fill="#10B981"
            fillOpacity={0.6}
            name="Money"
          />

          {/* Credit spending - stacked on top */}
          <Area
            type="monotone"
            dataKey="credit"
            stackId="1"
            stroke="#8B5CF6"
            fill="#8B5CF6"
            fillOpacity={0.6}
            name="Credit"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
