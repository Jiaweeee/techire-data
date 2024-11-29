import { Search } from 'lucide-react';
import { useState } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
}

export function SearchBar({ onSearch }: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-3xl">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for jobs..."
          className="w-full px-6 py-4 text-lg border rounded-full shadow-sm focus:outline-none focus:ring-2 focus:ring-black/5 focus:border-black/20"
        />
        <button
          type="submit"
          className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full hover:bg-gray-100 transition-colors"
        >
          <Search className="w-6 h-6" />
        </button>
      </div>
    </form>
  );
}