import { JobBrief } from '../types/api';
import { JobCard } from './JobCard';

interface JobListProps {
  jobs: JobBrief[];
  isLoading: boolean;
  total: number;
  searchQuery?: string;
}

export function JobList({ jobs, isLoading, total, searchQuery }: JobListProps) {
  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="h-32 bg-gray-200 rounded-lg"></div>
          </div>
        ))}
      </div>
    );
  }

  const jobList = Array.isArray(jobs) ? jobs : [];

  if (jobList.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No jobs found. Try adjusting your search.</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-lg text-gray-600">
          {searchQuery ? (
            <span>Found {total} jobs for "{searchQuery}"</span>
          ) : (
            <span>{total} jobs available</span>
          )}
        </h2>
      </div>
      
      <div className="space-y-4">
        {jobList.map(job => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
    </div>
  );
}