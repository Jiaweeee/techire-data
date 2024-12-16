import { DollarSign, HelpCircle } from 'lucide-react';
import { SalaryRange } from '../types/api';
import { formatSalary } from '../utils/salary';

interface SalaryDisplayProps {
  salaryRange: SalaryRange | null;
  className?: string;
}

export function SalaryDisplay({ salaryRange, className = '' }: SalaryDisplayProps) {
  if (!salaryRange) return null;

  return (
    <span className={`flex items-center gap-1.5 group relative ${className}`}>
      <DollarSign className="w-4 h-4 flex-shrink-0" />
      <span className="truncate">{formatSalary(salaryRange)}</span>
      {salaryRange.is_estimated && (
        <div className="relative inline-block">
          <HelpCircle className="w-4 h-4 text-gray-400" />
          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 w-48 text-center">
            This salary is an estimate based on similar positions and may not reflect the actual compensation.
            <div className="absolute top-full left-1/2 transform -translate-x-1/2 -mt-1">
              <div className="border-8 border-transparent border-t-gray-900"></div>
            </div>
          </div>
        </div>
      )}
    </span>
  );
} 