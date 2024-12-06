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

export interface JobBrief {
  id: string;
  url: string;
  title: string;
  company: CompanyBrief;
  location: string;
  employment_type: EmploymentType | null;
  posted_date: string | null;
  is_remote: boolean | null;
  salary_range: {
    min?: number;
    max?: number;
    fixed?: number;
    currency?: string;
  } | null;
  experience_level: number | null;
  skill_tags: string[] | null;
  summary: string | null;
}

export interface JobDetail extends JobBrief {
  full_description: string;
}

export interface SearchParams {
  q?: string;
  location?: string;
  employment_type?: string;
  is_remote?: boolean;
  company_ids?: string[];
  page?: number;
  per_page?: number;
}

export interface SearchResponse {
  results: JobBrief[];
  total: number;
  page: number;
  per_page: number;
}