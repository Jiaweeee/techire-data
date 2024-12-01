import { useNavigate } from 'react-router-dom';
import { JobDetail } from '../types/api';
import { MapPin, Building2, Clock, Globe } from 'lucide-react';

interface JobCardProps {
  job: JobDetail;
}

export function JobCard({ job }: JobCardProps) {
  const navigate = useNavigate();
  const postedDate = job.posted_date ? new Date(job.posted_date) : null;
  const timeAgo = postedDate
    ? new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(
        Math.ceil((postedDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24)),
        'day'
      )
    : 'Recently';

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
                  {job.employment_type}
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
      
      <p className="text-gray-600 mb-4 line-clamp-2">{job.full_description}</p>
      
      <div className="flex justify-between items-center text-sm text-gray-500">
        {job.salary_range && (
          <span className="font-medium">{job.salary_range}</span>
        )}
        <span className="flex items-center gap-1">
          <Clock className="w-4 h-4" />
          {timeAgo}
        </span>
      </div>
      
      {job.skill_tags && (
        <div className="mt-4 flex flex-wrap gap-2">
          {job.skill_tags.split(',').map((tag) => (
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