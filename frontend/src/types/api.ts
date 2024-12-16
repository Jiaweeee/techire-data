// API Response Types
import { EmploymentType } from "./employment";
import { SalaryPeriod } from "./salary";

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

export interface SalaryRange {
  min?: number;
  max?: number;
  fixed?: number;
  currency?: string;
  period?: SalaryPeriod;
  is_estimated?: boolean;
}

export interface JobBrief {
  id: string;
  url: string;
  title: string;
  company: CompanyBrief;
  locations: string[];
  employment_type: EmploymentType | null;
  posted_date: string | null;
  is_remote: boolean | null;
  salary_range: SalaryRange | null;
  experience_level: number | null;
  skill_tags: string[] | null;
  summary: string | null;
}

export interface JobDetail extends JobBrief {
  full_description: string;
}

export interface SearchParams {
  q?: string;
  employment_types?: string[];
  experience_levels?: number[];
  company_ids?: string[];
  sort_by?: number;
  is_remote?: boolean;
  location?: string;
  page?: number;
  per_page?: number;
}

export interface SearchResponse {
  results: JobBrief[];
  total: number;
  page: number;
  per_page: number;
}