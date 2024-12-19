import { useState, useEffect, useRef } from 'react';
import { Search } from 'lucide-react';
import { SearchParams, CompanyBrief } from '../types/api';
import { getEmploymentTypeLabel } from '../types/employment';
import { getExperienceLevelLabel } from '../types/experience';
import { searchCompanies, getCompanies } from '../services/api';
import { useDebounce } from '../hooks/useDebounce';
import { SalarySlider } from './SalarySlider';

export interface FilterTag {
    id: string;
    label: string;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    value: any;
    type: 'company' | 'employment' | 'experience';
}

interface FiltersProps {
  params: SearchParams;
  onFilterChange: (params: Partial<SearchParams>) => void;
  onTagsChange: (tags: FilterTag[]) => void;
}

export function Filters({ params, onFilterChange, onTagsChange }: FiltersProps) {
  const [companySearch, setCompanySearch] = useState('');
  const [companies, setCompanies] = useState<CompanyBrief[]>([]);
  const [showAllEmploymentTypes, setShowAllEmploymentTypes] = useState(false);
  const [showAllExperienceLevels, setShowAllExperienceLevels] = useState(false);
  const [isCompanyListOpen, setIsCompanyListOpen] = useState(false);
  const debouncedSearch = useDebounce(companySearch, 300);
  const companyDropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function fetchCompanies() {
      if (!debouncedSearch && isCompanyListOpen) {
        try {
          const data = await getCompanies();
          setCompanies(data);
        } catch (error) {
          console.error('Failed to fetch companies:', error);
          setCompanies([]);
        }
      } else if (debouncedSearch) {
        try {
          const data = await searchCompanies(debouncedSearch);
          setCompanies(data);
        } catch (error) {
          console.error('Failed to search companies:', error);
          setCompanies([]);
        }
      }
    }
    fetchCompanies();
  }, [debouncedSearch, isCompanyListOpen]);

  useEffect(() => {
    const tags: FilterTag[] = [
      // Company tags
      ...(params.company_ids?.map(id => {
        const company = companies.find(c => c.id === id);
        return {
          id: `company-${id}`,
          label: company?.name || `Company ${id}`,
          value: id,
          type: 'company' as const
        };
      }) || []),
      // Employment type tags
      ...(params.employment_types?.map(type => ({
        id: `employment-${type}`,
        label: getEmploymentTypeLabel(type),
        value: type,
        type: 'employment' as const
      })) || []),
      // Experience level tags
      ...(params.experience_levels?.map(level => ({
        id: `experience-${level}`,
        label: getExperienceLevelLabel(level),
        value: level,
        type: 'experience' as const
      })) || [])
    ];
    
    onTagsChange(tags);
  }, [params, companies, onTagsChange]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (companyDropdownRef.current && !companyDropdownRef.current.contains(event.target as Node)) {
        setIsCompanyListOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="space-y-6">
      {/* Title */}
      <div className="flex justify-between items-center">
        <span className="font-medium text-gray-900">Filter by</span>
      </div>

      {/* Companies Filter */}
      <div className="border-t border-gray-200 pt-4">
        <h3 className="font-semibold text-gray-900 mb-2">Companies</h3>
        <div className="space-y-2">
          <div className="relative" ref={companyDropdownRef}>
            <input
              type="text"
              value={companySearch}
              onChange={(e) => setCompanySearch(e.target.value)}
              onFocus={() => setIsCompanyListOpen(true)}
              placeholder="Search companies..."
              className="w-full px-3 py-2 border rounded-lg text-sm"
            />
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            
            {/* Company List Dropdown */}
            {isCompanyListOpen && companies.length > 0 && (
              <div className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                {companies.map(company => (
                  <div
                    key={company.id}
                    className="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center gap-2"
                    onClick={() => {
                        if (!params.company_ids?.includes(company.id)) {
                            const newCompanyIds = [...(params.company_ids || []), company.id];
                            onFilterChange({ company_ids: newCompanyIds });
                        }
                        setIsCompanyListOpen(false)
                    }}
                  >
                    <img 
                      src={company.icon_url} 
                      alt={`${company.name} logo`}
                      className="w-4 h-4 object-cover"
                      onError={(e) => {
                        (e.target as HTMLImageElement).src = '/default-company-icon.png';
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

      {/* Employment Type Filter */}
      <div className="border-t border-gray-200 pt-4">
        <h3 className="font-semibold text-gray-900 mb-2">Employment Type</h3>
        <div className="space-y-3">
          {(showAllEmploymentTypes ? [1, 2, 3, 4, 5, 6, 7, 8] : [1, 2, 3]).map(type => (
            <label key={type} className="flex items-center gap-2 text-base text-gray-500">
              <input
                type="checkbox"
                checked={params.employment_types?.includes(type)}
                onChange={(e) => {
                  const newTypes = e.target.checked
                    ? [...(params.employment_types || []), type]
                    : (params.employment_types || []).filter(t => t !== type);
                  onFilterChange({ employment_types: newTypes });
                }}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded-lg focus:ring-blue-500"
              />
              {getEmploymentTypeLabel(type)}
            </label>
          ))}
          <button
            onClick={() => setShowAllEmploymentTypes(!showAllEmploymentTypes)}
            className="text-base text-blue-600 hover:text-blue-800"
          >
            {showAllEmploymentTypes ? 'See less' : 'See more'}
          </button>
        </div>
      </div>

      {/* Experience Level Filter */}
      <div className="border-t border-gray-200 pt-4">
        <h3 className="font-semibold text-gray-900 mb-2">Experience Level</h3>
        <div className="space-y-3">
          {(showAllExperienceLevels ? [1, 2, 3, 4, 5] : [1, 2, 3]).map(level => (
            <label key={level} className="flex items-center gap-2 text-base text-gray-500">
              <input
                type="checkbox"
                checked={params.experience_levels?.includes(level)}
                onChange={(e) => {
                  const newLevels = e.target.checked
                    ? [...(params.experience_levels || []), level]
                    : (params.experience_levels || []).filter(l => l !== level);
                  onFilterChange({ experience_levels: newLevels });
                }}
                className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              />
              {getExperienceLevelLabel(level)}
            </label>
          ))}
          <button
            onClick={() => setShowAllExperienceLevels(!showAllExperienceLevels)}
            className="text-base text-blue-600 hover:text-blue-800"
          >
            {showAllExperienceLevels ? 'See less' : 'See more'}
          </button>
        </div>
      </div>

      {/* Salary Filter */}
      <div className="border-t border-gray-200 pt-4">
        <h3 className="font-semibold text-gray-900 mb-2">Salary</h3>
        <div className="px-2">
          <SalarySlider
            value={params.min_annual_salary || 0}
            onChange={(value) => {
              onFilterChange({ min_annual_salary: value });
            }}
          />
        </div>
      </div>
    </div>
  );
} 