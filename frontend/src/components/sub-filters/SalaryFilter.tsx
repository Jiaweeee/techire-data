import { SearchParams } from "../../types/api";
import { SalarySlider } from "../SalarySlider";

// Salary Filter Component
export function SalaryFilter({
  params,
  onFilterChange,
}: {
  params: SearchParams;
  onFilterChange: (params: Partial<SearchParams>) => void;
}) {
  return (
    <div className="border-t border-gray-200 pt-4">
      <h3 className="font-semibold text-gray-900 mb-2">Salary</h3>
      <div className="px-2">
        <SalarySlider
          value={params.min_annual_salary || 0}
          onChange={(value) => onFilterChange({ min_annual_salary: value })}
        />
      </div>
    </div>
  );
}