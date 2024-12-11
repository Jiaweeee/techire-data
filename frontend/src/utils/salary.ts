import { SalaryRange } from '../types/api';
import { getSalaryPeriodLabel } from '../types/salary';

export function formatSalary(salaryRange: SalaryRange | null): string {
  if (!salaryRange) return 'Unknown';
  
  const { min, max, fixed, currency = 'USD', period } = salaryRange;
  const periodLabel = getSalaryPeriodLabel(period || null);
  
  if (fixed) return `${currency} ${fixed.toLocaleString()}${periodLabel}`;
  if (min && max) return `${currency} ${min.toLocaleString()} - ${max.toLocaleString()}${periodLabel}`;
  if (min) return `${currency} ${min.toLocaleString()}+${periodLabel}`;
  if (max) return `Up to ${currency} ${max.toLocaleString()}${periodLabel}`;
  return 'Unknown';
} 