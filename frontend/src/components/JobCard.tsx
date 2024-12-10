import { useNavigate } from 'react-router-dom';
import { JobBrief } from '../types/api';
import { MapPin, Building2, Clock, Briefcase, DollarSign } from 'lucide-react';
import { getExperienceLevelLabel } from '../types/experience';
import { getSalaryPeriodLabel } from '../types/salary';

interface JobCardProps {
  job: JobBrief;
}

export function JobCard({ job }: JobCardProps) {
    const navigate = useNavigate();
    const postedDate = job.posted_date ? new Date(job.posted_date) : null;
    
    const formatSalary = () => {
      if (!job.salary_range) return 'Unknown';
      const { min, max, fixed, currency = 'USD', period } = job.salary_range;
      const periodLabel = getSalaryPeriodLabel(period || null);
      
      if (fixed) return `${currency} ${fixed.toLocaleString()}${periodLabel}`;
      if (min && max) return `${currency} ${min.toLocaleString()} - ${max.toLocaleString()}${periodLabel}`;
      if (min) return `${currency} ${min.toLocaleString()}+${periodLabel}`;
      if (max) return `Up to ${currency} ${max.toLocaleString()}${periodLabel}`;
      return 'Unknown';
    };
  
    return (
      <div
        onClick={() => navigate(`/jobs/${job.id}`)}
        className="bg-white rounded-lg shadow-sm border hover:shadow-md transition-all cursor-pointer h-full flex flex-col p-6 gap-4"
      >
        {/* Company Logo & Title Section */}
        <div className="flex gap-4">
          {/* Logo Container */}
          {job.company.icon_url ? (
            <img
              src={job.company.icon_url}
              alt={job.company.name}
              className="w-12 h-12 rounded-lg object-cover flex-shrink-0 border border-gray-100"
            />
          ) : (
            <div className="w-12 h-12 rounded-lg bg-gray-50 border border-gray-100 flex items-center justify-center flex-shrink-0">
              <Building2 className="w-6 h-6 text-gray-400" />
            </div>
          )}
          
          {/* Title and Company Info */}
          <div className="min-w-0 flex-1">
            <h3 className="font-semibold text-base text-gray-900 mb-1 line-clamp-1">{job.title}</h3>
            <p className="text-gray-500 text-sm">{job.company.name}</p>
          </div>
        </div>
  
        {/* Job Description */}
        {job.summary && (
          <p className="text-gray-600 text-sm leading-relaxed line-clamp-2">{job.summary}</p>
        )}
  
        {/* Tags and Info Section */}
        <div className="space-y-4 mt-auto">
          {/* Primary Tags */}
          <div className="flex flex-wrap gap-2">
            {job.experience_level && (
              <span className="bg-blue-50 text-blue-700 px-2.5 py-1 rounded text-xs font-medium inline-flex items-center gap-1">
                <Briefcase className="w-3.5 h-3.5" />
                {getExperienceLevelLabel(job.experience_level)}
              </span>
            )}
            <span className="bg-green-50 text-green-700 px-2.5 py-1 rounded text-xs font-medium inline-flex items-center gap-1">
              <DollarSign className="w-3.5 h-3.5" />
              {formatSalary()}
            </span>
          </div>
  
          {/* Location Info */}
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2 text-gray-600 text-sm">
              <MapPin className="w-4 h-4 text-gray-400" />
              <span>{job.location}</span>
              {job.is_remote && (
                <span className="bg-gray-50 text-gray-600 px-2 py-0.5 rounded text-xs font-medium">
                  Remote
                </span>
              )}
            </div>
          </div>
  
          {/* Bottom Row - Posted Date and Apply Button */}
          <div className="flex items-center justify-between pt-2 border-t border-gray-100">
            <div className="flex items-center gap-1.5 text-gray-500 text-sm">
              <Clock className="w-4 h-4" />
              <span>
                {postedDate
                  ? new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(
                      Math.ceil((postedDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24)),
                      'day'
                    )
                  : 'Recent'}
              </span>
            </div>
            {job.url && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  window.open(job.url, '_blank');
                }}
                className="border border-blue-200 bg-blue-50 hover:bg-blue-100 text-blue-600 px-4 py-1.5 rounded text-sm font-medium transition-colors"
              >
                Apply Now
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }