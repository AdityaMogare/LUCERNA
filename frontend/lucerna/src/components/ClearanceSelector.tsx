import type { ClearanceLevel } from "../types/dashboard";

const LABELS: Record<ClearanceLevel, string> = {
  unclassified: "Unclassified",
  confidential: "Confidential",
  secret: "Secret",
  top_secret: "Top Secret",
};

interface ClearanceSelectorProps {
  value: ClearanceLevel;
  onChange: (c: ClearanceLevel) => void;
}

export function ClearanceSelector({ value, onChange }: ClearanceSelectorProps) {
  return (
    <div className="clearance-selector">
      <span className="clearance-selector__label">Session clearance (demo)</span>
      <div className="clearance-selector__chips" role="group" aria-label="Clearance level">
        {(Object.keys(LABELS) as ClearanceLevel[]).map((level) => (
          <button
            key={level}
            type="button"
            className={`chip ${value === level ? "chip--active" : ""}`}
            onClick={() => onChange(level)}
          >
            {LABELS[level]}
          </button>
        ))}
      </div>
    </div>
  );
}
