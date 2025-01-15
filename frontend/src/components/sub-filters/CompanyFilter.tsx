import { useState, useEffect, useRef } from "react";
import { Search } from "lucide-react";
import { SearchParams, CompanyBrief } from "../../types/api";
import { useDebounce } from "../../hooks/useDebounce";

// Company Filter Component
interface CompanyFilterProps {
  params: SearchParams;
  onFilterChange: (params: Partial<SearchParams>) => void;
  companies: CompanyBrief[]; // Add companies prop
}

export function CompanyFilter({
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