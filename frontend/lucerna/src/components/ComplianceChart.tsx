import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { ComplianceSlice } from "../types/dashboard";

const BAR_COLORS = ["#38bdf8", "#22d3ee", "#a78bfa", "#34d399", "#fbbf24"];

interface ComplianceChartProps {
  data: ComplianceSlice[];
}

export function ComplianceChart({ data }: ComplianceChartProps) {
  return (
    <div className="panel">
      <div className="panel__header">
        <h2 className="panel__title">Compliance by category</h2>
        <p className="panel__subtitle">Weighted to your visible portfolio</p>
      </div>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={data} layout="vertical" margin={{ top: 8, right: 24, left: 8, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" horizontal={false} />
            <XAxis type="number" domain={[0, 100]} hide />
            <YAxis
              type="category"
              dataKey="category"
              width={120}
              tick={{ fill: "var(--muted)", fontSize: 12 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                background: "var(--surface-elevated)",
                border: "1px solid var(--border)",
                borderRadius: "8px",
                color: "var(--text)",
              }}
              formatter={(v: number) => [`${v}%`, "Compliance"]}
            />
            <Bar dataKey="ratePct" radius={[0, 6, 6, 0]} maxBarSize={22}>
              {data.map((_, i) => (
                <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
