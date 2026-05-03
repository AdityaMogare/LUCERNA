import type {
  ClearanceLevel,
  ComplianceSlice,
  FlaggedContract,
  KpiSnapshot,
  TrendPoint,
  UpcomingDeadline,
} from "../types/dashboard";

const clearanceOrder: ClearanceLevel[] = [
  "unclassified",
  "confidential",
  "secret",
  "top_secret",
];

export function userCanSee(
  userClearance: ClearanceLevel,
  resourceClearance: ClearanceLevel
): boolean {
  return clearanceOrder.indexOf(userClearance) >= clearanceOrder.indexOf(resourceClearance);
}

export const mockKpis: KpiSnapshot = {
  totalContractValueUsd: 184_200_000,
  complianceRatePct: 94.2,
  contractorPerformanceScore: 7.8,
  upcomingDeadlinesCount: 23,
  atRiskFundsUsd: 12_400_000,
};

export const mockSpendTrend: TrendPoint[] = [
  { period: "Oct", obligatedUsd: 42_000_000 },
  { period: "Nov", obligatedUsd: 48_500_000 },
  { period: "Dec", obligatedUsd: 51_200_000 },
  { period: "Jan", obligatedUsd: 55_800_000 },
  { period: "Feb", obligatedUsd: 61_100_000 },
  { period: "Mar", obligatedUsd: 67_400_000 },
];

export const mockComplianceByCategory: ComplianceSlice[] = [
  { category: "FAR clauses", ratePct: 97 },
  { category: "DFARS", ratePct: 92 },
  { category: "Small business", ratePct: 89 },
  { category: "Cyber (CMMC)", ratePct: 96 },
  { category: "Environmental", ratePct: 91 },
];

export const mockFlaggedContracts: FlaggedContract[] = [
  {
    id: "c-1042",
    title: "Aircraft sustainment — Lot 7",
    vendor: "AeroDyne Systems",
    valueUsd: 22_500_000,
    risk: "high",
    reason: "Option period lapses in 18 days; funds uncommitted.",
    clearanceRequired: "secret",
  },
  {
    id: "c-0891",
    title: "Base IT modernization",
    vendor: "Nexus Federal LLC",
    valueUsd: 8_200_000,
    risk: "medium",
    reason: "Deliverable variance >15% vs. plan; CLIN re-alignment pending.",
    clearanceRequired: "confidential",
  },
  {
    id: "c-1203",
    title: "Range operations support",
    vendor: "Highland Logistics",
    valueUsd: 3_100_000,
    risk: "low",
    reason: "Approaching funding ceiling; modification draft in review.",
    clearanceRequired: "unclassified",
  },
  {
    id: "c-0777",
    title: "Secure communications refresh",
    vendor: "Cipher Ridge Corp",
    valueUsd: 41_000_000,
    risk: "high",
    reason: "CDRL overdue; COR escalation recommended.",
    clearanceRequired: "top_secret",
  },
];

export const mockDeadlines: UpcomingDeadline[] = [
  {
    id: "d-1",
    contractId: "c-1042",
    title: "Option exercise decision",
    dueDate: "2026-05-17",
    daysRemaining: 18,
    clearanceRequired: "secret",
  },
  {
    id: "d-2",
    contractId: "c-0891",
    title: "Monthly progress report",
    dueDate: "2026-05-02",
    daysRemaining: 3,
    clearanceRequired: "confidential",
  },
  {
    id: "d-3",
    contractId: "c-1203",
    title: "Funding realignment package",
    dueDate: "2026-05-28",
    daysRemaining: 29,
    clearanceRequired: "unclassified",
  },
  {
    id: "d-4",
    contractId: "c-0777",
    title: "CDRL A012 submission",
    dueDate: "2026-04-30",
    daysRemaining: 1,
    clearanceRequired: "top_secret",
  },
];
