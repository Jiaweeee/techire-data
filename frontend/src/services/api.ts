import {
    SearchParams,
    SearchResponse,
    JobDetail,
    CompanyBrief,
    StatsResponse
} from '../types/api';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const searchJobs = async (params: SearchParams): Promise<SearchResponse> => {
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
      locations: params.locations,
      sort_by: params.sort_by,
      is_remote: params.is_remote,
      min_annual_salary: params.min_annual_salary,
      page: params.page || 1,
      per_page: params.per_page || 10,
    }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch jobs');
  }
  
  return response.json();
}

export const getJobDetail = async (jobId: string): Promise<JobDetail> => {
  const response = await fetch(`${API_BASE_URL}/jobs/detail?job_id=${jobId}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch job details');
  }
  
  return response.json();
}

// export const searchCompanies = async (query: string): Promise<CompanyBrief[]> => {
//   const response = await fetch(`${API_BASE_URL}/companies/search?q=${encodeURIComponent(query)}`);
  
//   if (!response.ok) {
//     throw new Error('Failed to fetch companies');
//   }
  
//   return response.json();
// }

export async function getCompanies(): Promise<CompanyBrief[]> {
  const response = await fetch(`${API_BASE_URL}/companies/list`);
  if (!response.ok) {
    throw new Error('Failed to fetch companies');
  }
  return response.json();
}

export const getStats = async (): Promise<StatsResponse> => {
  const response = await fetch(`${API_BASE_URL}/stats/summary`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch stats');
  }
  
  return response.json();
}

export async function getLocations(): Promise<string[]> {
    const response = await fetch(`${API_BASE_URL}/jobs/locations`);
    if (!response.ok) throw new Error('Failed to fetch locations');
    return response.json();
  }