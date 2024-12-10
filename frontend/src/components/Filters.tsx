import { useState, useEffect } from 'react';
import { ChevronDown, ChevronUp, Search } from 'lucide-react';
import { SearchParams, CompanyBrief } from '../types/api';
import { getEmploymentTypeLabel } from '../types/employment';
import { getExperienceLevelLabel } from '../types/experience';
import { searchCompanies } from '../services/api';
import { useDebounce } from '../hooks/useDebounce';

interface FiltersProps {
  params: SearchParams;
  onFilterChange: (params: Partial<SearchParams>) => void;
  onClear: () => void;
}

export function Filters({ params, onFilterChange, onClear }: FiltersProps) {
  const [companySearch, setCompanySearch] = useState('');
  const [companies, setCompanies] = useState<CompanyBrief[]>([]);
  const [sections, setSections] = useState({
    companies: true,
    employmentType: true,
    experienceLevel: true,
  });
  const debouncedSearch = useDebounce(companySearch, 300);

  useEffect(() => {
    async function fetchCompanies() {
      if (debouncedSearch) {
        try {
          const data = await searchCompanies(debouncedSearch);
          setCompanies(data);
        } catch (error) {
          console.error('Failed to search companies:', error);
          setCompanies([]);
        }
      } else {
        setCompanies([]);
      }
    }
    fetchCompanies();
  }, [debouncedSearch]);

  const toggleSection = (section: keyof typeof sections) => {
    setSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border p-6 space-y-6">
      {/* Title and Clear button */}
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold">Filters</h2>
        <button
          onClick={onClear}
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          Clear
        </button>
      </div>

      {/* Divider */}
      <div className="border-t"></div>

      {/* Companies Filter */}
      <div>
        <button
          onClick={() => toggleSection('companies')}
          className="flex justify-between items-center w-full mb-4"
        >
          <h3 className="font-medium">Companies</h3>
          {sections.companies ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
        
        {sections.companies && (
          <div className="space-y-4">
            <div className="relative">
              <input
                type="text"
                value={companySearch}
                onChange={(e) => setCompanySearch(e.target.value)}
                placeholder="Search companies..."
                className="w-full px-4 py-2 border rounded-lg pr-10"
              />
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            </div>
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {companies.map(company => (
                <label key={company.id} className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={params.company_ids?.includes(company.id)}
                    onChange={(e) => {
                      const newCompanyIds = e.target.checked
                        ? [...(params.company_ids || []), company.id]
                        : (params.company_ids || []).filter(id => id !== company.id);
                      onFilterChange({ company_ids: newCompanyIds });
                    }}
                    className="rounded border-gray-300"
                  />
                  {company.name}
                </label>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Dividers between sections */}
      <div className="border-t"></div>

      {/* Employment Type Filter */}
      <div>
        <button
          onClick={() => toggleSection('employmentType')}
          className="flex justify-between items-center w-full mb-4"
        >
          <h3 className="font-medium">Employment Type</h3>
          {sections.employmentType ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
        
        {sections.employmentType && (
          <div className="space-y-2">
            {[1, 2, 3, 4, 5, 6, 7, 8].map(type => (
              <label key={type} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={params.employment_types?.includes(type)}
                  onChange={(e) => {
                    const newTypes = e.target.checked
                      ? [...(params.employment_types || []), type]
                      : (params.employment_types || []).filter(t => t !== type);
                    onFilterChange({ employment_types: newTypes });
                  }}
                  className="rounded border-gray-300"
                />
                {getEmploymentTypeLabel(type)}
              </label>
            ))}
          </div>
        )}
      </div>

      {/* Divider */}
      <div className="border-t"></div>

      {/* Experience Level Filter */}
      <div>
        <button
          onClick={() => toggleSection('experienceLevel')}
          className="flex justify-between items-center w-full mb-4"
        >
          <h3 className="font-medium">Experience Level</h3>
          {sections.experienceLevel ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
        
        {sections.experienceLevel && (
          <div className="space-y-2">
            {[1, 2, 3, 4, 5].map(level => (
              <label key={level} className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={params.experience_levels?.includes(level)}
                  onChange={(e) => {
                    const newLevels = e.target.checked
                      ? [...(params.experience_levels || []), level]
                      : (params.experience_levels || []).filter(l => l !== level);
                    onFilterChange({ experience_levels: newLevels });
                  }}
                  className="rounded border-gray-300"
                />
                {getExperienceLevelLabel(level)}
              </label>
            ))}
          </div>
        )}
      </div>
    </div>
  );
} 