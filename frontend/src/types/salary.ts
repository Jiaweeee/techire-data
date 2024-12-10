export enum SalaryPeriod {
    HOUR = 1,
    DAY = 2,
    WEEK = 3,
    MONTH = 4,
    YEAR = 5
}

export function getSalaryPeriodLabel(period: SalaryPeriod | null): string {
    if (!period) return '';
    
    switch (period) {
        case SalaryPeriod.HOUR:
            return '/hr';
        case SalaryPeriod.DAY:
            return '/day';
        case SalaryPeriod.WEEK:
            return '/week';
        case SalaryPeriod.MONTH:
            return '/month';
        case SalaryPeriod.YEAR:
            return '/year';
        default:
            return '';
    }
} 