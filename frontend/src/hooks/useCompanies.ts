import { useState, useCallback } from 'react';
import { CompanyBrief } from '../types/api';

export function useCompanies() {
  const [companies, setCompanies] = useState<CompanyBrief[]>([]);

  const searchCompanies = useCallback(async (query: string) => {
    try {
      const response = await fetch(`/api/v1/companies/search?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      setCompanies(data);
    } catch (error) {
      console.error('Failed to search companies:', error);
      setCompanies([]);
    }
  }, []);

  return { companies, searchCompanies };
} 