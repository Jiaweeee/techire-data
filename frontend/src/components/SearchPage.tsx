import { useState, useCallback, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { SearchBar } from './SearchBar';
import { JobList } from './JobList';
import { Filters, FilterTag } from './Filters';
import { JobBrief, SearchParams } from '../types/api';
import { searchJobs } from '../services/api';
import { JobSortBy } from '../types/job';
import { ChevronDown, MessageCircle, HelpCircle } from 'lucide-react';
import { Logo } from './Logo';
import { Head } from './Head';

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
  const [showFeedback, setShowFeedback] = useState(false);
  const feedbackBtnRef = useRef<HTMLDivElement>(null);

  const handleSearch = useCallback(async (newParams: Partial<SearchParams>) => {
    setIsLoading(true);
    const updatedParams = { ...params, ...newParams };
    if (newParams.page === 1) {
      // Clear existing results if it's a new search
      setJobs([]);
    }
    try {
      const response = await searchJobs(updatedParams);
      if (newParams.page === 1) {
        setJobs(response.results);
      } else {
        setJobs(prev => [...prev, ...response.results]);
      }
      setTotal(response.total);
    } catch (error) {
      console.error('Failed to search jobs:', error);
    } finally {
      setParams(updatedParams);
      if (updatedParams.q) {
        setSearchParams({ q: updatedParams.q });
      }
      setIsLoading(false);
    }
  }, [params, setSearchParams]);

  useEffect(() => {
    const query = searchParams.get('q');
    if (query) {
      handleSearch({ q: query, page: 1 });
    }
  }, []);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        feedbackBtnRef.current &&
        !feedbackBtnRef.current.contains(event.target as Node)
      ) {
        setShowFeedback(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
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
        case 'location':
            handleSearch({ 
                locations: params.locations?.filter(location => location !== tag.value),
                page: 1
            });
            break;
    }
  };

  const query = searchParams.get('q');
  
  return (
    <>
      <Head 
        title={query ? `${query} - Job Search` : 'Search Tech Jobs'}
        description={query 
          ? `Browse tech jobs matching "${query}". Find the latest opportunities from top tech companies.`
          : 'Search thousands of tech jobs from leading technology companies. Direct access to real job opportunities.'
        }
        canonical={`${window.location.origin}/search${query ? `?q=${query}` : ''}`}
        type="website"
      />
      <div className="min-h-screen bg-gray-50">
        {/* Search Container */}
        <div>
          <div className="max-w-5xl mx-auto px-4 py-12">
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

      {/* Feedback Button */}
      <div className="fixed bottom-8 right-8 z-50">
        <div className="relative">
          <button
            onClick={() => setShowFeedback(!showFeedback)}
            className="w-10 h-10 rounded-full bg-white text-gray-500 flex items-center justify-center shadow-lg hover:bg-gray-100 transition-colors"
          >
            <HelpCircle className="w-5 h-5" />
          </button>
          
          {showFeedback && (
            <div className="absolute bottom-14 right-0 bg-white rounded-lg shadow-lg p-2 w-36">
              <div ref={feedbackBtnRef} className="flex items-center justify-center hover:bg-gray-100 w-full">
                <MessageCircle className="w-5 h-5 text-gray-500" />
                <button
                  onClick={() => {
                    setShowFeedback(false);
                    window.open('https://realtechjobs.featurebase.app/', '_blank');
                  }}
                  className="text-center text-gray-500 px-2 py-1 rounded"
                >
                  Feedback
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
} 