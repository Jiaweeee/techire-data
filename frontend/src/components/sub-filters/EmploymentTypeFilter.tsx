import { useState } from "react";
import { SearchParams } from "../../types/api";
import { getEmploymentTypeLabel } from "../../types/employment";

// Employment Type Filter Component
export function EmploymentTypeFilter({
  params,
  onFilterChange,
}: {
  params: SearchParams;
  onFilterChange: (params: Partial<SearchParams>) => void;
}) {
  const [showAll, setShowAll] = useState(false);

  return (
    <div className="border-t border-gray-200 pt-4">
      <h3 className="font-semibold text-gray-900 mb-2">Employment Type</h3>
      <div className="space-y-3">
        {(showAll ? [1, 2, 3, 4, 5, 6, 7, 8] : [1, 2, 3]).map((type) => (
          <label
            key={type}
            className="flex items-center gap-2 text-base text-gray-500"
          >
            <input
              type="checkbox"
              checked={params.employment_types?.includes(type)}
              onChange={(e) => {
                const newTypes = e.target.checked
                  ? [...(params.employment_types || []), type]
                  : (params.employment_types || []).filter((t) => t !== type);
                onFilterChange({ employment_types: newTypes });
              }}
              className="w-5 h-5 text-blue-600 border-gray-300 rounded-lg focus:ring-blue-500"
            />
            {getEmploymentTypeLabel(type)}
          </label>
        ))}
        <button
          onClick={() => setShowAll(!showAll)}
          className="text-base text-blue-600 hover:text-blue-800"
        >
          {showAll ? "See less" : "See more"}
        </button>
      </div>
    </div>
  );
}