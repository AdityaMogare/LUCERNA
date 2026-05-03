import type { ClearanceLevel, FlaggedContract } from "../types/dashboard";

function formatMoney(n: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(n);
}

function riskClass(risk: FlaggedContract["risk"]): string {
  if (risk === "high") return "risk-pill risk-pill--high";
  if (risk === "medium") return "risk-pill risk-pill--medium";
  return "risk-pill risk-pill--low";
}

function clearanceLabel(c: ClearanceLevel): string {
  return c.replace("_", " ").replace(/\b\w/g, (x) => x.toUpperCase());
}

interface FlaggedContractsTableProps {
  rows: FlaggedContract[];
}

export function FlaggedContractsTable({ rows }: FlaggedContractsTableProps) {
  return (
    <div className="panel panel--table">
      <div className="panel__header">
        <h2 className="panel__title">AI-flagged contracts</h2>
        <p className="panel__subtitle">Text-to-SQL + policy rules — demo data</p>
      </div>
      <div className="table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              <th>Contract</th>
              <th>Vendor</th>
              <th>Value</th>
              <th>Risk</th>
              <th>Reason</th>
              <th>Min clearance</th>
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 ? (
              <tr>
                <td colSpan={6} className="data-table__empty">
                  No rows visible at this clearance. Raise session level to see compartmented
                  records.
                </td>
              </tr>
            ) : (
              rows.map((r) => (
                <tr key={r.id}>
                  <td>
                    <span className="mono">{r.id}</span>
                    <br />
                    <span className="data-table__title">{r.title}</span>
                  </td>
                  <td>{r.vendor}</td>
                  <td className="tabular">{formatMoney(r.valueUsd)}</td>
                  <td>
                    <span className={riskClass(r.risk)}>{r.risk}</span>
                  </td>
                  <td className="data-table__reason">{r.reason}</td>
                  <td>
                    <span className="clearance-badge">{clearanceLabel(r.clearanceRequired)}</span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
