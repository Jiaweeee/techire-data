import { formatSalary } from './salary';
import { SalaryRange } from '../types/api';
import { SalaryPeriod } from '../types/salary';
import { describe, it, expect } from '@jest/globals';

describe('formatSalary', () => {
  it('should return Unknown when salary range is null', () => {
    expect(formatSalary(null)).toBe('Unknown');
  });

  it('should format fixed salary correctly', () => {
    const salary: SalaryRange = {
      fixed: 5000,
      currency: 'USD',
      period: SalaryPeriod.MONTH
    };
    expect(formatSalary(salary)).toBe('USD 5K/month');
  });

  it('should format salary range correctly', () => {
    const salary: SalaryRange = {
      min: 80000,
      max: 120000,
      currency: 'USD',
      period: SalaryPeriod.YEAR
    };
    expect(formatSalary(salary)).toBe('USD 80K - 120K/year');
  });

  it('should format minimum salary correctly', () => {
    const salary: SalaryRange = {
      min: 10000,
      currency: 'USD',
      period: SalaryPeriod.MONTH
    };
    expect(formatSalary(salary)).toBe('USD 10K+/month');
  });

  it('should format maximum salary correctly', () => {
    const salary: SalaryRange = {
      max: 150000,
      currency: 'USD',
      period: SalaryPeriod.YEAR
    };
    expect(formatSalary(salary)).toBe('Up to USD 150K/year');
  });

  it('should format decimal K values correctly', () => {
    const salary: SalaryRange = {
      fixed: 1500,
      currency: 'USD',
      period: SalaryPeriod.MONTH
    };
    expect(formatSalary(salary)).toBe('USD 1.5K/month');
  });

  it('should not use K for values less than 1000', () => {
    const salary: SalaryRange = {
      fixed: 999,
      currency: 'USD',
      period: SalaryPeriod.MONTH
    };
    expect(formatSalary(salary)).toBe('USD 999/month');
  });
});