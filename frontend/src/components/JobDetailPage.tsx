import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { ArrowLeft, Building2, MapPin, Globe, ExternalLink } from 'lucide-react';
import { getJobDetail } from '../services/api';
import type { JobDetail } from '../types/api';

export function JobDetailPage() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState<JobDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadJob() {
      if (!jobId) return;
      try {
        const jobData = await getJobDetail(jobId);
        setJob(jobData);
      } catch (error) {
        console.error('Failed to load job:', error);
      } finally {
        setIsLoading(false);
      }
    }
    loadJob();
  }, [jobId]);

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
    <div className="max-w-4xl mx-auto">
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-8"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to search
      </button>

      <div className="bg-white rounded-lg shadow-sm border p-8">
        <div className="flex justify-between items-start mb-6">
          <div className="flex gap-4 flex-1 min-w-0">
            <div className="flex-shrink-0">
              {job.company.icon_url ? (
                <img
                  src={job.company.icon_url}
                  alt={job.company.name}
                  className="w-16 h-16 rounded-lg object-cover"
                />
              ) : (
                <div className="w-16 h-16 rounded-lg bg-gray-100 flex items-center justify-center">
                  <Building2 className="w-8 h-8 text-gray-400" />
                </div>
              )}
            </div>
            <div className="min-w-0">
              <h1 className="text-2xl font-bold mb-2 line-clamp-2">{job.title}</h1>
              <div className="flex items-center gap-4 text-gray-600">
                <span className="flex items-center gap-1">
                  <Building2 className="w-4 h-4" />
                  {job.company.name}
                </span>
                <span className="flex items-center gap-1">
                  <MapPin className="w-4 h-4" />
                  {job.location}
                </span>
                {job.is_remote && (
                  <span className="flex items-center gap-1 bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                    <Globe className="w-4 h-4" />
                    Remote
                  </span>
                )}
              </div>
            </div>
          </div>
          
          <a
            href={job.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex-shrink-0 ml-4"
          >
            Apply Now
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>

        <div className="flex gap-4 mb-8">
          {job.salary_range && (
            <div className="bg-gray-100 px-4 py-2 rounded-lg">
              <span className="text-gray-600">Salary</span>
              <p className="font-medium">{job.salary_range}</p>
            </div>
          )}
          {job.employment_type && (
            <div className="bg-gray-100 px-4 py-2 rounded-lg">
              <span className="text-gray-600">Employment Type</span>
              <p className="font-medium">{job.employment_type}</p>
            </div>
          )}
        </div>

        <div className="prose max-w-none">
          <ReactMarkdown>{job.full_description}</ReactMarkdown>
        </div>

        {job.skill_tags && (
          <div className="mt-8 pt-8 border-t">
            <h2 className="text-lg font-semibold mb-4">Required Skills</h2>
            <div className="flex flex-wrap gap-2">
              {job.skill_tags.split(',').map((tag) => (
                <span
                  key={tag}
                  className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full"
                >
                  {tag.trim()}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}