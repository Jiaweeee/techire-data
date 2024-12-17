import { useState, useCallback, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { SearchBar } from './SearchBar';
import { JobList } from './JobList';
import { Filters, FilterTag } from './Filters';
import { JobBrief, SearchParams } from '../types/api';
import { searchJobs } from '../services/api';
import { JobSortBy } from '../types/job';
import { ChevronDown } from 'lucide-react';
import { Logo } from './Logo';

export function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [jobs, setJobs] = useState<JobBrief[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [params, setParams] = useState<SearchParams>({
    page: 1,
    per_page: 10,
    sort_by: JobSortBy.RELEVANCE,
    q: searchParams.get('q') || undefined
  });
  const [filterTags, setFilterTags] = useState<FilterTag[]>([]);

  const handleSearch = useCallback(async (newParams: Partial<SearchParams>) => {
    setIsLoading(true);
    try {
      const updatedParams = { ...params, ...newParams };
      if (newParams.page === 1) {
        // Clear existing results if it's a new search
        setJobs([]);
      }
      const response = await searchJobs(updatedParams);
      if (newParams.page === 1) {
        setJobs(response.results);
      } else {
        setJobs(prev => [...prev, ...response.results]);
      }
      setTotal(response.total);
      setParams(updatedParams);
      
      if (updatedParams.q) {
        setSearchParams({ q: updatedParams.q });
      }
    } catch (error) {
      console.error('Failed to search jobs:', error);
    } finally {
      setIsLoading(false);
    }
  }, [params, setSearchParams]);

  useEffect(() => {
    const query = searchParams.get('q');
    if (query) {
      handleSearch({ q: query, page: 1 });
    }
  }, []);

  const handleLoadMore = () => {
    handleSearch({ page: (params.page || 1) + 1 });
  };

  const handleClearFilters = () => {
    setParams(prev => ({
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

  const handleRemoveTag = (tag: FilterTag) => {
    switch (tag.type) {
      case 'company':
        handleSearch({ 
          company_ids: params.company_ids?.filter(id => id !== tag.value), 
          page: 1
        });
        break;
      case 'employment':
        handleSearch({ 
          employment_types: params.employment_types?.filter(type => type !== tag.value),
          page: 1
        });
        break;
      case 'experience':
        handleSearch({ 
          experience_levels: params.experience_levels?.filter(level => level !== tag.value),
          page: 1
        });
        break;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Search Container */}
      <div>
        <div className="max-w-5xl mx-auto px-4 py-8">
          <div className="flex items-center gap-12">
            {/* Left side - same width as Filters */}
            <div className="w-64 flex-shrink-0">
              <Logo />
            </div>
            {/* Right side - aligns with Results */}
            <div className="flex-1">
              <SearchBar
                initialQuery={params.q}
                onSearch={(query) => handleSearch({ q: query, page: 1 })}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto px-4 py-6">
        <div className="flex gap-12">
          {/* Filters */}
          <div className="w-64 flex-shrink-0">
            <Filters
              params={params}
              onFilterChange={(newParams) => handleSearch({ ...newParams, page: 1 })}
              onTagsChange={setFilterTags}
            />
          </div>

          {/* Results */}
          <div className="flex-1">
            {/* Selected Filters */}
            {filterTags.length > 0 && (
                <div className="mb-4 flex flex-wrap gap-2">
                {filterTags.map(tag => (
                    <span 
                    key={tag.id}
                    className="inline-flex items-center bg-gray-100 text-gray-700 text-sm rounded-full px-3 py-1"
                    >
                    {tag.label}
                    <button 
                        onClick={() => handleRemoveTag(tag)}
                        className="ml-2 text-gray-500 hover:text-gray-700"
                    >
                        ×
                    </button>
                    </span>
                ))}
                </div>
            )}
            {/* Results Header */}
            <div className="mb-4 flex items-center justify-between">
                <div className="relative">
                    <select
                        value={params.sort_by}
                        onChange={(e) => handleSearch({ sort_by: Number(e.target.value), page: 1 })}
                        className="appearance-none bg-white border rounded-lg px-4 py-2 pr-8 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                    >
                        <option value={JobSortBy.RELEVANCE}>Relevance</option>
                        <option value={JobSortBy.DATE}>Newest</option>
                    </select>
                    {/* Add dropdown arrow */}
                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                    <ChevronDown className="h-4 w-4" />
                </div>
            </div>
            
            <button
                onClick={handleClearFilters}
                className="text-sm text-gray-500 hover:bg-gray-100 rounded-md px-3 py-1.5"
            >
                Clear Filters
            </button>
            </div>
            

            {/* Job List */}
            <JobList
              jobs={jobs}
              isLoading={isLoading}
              hasMore={jobs.length < total}
              total={total}
              onLoadMore={handleLoadMore}
            />
          </div>
        </div>
      </div>
    </div>
  );
} 