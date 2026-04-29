export type ClearanceLevel = "unclassified" | "confidential" | "secret" | "top_secret";

export interface KpiSnapshot {
  totalContractValueUsd: number;
  complianceRatePct: number;
  contractorPerformanceScore: number;
  upcomingDeadlinesCount: number;
  atRiskFundsUsd: number;
}

export interface TrendPoint {
  period: string;
  obligatedUsd: number;
}

export interface ComplianceSlice {
  category: string;
  ratePct: number;
}

export interface FlaggedContract {
  id: string;
  title: string;
  vendor: string;
  valueUsd: number;
  risk: "high" | "medium" | "low";
  reason: string;
  clearanceRequired: ClearanceLevel;
}

export interface UpcomingDeadline {
  id: string;
  contractId: string;
  title: string;
  dueDate: string;
  daysRemaining: number;
  clearanceRequired: ClearanceLevel;
}
