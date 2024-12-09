import { SearchParams, SearchResponse, JobDetail } from '../types/api';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export async function searchJobs(params: SearchParams): Promise<SearchResponse> {
  const response = await fetch(`${API_BASE_URL}/jobs/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      q: params.q,
      employment_types: params.employment_types,
      experience_levels: params.experience_levels,
      company_ids: params.company_ids,
      sort_by: params.sort_by,
      is_remote: params.is_remote,
      location: params.location,
      page: params.page || 1,
      per_page: params.per_page || 10,
    }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch jobs');
  }
  
  return response.json();
}

export async function getJobDetail(jobId: string): Promise<JobDetail> {
  const response = await fetch(`${API_BASE_URL}/jobs/detail?job_id=${jobId}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch job details');
  }
  
  return response.json();
}