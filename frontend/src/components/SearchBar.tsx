import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { JobSortBy } from '../types/job';

interface SearchBarProps {
  initialQuery?: string;
  sortBy?: JobSortBy;
  total?: number;
  hasSearched?: boolean;
  onSearch: (query: string) => void;
  onSortChange: (sortBy: JobSortBy) => void;
}

export function SearchBar({
    initialQuery = '',
    sortBy = JobSortBy.RELEVANCE,
    total = 0,
    hasSearched = false,
    onSearch,
    onSortChange
}: SearchBarProps) {
  const [query, setQuery] = useState(initialQuery);

  useEffect(() => {
    setQuery(initialQuery);
  }, [initialQuery]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <div className="mb-8">
      <form onSubmit={handleSubmit} className="mb-4">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for jobs..."
            className="w-full px-6 py-4 text-lg border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-black/5 focus:border-black/20"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full hover:bg-gray-100 transition-colors"
          >
            <Search className="w-6 h-6" />
          </button>
        </div>
      </form>

      <div className="flex justify-between items-center">
        <div className="text-gray-600">
          {hasSearched && initialQuery && <span>Found {total} jobs for "{initialQuery}"</span>}
        </div>
        <select
          value={sortBy}
          onChange={(e) => onSortChange(Number(e.target.value) as JobSortBy)}
          className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black/5"
        >
          <option value={JobSortBy.RELEVANCE}>Sort by: Relevance</option>
          <option value={JobSortBy.DATE}>Sort by: Date</option>
        </select>
      </div>
    </div>
  );
}