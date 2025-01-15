import { useState, useEffect } from "react";
import { SearchParams, CompanyBrief } from "../types/api";
import { getEmploymentTypeLabel } from "../types/employment";
import { getExperienceLevelLabel } from "../types/experience";
import { getCompanies } from "../services/api";
import {
    CompanyFilter,
    LocationFilter,
    EmploymentTypeFilter,
    ExperienceLevelFilter,
    SalaryFilter,
  } from "./sub-filters";

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
        type: "employment" as const,
      })) || []),
      ...(params.experience_levels?.map((level) => ({
        id: `experience-${level}`,
        label: getExperienceLevelLabel(level),
        value: level,
        type: "experience" as const,
      })) || []),
      ...(params.locations?.map((location) => ({
        id: `location-${location}`,
        label: location,
        value: location,
        type: "location" as const,
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
