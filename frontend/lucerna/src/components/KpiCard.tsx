import type { ReactNode } from "react";

interface KpiCardProps {
  label: string;
  value: string;
  hint?: string;
  icon?: ReactNode;
  variant?: "default" | "warning";
}

export function KpiCard({ label, value, hint, icon, variant = "default" }: KpiCardProps) {
  return (
    <article
      className={`kpi-card ${variant === "warning" ? "kpi-card--warning" : ""}`}
      aria-label={label}
    >
      <div className="kpi-card__top">
        {icon ? <span className="kpi-card__icon">{icon}</span> : null}
        <span className="kpi-card__label">{label}</span>
      </div>
      <p className="kpi-card__value">{value}</p>
      {hint ? <p className="kpi-card__hint">{hint}</p> : null}
    </article>
  );
}
