export enum ExperienceLevel {
    ENTRY = 1,
    MID = 2,
    SENIOR = 3,
    LEAD = 4,
    EXECUTIVE = 5
}

export function getExperienceLevelLabel(level: ExperienceLevel | null): string {
    if (!level) return '';
    
    switch (level) {
        case ExperienceLevel.ENTRY:
            return 'Entry-Level';
        case ExperienceLevel.MID:
            return 'Mid';
        case ExperienceLevel.SENIOR:
            return 'Senior';
        case ExperienceLevel.LEAD:
            return 'Lead';
        case ExperienceLevel.EXECUTIVE:
            return 'Executive';
        default:
            return '';
    }
} 