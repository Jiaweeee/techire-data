JOB_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "title": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "full_description": {
                "type": "text",
                "analyzer": "standard"
            },
            "company": {
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    }
                }
            },
            "skill_tags": {
                "type": "text",
                "fields": {
                    "keyword": {"type": "keyword"}
                }
            },
            "location": {"type": "text"},
            "employment_type": {"type": "keyword"},
            "posted_date": {
                "type": "date",
                "format": "strict_date_optional_time||date_optional_time"
            },
            "is_remote": {"type": "boolean"},
            "expired": {"type": "boolean"}
        }
    }
} 