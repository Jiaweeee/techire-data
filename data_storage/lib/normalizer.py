import re
from typing import Optional
from ..models import EmploymentType

class JobDataNormalizer:
    # 工作类型映射字典
    EMPLOYMENT_TYPE_MAPPING = {
        # Full-time variations
        r"full[\s-]?time|full|ft": EmploymentType.FULL_TIME,
        # Part-time variations
        r"part[\s-]?time|pt": EmploymentType.PART_TIME,
        # Contract variations
        r"contract|contractor|consulting": EmploymentType.CONTRACT,
        # Internship variations
        r"internship|intern": EmploymentType.INTERNSHIP,
        # Remote variations
        r"remote|work from home|wfh": EmploymentType.REMOTE,
        # Hybrid variations
        r"hybrid|flexible": EmploymentType.HYBRID,
        # On-site variations
        r"on[\s-]?site|onsite|in[\s-]?office": EmploymentType.ON_SITE,
    }

    @classmethod
    def normalize_employment_type(cls, raw_type: str) -> Optional[EmploymentType]:
        if not raw_type:
            return None
            
        raw_type = raw_type.lower().strip()
        for pattern, normalized_type in cls.EMPLOYMENT_TYPE_MAPPING.items():
            if re.search(pattern, raw_type):
                return normalized_type
        return None
