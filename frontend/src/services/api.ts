import { SearchParams, SearchResponse, JobDetail } from '../types/api';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export async function searchJobs(params: SearchParams): Promise<SearchResponse> {
  const searchParams = new URLSearchParams();
  
  if (params.q) searchParams.set('q', params.q);
  if (params.posted_after) searchParams.set('posted_after', params.posted_after);
  if (params.is_remote !== undefined) searchParams.set('is_remote', String(params.is_remote));
  if (params.page) searchParams.set('page', String(params.page));
  if (params.per_page) searchParams.set('per_page', String(params.per_page));
  
  const response = await fetch(`${API_BASE_URL}/jobs/search?${searchParams}`);
  
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