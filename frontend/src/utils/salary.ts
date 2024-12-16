import { SalaryRange } from '../types/api';
import { getSalaryPeriodLabel } from '../types/salary';

function formatNumber(num: number): string {
  if (num >= 1000) {
    return (num / 1000).toLocaleString(undefined, { 
      maximumFractionDigits: 1,
      minimumFractionDigits: 0 
    }) + 'K';
  }
  return num.toLocaleString();
}

export function formatSalary(salaryRange: SalaryRange | null): string {
  if (!salaryRange) return 'Unknown';
  
  const { min, max, fixed, currency = 'USD', period } = salaryRange;
  const periodLabel = getSalaryPeriodLabel(period || null);
  
  if (fixed) return `${currency} ${formatNumber(fixed)}${periodLabel}`;
  if (min && max) return `${currency} ${formatNumber(min)} - ${formatNumber(max)}${periodLabel}`;
  if (min) return `${currency} ${formatNumber(min)}+${periodLabel}`;
  if (max) return `Up to ${currency} ${formatNumber(max)}${periodLabel}`;
  return 'Unknown';
} 