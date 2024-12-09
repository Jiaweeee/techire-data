export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  salary: string;
  description: string;
  isRemote: boolean;
  postedAt: string;
}

export interface SearchResponse {
  jobs: Job[];
  total: number;
  page: number;
  perPage: number;
}

export enum JobSortBy {
  RELEVANCE = 0,
  DATE = 1
}