export enum EmploymentType {
    FULL_TIME = 1,
    PART_TIME = 2,
    CONTRACT = 3,
    INTERNSHIP = 4,
    TEMPORARY = 5,
    REMOTE = 6,
    HYBRID = 7,
    ON_SITE = 8
}

export function getEmploymentTypeLabel(type: EmploymentType | null): string {
    if (!type) return '';
    
    switch (type) {
        case EmploymentType.FULL_TIME:
            return 'Full-Time';
        case EmploymentType.PART_TIME:
            return 'Part-Time';
        case EmploymentType.CONTRACT:
            return 'Contract';
        case EmploymentType.INTERNSHIP:
            return 'Internship';
        case EmploymentType.TEMPORARY:
            return 'Temporary';
        case EmploymentType.REMOTE:
            return 'Remote';
        case EmploymentType.HYBRID:
            return 'Hybrid';
        case EmploymentType.ON_SITE:
            return 'On-site';
        default:
            return '';
    }
} 