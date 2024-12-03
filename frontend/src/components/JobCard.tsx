import { useNavigate } from 'react-router-dom';
import { JobBrief } from '../types/api';
import { MapPin, Building2, Clock, Globe } from 'lucide-react';
import { getEmploymentTypeLabel } from '../types/employment';

interface JobCardProps {
  job: JobBrief;
}

export function JobCard({ job }: JobCardProps) {
  const navigate = useNavigate();
  const postedDate = job.posted_date ? new Date(job.posted_date) : null;
  
  // Format salary range
  const formatSalary = () => {
    if (!job.salary_range) return null;
    const { min, max, fixed, currency = 'USD' } = job.salary_range;
    if (fixed) return `${currency} ${fixed.toLocaleString()}`;
    if (min && max) return `${currency} ${min.toLocaleString()} - ${max.toLocaleString()}`;
    if (min) return `${currency} ${min.toLocaleString()}+`;
    if (max) return `Up to ${currency} ${max.toLocaleString()}`;
    return null;
  };

  return (
    <div
      className="bg-white p-6 rounded-lg shadow-sm border hover:shadow-md transition-shadow cursor-pointer"
      onClick={() => navigate(`/jobs/${job.id}`)}
    >
      <div className="flex justify-between items-start mb-4">
        <div className="flex gap-4">
        {job.company.icon_url ? (
            <img
              src={job.company.icon_url}
              alt={job.company.name}
              className="w-12 h-12 rounded-lg object-cover"
            />
          ) : (
            <div className="w-12 h-12 rounded-lg bg-gray-100 flex items-center justify-center">
              <Building2 className="w-6 h-6 text-gray-400" />
            </div>
          )}
          <div>
            <h3 className="text-xl font-semibold mb-2">{job.title}</h3>
            <div className="flex items-center gap-4 text-gray-600">
              <span className="flex items-center gap-1">
                <Building2 className="w-4 h-4" />
                {job.company.name}
              </span>
              <span className="flex items-center gap-1">
                <MapPin className="w-4 h-4" />
                {job.location}
              </span>
              {job.employment_type && (
                <span className="text-gray-500 text-sm">
                  {getEmploymentTypeLabel(job.employment_type)}
                </span>
              )}
            </div>
          </div>
        </div>
        {job.is_remote && (
          <span className="flex items-center gap-1 bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
            <Globe className="w-4 h-4" />
            Remote
          </span>
        )}
      </div>
      
      {job.summary && (
        <p className="text-gray-600 mb-4 line-clamp-2">{job.summary}</p>
      )}
      
      <div className="flex justify-between items-center text-sm text-gray-500">
        {formatSalary() && (
          <span className="font-medium">{formatSalary()}</span>
        )}
        {postedDate && (
          <span className="flex items-center gap-1">
            <Clock className="w-4 h-4" />
            {new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(
              Math.ceil((postedDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24)),
              'day'
            )}
          </span>
        )}
      </div>
      
      {job.skill_tags && job.skill_tags.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-2">
          {job.skill_tags.map((tag) => (
            <span
              key={tag}
              className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
            >
              {tag.trim()}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}