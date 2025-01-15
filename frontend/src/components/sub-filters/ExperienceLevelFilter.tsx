import { useState } from "react";
import { SearchParams } from "../../types/api";
import { getExperienceLevelLabel } from "../../types/experience";

// Experience Level Filter Component
export function ExperienceLevelFilter({
  params,
  onFilterChange,
}: {
  params: SearchParams;
  onFilterChange: (params: Partial<SearchParams>) => void;
}) {
  const [showAll, setShowAll] = useState(false);

  return (
    <div className="border-t border-gray-200 pt-4">
      <h3 className="font-semibold text-gray-900 mb-2">Experience Level</h3>
      <div className="space-y-3">
        {(showAll ? [1, 2, 3, 4, 5] : [1, 2, 3]).map((level) => (
          <label
            key={level}
            className="flex items-center gap-2 text-base text-gray-500"
          >
            <input
              type="checkbox"
              checked={params.experience_levels?.includes(level)}
              onChange={(e) => {
                const newLevels = e.target.checked
                  ? [...(params.experience_levels || []), level]
                  : (params.experience_levels || []).filter((l) => l !== level);
                onFilterChange({ experience_levels: newLevels });
              }}
              className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            {getExperienceLevelLabel(level)}
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