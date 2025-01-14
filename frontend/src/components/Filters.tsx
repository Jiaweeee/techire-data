import { useState, useEffect, useRef } from "react";
import { Search } from "lucide-react";
import { SearchParams, CompanyBrief } from "../types/api";
import { getEmploymentTypeLabel } from "../types/employment";
import { getExperienceLevelLabel } from "../types/experience";
import { getCompanies, getLocations } from "../services/api";
import { useDebounce } from "../hooks/useDebounce";
import { SalarySlider } from "./SalarySlider";

export interface FilterTag {
  id: string;
  label: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  value: any;
  type: "company" | "employment" | "experience" | "location";
}

interface FiltersProps {
  params: SearchParams;
  onFilterChange: (params: Partial<SearchParams>) => void;
  onTagsChange: (tags: FilterTag[]) => void;
}

// Company Filter Component
interface CompanyFilterProps {
  params: SearchParams;
  onFilterChange: (params: Partial<SearchParams>) => void;
  companies: CompanyBrief[]; // Add companies prop
}

function CompanyFilter({
  params,
  onFilterChange,
  companies,
}: CompanyFilterProps) {
  const [companySearch, setCompanySearch] = useState("");
  const [filteredCompanies, setFilteredCompanies] = useState<CompanyBrief[]>(
    []
  );
  const [isOpen, setIsOpen] = useState(false);
  const debouncedSearch = useDebounce(companySearch, 300);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (debouncedSearch) {
      const filtered = companies.filter((company) =>
        company.name.toLowerCase().includes(debouncedSearch.toLowerCase())
      );
      setFilteredCompanies(filtered);
    } else {
      setFilteredCompanies(companies);
    }
  }, [debouncedSearch, companies]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="border-t border-gray-200 pt-4">
      <h3 className="font-semibold text-gray-900 mb-2">Companies</h3>
      <div className="space-y-2">
        <div className="relative" ref={dropdownRef}>
          <input
            type="text"
            value={companySearch}
            onChange={(e) => setCompanySearch(e.target.value)}
            onFocus={() => setIsOpen(true)}
            placeholder="Search companies..."
            className="w-full px-3 py-2 border rounded-lg text-sm"
          />
          <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />

          {isOpen && filteredCompanies.length > 0 && (
            <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
              {filteredCompanies.map((company) => (
                <div
                  key={company.id}
                  className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-2"
                  onClick={() => {
                    if (!params.company_ids?.includes(company.id)) {
                      const newCompanyIds = [
                        ...(params.company_ids || []),
                        company.id,
                      ];
                      onFilterChange({ company_ids: newCompanyIds });
                    }
                    setIsOpen(false);
                  }}
                >
                  <img
                    src={company.icon_url}
                    alt={`${company.name} logo`}
                    className="w-4 h-4 object-cover"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src =
                        "/default-company-icon.png";
                    }}
                  />
                  <span className="text-sm text-gray-700">{company.name}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Location Filter Component
function LocationFilter({
  params,
  onFilterChange,
}: {
  params: SearchParams;
  onFilterChange: (params: Partial<SearchParams>) => void;
}) {
  const [search, setSearch] = useState("");
  const [locations, setLocations] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function fetchLocations() {
      try {
        const data = await getLocations();
        setLocations(data.sort((a, b) => a.localeCompare(b)));
      } catch (error) {
        console.error("Failed to fetch locations:", error);
        setLocations([]);
      }
    }
    fetchLocations();
  }, []);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const filteredLocations = locations.filter((location) =>
    location.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="border-t border-gray-200 pt-4">
      <h3 className="font-semibold text-gray-900 mb-2">Locations</h3>
      <div className="space-y-2">
        <div className="relative" ref={dropdownRef}>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onFocus={() => setIsOpen(true)}
            placeholder="Search locations..."
            className="w-full px-3 py-2 border rounded-lg text-sm"
          />
          <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />

          {isOpen && filteredLocations.length > 0 && (
            <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
              {filteredLocations.map((location) => (
                <div
                  key={location}
                  className="px-4 py-2 hover:bg-gray-100 cursor-pointer text-sm text-gray-700"
                  onClick={() => {
                    if (!params.locations?.includes(location)) {
                      const newLocations = [
                        ...(params.locations || []),
                        location,
                      ];
                      onFilterChange({ locations: newLocations });
                    }
                    setIsOpen(false);
                  }}
                >
                  {location}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Employment Type Filter Component
function EmploymentTypeFilter({
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

// Experience Level Filter Component
function ExperienceLevelFilter({
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

// Salary Filter Component
function SalaryFilter({
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

export function Filters({
  params,
  onFilterChange,
  onTagsChange,
}: FiltersProps) {
  const [allCompanies, setAllCompanies] = useState<CompanyBrief[]>([]);

  useEffect(() => {
    async function fetchCompanies() {
      try {
        const data = await getCompanies();
        setAllCompanies(data);
      } catch (error) {
        console.error("Failed to fetch companies:", error);
        setAllCompanies([]);
      }
    }
    fetchCompanies();
  }, []);

  useEffect(() => {
    const tags: FilterTag[] = [
      ...(params.company_ids?.map((id) => {
        const company = allCompanies.find((c) => c.id === id);
        return {
          id: `company-${id}`,
          label: company?.name || `Company ${id}`,
          value: id,
          type: "company" as const,
        };
      }) || []),
      ...(params.employment_types?.map((type) => ({
        id: `employment-${type}`,
        label: getEmploymentTypeLabel(type),
        value: type,
        type: "employment",
      })) || []),
      ...(params.experience_levels?.map((level) => ({
        id: `experience-${level}`,
        label: getExperienceLevelLabel(level),
        value: level,
        type: "experience",
      })) || []),
      ...(params.locations?.map((location) => ({
        id: `location-${location}`,
        label: location,
        value: location,
        type: "location",
      })) || []),
    ];

    onTagsChange(tags);
  }, [params, onTagsChange, allCompanies]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <span className="font-medium text-gray-900">Filter by</span>
      </div>

      <CompanyFilter
        params={params}
        onFilterChange={onFilterChange}
        companies={allCompanies}
      />
      <LocationFilter params={params} onFilterChange={onFilterChange} />
      <EmploymentTypeFilter params={params} onFilterChange={onFilterChange} />
      <ExperienceLevelFilter params={params} onFilterChange={onFilterChange} />
      <SalaryFilter params={params} onFilterChange={onFilterChange} />
    </div>
  );
}
