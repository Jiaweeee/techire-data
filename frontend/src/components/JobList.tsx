import { JobBrief } from '../types/api';
import { JobCard } from './JobCard';

interface JobListProps {
  jobs: JobBrief[];
  isLoading: boolean;
  total: number;
  searchQuery?: string;
  hasMore: boolean;
  onLoadMore: () => void;
}

export function JobList({ jobs, isLoading, total, hasMore, onLoadMore }: JobListProps) {
  if (isLoading && jobs.length === 0) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="bg-white rounded-lg shadow-sm border p-6 space-y-4">
              <div className="flex gap-4">
                <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
              <div className="h-16 bg-gray-200 rounded"></div>
              <div className="flex gap-2">
                <div className="h-6 bg-gray-200 rounded w-20"></div>
                <div className="h-6 bg-gray-200 rounded w-20"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No jobs found. Try adjusting your search criteria.</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {jobs.map(job => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
      
      {hasMore && (
        <div className="text-center pt-8">
          <button
            onClick={onLoadMore}
            className="px-6 py-3 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 font-medium"
          >
            {isLoading ? 'Loading...' : 'Load More'}
          </button>
        </div>
      )}
    </div>
  );
}