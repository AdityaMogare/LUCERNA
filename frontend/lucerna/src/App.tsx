import { useMemo, useState } from "react";
import { ClearanceSelector } from "./components/ClearanceSelector";
import { ComplianceChart } from "./components/ComplianceChart";
import { DeadlinesPanel } from "./components/DeadlinesPanel";
import { FlaggedContractsTable } from "./components/FlaggedContractsTable";
import { KpiCard } from "./components/KpiCard";
import { SpendTrendChart } from "./components/SpendTrendChart";
import {
  mockComplianceByCategory,
  mockDeadlines,
  mockFlaggedContracts,
  mockKpis,
  mockSpendTrend,
  userCanSee,
} from "./data/mockDashboard";
import type { ClearanceLevel } from "./types/dashboard";
import "./App.css";

function formatMoney(n: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(n);
}

export default function App() {
  const [clearance, setClearance] = useState<ClearanceLevel>("secret");

  const visibleContracts = useMemo(
    () => mockFlaggedContracts.filter((c) => userCanSee(clearance, c.clearanceRequired)),
    [clearance]
  );

  const visibleDeadlines = useMemo(
    () => mockDeadlines.filter((d) => userCanSee(clearance, d.clearanceRequired)),
    [clearance]
  );

  const adjustedKpis = useMemo(() => {
    const visibleValue = visibleContracts.reduce((s, c) => s + c.valueUsd, 0);
    const highRisk = visibleContracts.filter((c) => c.risk === "high").length;
    return {
      ...mockKpis,
      totalContractValueUsd: visibleValue || mockKpis.totalContractValueUsd * 0.15,
      upcomingDeadlinesCount: visibleDeadlines.length,
      atRiskFundsUsd:
        visibleContracts.reduce((s, c) => s + (c.risk === "high" ? c.valueUsd * 0.08 : 0), 0) ||
        mockKpis.atRiskFundsUsd * 0.2,
      contractorPerformanceScore: Math.min(
        10,
        mockKpis.contractorPerformanceScore - (highRisk > 0 ? 0.4 : 0)
      ),
    };
  }, [visibleContracts, visibleDeadlines.length]);

  return (
    <div className="app">
      <header className="header">
        <div className="header__brand">
          <div className="logo-mark" aria-hidden />
          <div>
            <p className="header__product">Lucerna</p>
            <h1 className="header__title">Command dashboard</h1>
          </div>
        </div>
        <div className="header__actions">
          <ClearanceSelector value={clearance} onChange={setClearance} />
        </div>
      </header>

      <p className="banner">
        Demo mode: metrics and rows filter by simulated clearance. Wire to Django + Postgres RLS
        when the gateway is ready.
      </p>

      <section className="kpi-grid" aria-label="Key metrics">
        <KpiCard
          label="Total contract value (visible)"
          value={formatMoney(adjustedKpis.totalContractValueUsd)}
          hint="Scoped portfolio under current clearance"
          icon={<span className="glyph">$</span>}
        />
        <KpiCard
          label="Compliance rate"
          value={`${mockKpis.complianceRatePct.toFixed(1)}%`}
          hint="Organization rollup"
          icon={<span className="glyph">✓</span>}
        />
        <KpiCard
          label="Contractor performance"
          value={`${adjustedKpis.contractorPerformanceScore.toFixed(1)} / 10`}
          hint="Composite score — demo"
          icon={<span className="glyph">★</span>}
        />
        <KpiCard
          label="Upcoming deadlines"
          value={String(adjustedKpis.upcomingDeadlinesCount)}
          hint="Next 45 days in visible set"
          icon={<span className="glyph">⏱</span>}
        />
        <KpiCard
          label="At-risk funds (est.)"
          value={formatMoney(adjustedKpis.atRiskFundsUsd)}
          hint="Stalled / expiry exposure — illustrative"
          variant="warning"
          icon={<span className="glyph">!</span>}
        />
      </section>

      <section className="charts-grid">
        <SpendTrendChart data={mockSpendTrend} />
        <ComplianceChart data={mockComplianceByCategory} />
      </section>

      <section className="lower-grid">
        <FlaggedContractsTable rows={visibleContracts} />
        <DeadlinesPanel items={visibleDeadlines} />
      </section>

      <footer className="footer">
        <p>
          Lucerna MVP dashboard · React · Prepared for DRF + PostgreSQL RLS integration
        </p>
      </footer>
    </div>
  );
}
