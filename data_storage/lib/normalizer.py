import re
from typing import Optional
from ..models import EmploymentType
from datetime import datetime
from dateutil import parser

class EmploymentTypeNormalizer:
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
    def normalize(cls, raw_type: str) -> Optional[EmploymentType]:
        if not raw_type:
            return None
            
        raw_type = raw_type.lower().strip()
        for pattern, normalized_type in cls.EMPLOYMENT_TYPE_MAPPING.items():
            if re.search(pattern, raw_type):
                return normalized_type
        return None

class DateNormalizer:
    @staticmethod
    def normalize(raw_date: str | int | float) -> datetime:
        if not raw_date:
            return None
        
        # 处理时间戳 (毫秒)
        if isinstance(raw_date, (int, float)) or raw_date.isdigit():
            timestamp = float(raw_date)
            # 如果时间戳是毫秒级的，转换为秒级
            if timestamp > 1e11:  # 简单判断是否为毫秒时间戳
                timestamp = timestamp / 1000
            # 转换为datetime并去除毫秒
            dt = datetime.fromtimestamp(timestamp)
            return dt.replace(microsecond=0)
        
        try:
            # 尝试解析日期，并去除毫秒
            dt = parser.isoparse(raw_date)
            return dt.replace(microsecond=0)
        except ValueError:
            pass
        
        # 如果解析失败，尝试其他常见格式
        formats = [
            "%b %d",  # Mar 17
            "%Y-%m-%dT%H:%M:%S",  # 2024-10-21T06:07:00
            "%Y-%m-%d",  # 2024-10-21
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(raw_date, fmt)
            except ValueError:
                continue
        
        # 如果所有格式都无法解析，返回 None
        return None