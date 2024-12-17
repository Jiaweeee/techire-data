import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { LucideCheckCircle } from 'lucide-react';
import { SearchBar } from './SearchBar';
import { getStats } from '../services/api';
import type { StatsResponse } from '../types/api';
import { Head } from './Head';

export function HomePage() {
  const navigate = useNavigate();
  const [stats, setStats] = useState<StatsResponse | null>(null);

  useEffect(() => {
    async function fetchStats() {
      try {
        const data = await getStats();
        setStats(data);
      } catch (error) {
        console.error('Failed to load stats:', error);
      }
    }
    fetchStats();
  }, []);

  const handleSearch = (query: string) => {
    navigate(`/search?q=${encodeURIComponent(query)}`);
  };

  return (
    <>
      <Head />
      <div className="min-h-screen flex flex-col items-center bg-gray-50 px-4">
        <div className="w-full max-w-3xl mx-auto text-center space-y-8 mt-[30vh]">
          {/* Logo */}
          <div className="flex justify-center">
            <LucideCheckCircle color="#FF0000" strokeWidth={3} className="w-16 h-16" />
          </div>

          {/* Slogan */}
          <h1 className="text-4xl font-bold text-gray-900">
              Find Fresh Tech Jobs Straight From The Source
          </h1>

          {/* Search */}
          <div className="mt-8">
            <SearchBar onSearch={handleSearch} />
          </div>

          {/* Stats */}
          <p className="text-gray-400">
            {stats ? (
              <>
                Indexed <span className="font-medium text-gray-900">{stats.total_jobs.toLocaleString()}</span> jobs directly from{' '}
                <span className="font-medium text-gray-900">{stats.total_companies.toLocaleString()}</span> official company career pages and counting
              </>
            ) : (
              null
            )}
          </p>
        </div>
      </div>
    </>
  );
} 