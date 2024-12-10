import { useState, useCallback } from 'react';
import { SearchBar } from './SearchBar';
import { JobList } from './JobList';
import { Filters } from './Filters';
import { JobBrief, SearchParams } from '../types/api';
import { searchJobs } from '../services/api';
import { JobSortBy } from '../types/job';

export function SearchPage() {
  const [jobs, setJobs] = useState<JobBrief[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [searchParams, setSearchParams] = useState<SearchParams>({
    page: 1,
    per_page: 10, // Changed to 9 for 3x3 grid
    sort_by: JobSortBy.RELEVANCE
  });

  const handleSearch = useCallback(async (newParams: Partial<SearchParams>) => {
    setIsLoading(true);
    try {
      const updatedParams = { ...searchParams, ...newParams };
      if (newParams.page === 1) {
        // Clear existing results if it's a new search
        setJobs([]);
      }
      const response = await searchJobs(updatedParams);
      setHasSearched(true);
      if (newParams.page === 1) {
        setJobs(response.results);
      } else {
        setJobs(prev => [...prev, ...response.results]);
      }
      setTotal(response.total);
      setSearchParams(updatedParams);
    } catch (error) {
      console.error('Failed to search jobs:', error);
    } finally {
      setIsLoading(false);
    }
  }, [searchParams]);

  const handleLoadMore = () => {
    handleSearch({ page: (searchParams.page || 1) + 1 });
  };

  const handleClearFilters = () => {
    setSearchParams(prev => ({
      q: prev.q,
      page: 1,
      per_page: 10,
      sort_by: JobSortBy.RELEVANCE
    }));
    handleSearch({
      page: 1,
      company_ids: undefined,
      employment_types: undefined,
      experience_levels: undefined
    });
  };

  return (
    <div className="max-w-[1400px] mx-auto px-6 py-8">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Find Your Next Opportunity</h1>
        <p className="text-gray-600">Search through millions of jobs from top companies</p>
      </div>

      <div className="flex gap-8">
        {/* Filters Section */}
        <div className="w-[280px] flex-shrink-0">
          <div className="sticky top-4">
            <Filters
              params={searchParams}
              onFilterChange={(newParams) => handleSearch({ ...newParams, page: 1 })}
              onClear={handleClearFilters}
            />
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 min-w-0">
          <SearchBar
            initialQuery={searchParams.q}
            sortBy={searchParams.sort_by}
            total={total}
            hasSearched={hasSearched}
            onSearch={(query) => handleSearch({ q: query, page: 1 })}
            onSortChange={(sort_by) => handleSearch({ sort_by, page: 1 })}
          />
          
          <JobList
            jobs={jobs}
            searchQuery={searchParams.q}
            isLoading={isLoading}
            hasMore={jobs.length < total}
            onLoadMore={handleLoadMore}
          />
        </div>
      </div>
    </div>
  );
} 