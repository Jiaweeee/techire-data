import { useNavigate } from 'react-router-dom';
import { JobBrief } from '../types/api';
import { MapPin, Building2, Clock, Briefcase } from 'lucide-react';
import { getExperienceLevelLabel } from '../types/experience';
import { getSalaryPeriodLabel } from '../types/salary';

interface JobCardProps {
  job: JobBrief;
}

export function JobCard({ job }: JobCardProps) {
  const navigate = useNavigate();
  const postedDate = job.posted_date ? new Date(job.posted_date) : null;

  const formatSalary = () => {
    if (!job.salary_range) return null;
    const { min, max, fixed, currency = 'USD', period } = job.salary_range;
    const periodLabel = getSalaryPeriodLabel(period || null);
    
    if (fixed) return `${currency} ${fixed.toLocaleString()}${periodLabel}`;
    if (min && max) return `${currency} ${min.toLocaleString()} - ${max.toLocaleString()}${periodLabel}`;
    if (min) return `${currency} ${min.toLocaleString()}+${periodLabel}`;
    if (max) return `Up to ${currency} ${max.toLocaleString()}${periodLabel}`;
    return null;
  };

  return (
    <div
      onClick={() => navigate(`/jobs/${job.id}`)}
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

          {/* Title and Company */}
          <div className="flex-1 min-w-0">
            <h3 className="font-medium text-lg text-gray-900 mb-1 line-clamp-1">
              {job.title}
            </h3>
            <p className="text-gray-600">{job.company.name}</p>
          </div>

          {/* Apply Button */}
          {job.url && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                window.open(job.url, '_blank');
              }}
              className="flex-shrink-0 text-sm font-medium text-blue-600 hover:text-blue-800"
            >
              Apply
            </button>
          )}
        </div>

        {/* Job Details */}
        <div className="space-y-4">
          {/* Location and Type */}
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <span className="flex items-center gap-1.5">
              <MapPin className="w-4 h-4" />
              {job.location}
            </span>
            {job.is_remote && (
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
                Remote
              </span>
            )}
          </div>

          {/* Tags */}
          {(job.experience_level || formatSalary()) && (
            <div className="flex flex-wrap gap-2">
              {job.experience_level && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                  <Briefcase className="w-3.5 h-3.5 mr-1" />
                  {getExperienceLevelLabel(job.experience_level)}
                </span>
              )}
              {formatSalary() && (
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-50 text-green-700">
                  {formatSalary()}
                </span>
              )}
            </div>
          )}

          {/* Posted Date */}
          {postedDate && (
            <div className="flex items-center gap-1.5 text-sm text-gray-500">
              <Clock className="w-4 h-4" />
              <span>
                {new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(
                  Math.ceil((postedDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24)),
                  'day'
                )}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}