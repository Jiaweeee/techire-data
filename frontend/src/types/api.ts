// API Response Types
import { EmploymentType } from "./employment";

export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface HTTPValidationError {
  detail: ValidationError[];
}

export interface CompanyBrief {
  id: string;
  name: string;
  icon_url: string;
}

export interface CompanyDetail extends CompanyBrief {
  code: string;
  official_site_url: string;
  careers_page_url: string;
  introduction: string;
  industry: string | null;
  headquarters: string | null;
}

export interface JobDetail {
  id: string;
  url: string;
  title: string;
  company: CompanyBrief;
  location: string;
  employment_type: EmploymentType | null;
  posted_date: string | null;
  salary_range: string | null;
  is_remote: boolean | null;
  full_description: string;
  skill_tags: string | null;
}

export interface SearchParams {
  q?: string;
  posted_after?: string;
  is_remote?: boolean;
  page?: number;
  per_page?: number;
  company_ids?: string[];
  employment_types?: string[];
}

export interface SearchResponse {
  results: JobDetail[];
  total: number;
  page: number;
  per_page: number;
}