import { useState } from 'react';
import { Calendar, Briefcase } from 'lucide-react';

interface SearchFiltersProps {
  onFilterChange: (filters: {
    posted_after?: string;
    is_remote?: boolean;
    per_page?: number;
  }) => void;
}

export function SearchFilters({ onFilterChange }: SearchFiltersProps) {
  const [isRemote, setIsRemote] = useState<boolean | undefined>(undefined);
  const [postedAfter, setPostedAfter] = useState<string>('');

  const handleRemoteChange = (value: boolean) => {
    setIsRemote(value);
    onFilterChange({ is_remote: value });
  };

  const handlePostedAfterChange = (value: string) => {
    setPostedAfter(value);
    if (value) {
      const date = new Date();
      switch (value) {
        case '24h':
          date.setHours(date.getHours() - 24);
          break;
        case '7d':
          date.setDate(date.getDate() - 7);
          break;
        case '30d':
          date.setDate(date.getDate() - 30);
          break;
      }
      onFilterChange({ posted_after: date.toISOString() });
    } else {
      onFilterChange({ posted_after: undefined });
    }
  };

  return (
    <div className="flex flex-wrap gap-4 items-center justify-center mb-8">
      <div className="flex items-center gap-2">
        <Calendar className="w-4 h-4 text-gray-500" />
        <select
          value={postedAfter}
          onChange={(e) => handlePostedAfterChange(e.target.value)}
          className="border rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-black/5"
        >
          <option value="">Any time</option>
          <option value="24h">Past 24 hours</option>
          <option value="7d">Past week</option>
          <option value="30d">Past month</option>
        </select>
      </div>

      <div className="flex items-center gap-4">
        <Briefcase className="w-4 h-4 text-gray-500" />
        <div className="flex gap-2">
          <button
            onClick={() => handleRemoteChange(true)}
            className={`px-3 py-1.5 text-sm rounded-md ${
              isRemote === true
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-700'
            }`}
          >
            Remote
          </button>
          <button
            onClick={() => handleRemoteChange(false)}
            className={`px-3 py-1.5 text-sm rounded-md ${
              isRemote === false
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-700'
            }`}
          >
            On-site
          </button>
          <button
            onClick={() => handleRemoteChange(undefined)}
            className={`px-3 py-1.5 text-sm rounded-md ${
              isRemote === undefined
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-700'
            }`}
          >
            All
          </button>
        </div>
      </div>
    </div>
  );
}