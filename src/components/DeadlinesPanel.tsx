import type { ClearanceLevel, UpcomingDeadline } from "../types/dashboard";

function clearanceLabel(c: ClearanceLevel): string {
  return c.replace("_", " ").replace(/\b\w/g, (x) => x.toUpperCase());
}

interface DeadlinesPanelProps {
  items: UpcomingDeadline[];
}

export function DeadlinesPanel({ items }: DeadlinesPanelProps) {
  return (
    <div className="panel">
      <div className="panel__header">
        <h2 className="panel__title">Upcoming deadlines</h2>
        <p className="panel__subtitle">Filtered by RLS / clearance (simulated)</p>
      </div>
      <ul className="deadline-list">
        {items.length === 0 ? (
          <li className="deadline-list__empty">No deadlines in your visible set.</li>
        ) : (
          items.map((d) => (
            <li key={d.id} className="deadline-item">
              <div className="deadline-item__main">
                <span className="deadline-item__days">
                  {d.daysRemaining === 0
                    ? "Today"
                    : d.daysRemaining === 1
                      ? "1 day"
                      : `${d.daysRemaining} days`}
                </span>
                <div>
                  <p className="deadline-item__title">{d.title}</p>
                  <p className="deadline-item__meta">
                    <span className="mono">{d.contractId}</span>
                    <span className="dot" aria-hidden />
                    Due {d.dueDate}
                  </p>
                </div>
              </div>
              <span className="clearance-badge clearance-badge--sm">
                {clearanceLabel(d.clearanceRequired)}
              </span>
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
