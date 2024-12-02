import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Logo } from './components/Logo';
import { SearchBar } from './components/SearchBar';
import { SearchFilters } from './components/SearchFilters';
import { JobList } from './components/JobList';
import { Pagination } from './components/Pagination';
import { searchJobs } from './services/api';
import type { JobDetail, SearchParams } from './types/api';
import { JobDetailPage } from './components/JobDetailPage';

function App() {
  const [jobs, setJobs] = useState<JobDetail[]>([]);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [currentQuery, setCurrentQuery] = useState('');
  const [searchParams, setSearchParams] = useState<SearchParams>({
    page: 1,
    per_page: 10,
  });

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setCurrentQuery(query);
    try {
      console.log('Searching with params:', { ...searchParams, q: query });
      const response = await searchJobs({ ...searchParams, q: query });
      console.log('Search response:', response);
      setJobs(response.results);
      setTotal(response.total);
    } catch (error) {
      console.error('Failed to search jobs:', error);
      setJobs([]);
      setTotal(0);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (filters: Partial<SearchParams>) => {
    const newParams = { ...searchParams, ...filters };
    setSearchParams(newParams);
  };

  const handlePageChange = (page: number) => {
    setSearchParams(prev => ({ ...prev, page }));
  };

  const handleQueryChange = (query: string) => {
    setCurrentQuery(query);
    setSearchParams(prev => ({ ...prev, q: query, page: 1 }));
  };

  useEffect(() => {
    if (currentQuery) {
      handleSearch(currentQuery);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams, currentQuery]);

  const totalPages = Math.ceil(total / (searchParams.per_page || 10));

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="container mx-auto px-4 py-4">
            <Logo />
          </div>
        </header>

        <main className="container mx-auto px-4 py-16">
          <Routes>
            <Route path="/" element={
              <div className="max-w-4xl mx-auto space-y-8">
                <h1 className="text-4xl font-bold text-center mb-2">
                  Find Your Next Opportunity
                </h1>
                <p className="text-gray-600 text-center mb-8">
                  Search through millions of jobs from top companies
                </p>

                <div className="flex justify-center">
                  <SearchBar onSearch={handleQueryChange} />
                </div>
                <SearchFilters onFilterChange={handleFilterChange} />

                <div className="mt-8">
                  <JobList 
                    jobs={jobs} 
                    isLoading={isLoading} 
                    total={total}
                    searchQuery={currentQuery}
                  />
                  <Pagination 
                    currentPage={searchParams.page || 1} 
                    totalPages={totalPages}
                    onPageChange={handlePageChange} 
                  />
                </div>
              </div>
            } />
            <Route path="/jobs/:jobId" element={<JobDetailPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;