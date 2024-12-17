import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Building2, MapPin, Briefcase, Clock } from 'lucide-react';
import { getJobDetail } from '../services/api';
import type { JobDetail } from '../types/api';
import { getEmploymentTypeLabel } from '../types/employment';
import { getExperienceLevelLabel } from '../types/experience';
import { SalaryDisplay } from './SalaryDisplay';
import { Head } from './Head';

export function JobDetailPage() {
  const { jobId } = useParams();
  const [job, setJob] = useState<JobDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLocationsExpanded, setIsLocationsExpanded] = useState(false);

  useEffect(() => {
    async function loadJob() {
      if (!jobId) return;
      try {
        const jobData = await getJobDetail(jobId);
        setJob(jobData);
        document.title = `${jobData.title} at ${jobData.company.name}`;
      } catch (error) {
        console.error('Failed to load job:', error);
      } finally {
        setIsLoading(false);
      }
    }
    loadJob();
  }, [jobId]);

  const handleLocationsClick = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsLocationsExpanded(!isLocationsExpanded);
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
        <div className="h-64 bg-gray-200 rounded"></div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="max-w-4xl mx-auto text-center py-12">
        <p className="text-gray-500">Job not found</p>
      </div>
    );
  }

  return (
    <>
      {job && (
        <Head 
          title={`${job.title} at ${job.company.name}`}
          description={`${job.title} position at ${job.company.name}. ${
            job.summary ? job.summary.slice(0, 150) + '...' : ''
          }`}
          canonical={`${window.location.origin}/jobs/${job.id}`}
        />
      )}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column - Job Details */}
          <div className="lg:col-span-4 space-y-6">
            {/* Header Section */}
            <div className="space-y-4">
              {/* Company Info */}
              <div className="flex items-center gap-2">
                {job.company.icon_url ? (
                  <img
                    src={job.company.icon_url}
                    alt={job.company.name}
                    className="w-10 h-10 rounded object-contain border border-gray-100 bg-white flex-shrink-0"
                  />
                ) : (
                  <div className="w-10 h-10 rounded bg-gray-50 border border-gray-100 flex items-center justify-center flex-shrink-0">
                    <Building2 className="w-5 h-5 text-gray-400" />
                  </div>
                )}
                <span className="text-gray-500 font-medium">{job.company.name}</span>
              </div>

              {/* Job Title */}
              <h1 className="font-medium text-2xl text-gray-900">{job.title}</h1>
            </div>

            {/* Job Details Card */}
            <div className="space-y-4 bg-white rounded-lg border p-4">
              <div className="flex flex-col gap-4 text-sm text-gray-500">
                <span className="flex items-center gap-1.5">
                  <MapPin className="w-4 h-4" />
                  {job.locations.length === 1 ? (
                    job.locations[0]
                  ) : (
                    <>
                      {isLocationsExpanded ? (
                        <div className="flex flex-col gap-1">
                          {job.locations.map((location, index) => (
                            <span key={index}>{location}</span>
                          ))}
                        </div>
                      ) : (
                        <>
                          {job.locations[0]}
                          <button
                            onClick={handleLocationsClick}
                            className="underline"
                          >
                            {` +${job.locations.length - 1} more`}
                          </button>
                        </>
                      )}
                    </>
                  )}
                  {job.is_remote && (
                    <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700">
                      Remote
                    </span>
                  )}
                </span>
                
                {job.employment_type && (
                  <span className="flex items-center gap-1.5">
                    <Clock className="w-4 h-4" />
                    {getEmploymentTypeLabel(job.employment_type)}
                  </span>
                )}
                
                {job.experience_level && (
                  <span className="flex items-center gap-1.5">
                    <Briefcase className="w-4 h-4" />
                    {getExperienceLevelLabel(job.experience_level)}
                  </span>
                )}

                {job.salary_range && (
                  <span className="flex items-center gap-1.5">
                    <SalaryDisplay salaryRange={job.salary_range} />
                  </span>
                )}
              </div>
            </div>

            {/* Skills Section */}
            {job.skill_tags && job.skill_tags.length > 0 && (
              <div className="bg-white rounded-lg border p-4">
                <h2 className="text-sm font-medium text-gray-900 mb-3">Required Skills</h2>
                <div className="flex flex-wrap gap-2">
                  {job.skill_tags.map((tag) => (
                    <span
                      key={tag}
                      className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
                    >
                      {tag.trim()}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Apply Button */}
            <a
              href={job.url}
              target="_blank"
              rel="noopener noreferrer"
              className="block w-full text-center px-6 py-3 bg-blue-600 text-white font-medium rounded-full 
                hover:bg-blue-700 transition-colors duration-200"
            >
              Apply Now
            </a>
          </div>

          {/* Right Column - Job Description */}
          <div className="lg:col-span-8">
            <div className="bg-white rounded-lg border p-6">
              <div 
                dangerouslySetInnerHTML={{
                  __html: job.full_description
                }}
                className="prose prose-gray max-w-none job-section"
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}