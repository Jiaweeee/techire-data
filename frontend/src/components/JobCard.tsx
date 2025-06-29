import { useState } from 'react';
import { JobBrief } from '../types/api';
import { MapPin, Building2, Clock, Briefcase } from 'lucide-react';
import { getExperienceLevelLabel } from '../types/experience';
import { SalaryDisplay } from './SalaryDisplay';

interface JobCardProps {
  job: JobBrief;
}

export function JobCard({ job }: JobCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const postedDate = job.posted_date ? new Date(job.posted_date) : null;

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsExpanded(!isExpanded);
  };

  return (
    <div
      onClick={() => window.open(`/jobs/${job.id}`, '_blank')}
      className="bg-white border rounded-lg hover:shadow-md transition-shadow cursor-pointer"
    >
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start gap-4 mb-4">
          {/* Company Logo */}
          {job.company.icon_url ? (
            <img
              src={job.company.icon_url}
              alt={job.company.name}
              className="w-12 h-12 rounded object-contain border border-gray-100 bg-white flex-shrink-0"
            />
          ) : (
            <div className="w-12 h-12 rounded bg-gray-50 border border-gray-100 flex items-center justify-center flex-shrink-0">
              <Building2 className="w-6 h-6 text-gray-400" />
            </div>
          )}

          {/* Title, Company and Posted Date */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between gap-4">
              <h3 className="font-medium text-lg text-gray-900 mb-1 line-clamp-1">
                {job.title}
              </h3>
              <span className="flex items-center gap-1.5 text-sm text-gray-500 flex-shrink-0">
                <Clock className="w-4 h-4" />
                <span>
                  {postedDate 
                    ? new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(
                        Math.ceil((postedDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24)),
                        'day'
                      )
                    : 'Recently'}
                </span>
              </span>
            </div>
            <p className="text-gray-600">{job.company.name}</p>
          </div>
        </div>

        {/* Job Summary */}
        {job.summary && (
          <div className="mb-4">
            <p className={`text-sm text-gray-600 ${!isExpanded ? 'line-clamp-1' : ''}`}>
              {job.summary}
            </p>
            <button
              onClick={handleClick}
              className="text-sm text-blue-600 hover:text-blue-700 mt-1 font-medium"
            >
              {isExpanded ? 'Show less' : 'See more'}
            </button>
          </div>
        )}

        {/* Divider */}
        <div className="h-px bg-gray-200 mb-4" />

        {/* Job Details */}
        <div className="space-y-4">
          {/* Location, Experience, Salary */}
          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
            <span className="flex items-center gap-1.5 min-w-0 truncate">
              <MapPin className="w-4 h-4 flex-shrink-0" />
              <span className="truncate">
                {job.locations.length === 1 ? (
                  job.locations[0]
                ) : (
                  <>
                    {job.locations[0]}
                    <span>
                      {`; +${job.locations.length - 1} more`}
                    </span>
                  </>
                )}
              </span>
            </span>

            {job.is_remote && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 flex-shrink-0">
                Remote
              </span>
            )}
            
            {job.experience_level && (
              <>
                <div className="w-px h-4 bg-gray-200 flex-shrink-0" />
                <span className="flex items-center gap-1.5 flex-shrink-0">
                  <Briefcase className="w-4 h-4" />
                  {getExperienceLevelLabel(job.experience_level)}
                </span>
              </>
            )}

            <>
              <div className="w-px h-4 bg-gray-200 flex-shrink-0" />
              <SalaryDisplay salaryRange={job.salary_range} />
            </>
          </div>
        </div>
      </div>
    </div>
  );
}