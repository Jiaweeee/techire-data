import { JobBrief } from '../types/api';
import { JobCard } from './JobCard';

interface JobListProps {
  jobs: JobBrief[];
  isLoading: boolean;
  hasMore: boolean;
  total: number;
  onLoadMore: () => void;
}

export function JobList({ jobs, isLoading, hasMore, total, onLoadMore }: JobListProps) {
  if (isLoading && jobs.length === 0) {
    return (
      <div className="grid gap-4">
        {[...Array(10)].map((_, i) => (
          <div key={i} className="animate-pulse bg-white rounded-lg p-4">
            <div className="flex gap-4">
              <div className="w-12 h-12 bg-gray-200 rounded"></div>
              <div className="flex-1 space-y-3">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="text-center py-36">
        <p className="text-gray-400 text-xl font-semibold">
            There are currently no open roles matching your search.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {jobs.map(job => (
        <JobCard key={job.id} job={job} />
      ))}
      
      <div className="text-center text-gray-400 pt-6">
        Showing {jobs.length} out of {total} jobs
      </div>

      {hasMore && (
        <div className="text-center pb-6">
          <button
            onClick={onLoadMore}
            className="px-6 py-2 border border-gray-300 rounded-lg text-gray-400 hover:bg-gray-50 transition-colors"
          >
            {isLoading ? 'Loading...' : 'Load More'}
          </button>
        </div>
      )}
    </div>
  );
}