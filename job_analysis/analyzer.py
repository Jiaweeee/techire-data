from typing import Dict, Any, Optional
from openai import OpenAI
from data_storage.crud import JobAnalysisCRUD
from data_storage.models import Job, ExperienceLevel
import os, json
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class JobAnalyzer:
    """
    Analyze job information using LLM to extract structured data
    """
    def __init__(self):
        self.job_analysis_crud = JobAnalysisCRUD()
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        self.chat_model = os.getenv("CHAT_MODEL")
    
    def analyze(self, job: Job) -> Optional[Dict[str, Any]]:
        prompt = self._create_analysis_prompt(job.title, job.full_description)
        return self._get_llm_analysis(prompt)

    def _create_analysis_prompt(self, title: str, description: str) -> str:
        return f"""Analyze the following job posting and extract key information in JSON format:

        Title: {title}
        Description: {description}

        Please extract and return a JSON object with the following structure:
        {{
            "salary_min": number or null,      // Minimum salary amount
            "salary_max": number or null,      // Maximum salary amount
            "salary_fixed": number or null,    // Fixed/exact salary amount
            "salary_currency": string or null, // Currency code (e.g., "USD", "EUR", "GBP")
            "skill_tags": [                    // List of 3-7 MOST important required skills
                string,                        // Focus on core technical skills and key technologies
                ...                           // e.g., ["Python", "AWS", "React"]
            ],
            "experience_level": string,        // One of: "ENTRY", "MID", "SENIOR", "LEAD", "EXECUTIVE"
            "summary": string                  // 2-3 concise sentences summarizing key responsibilities
        }}

        Guidelines:
        - Extract only numerical values for salary fields
        - Include currency code in standard format (USD, EUR, etc.)
        - List ONLY the 3-7 most critical skills or technologies that are essential for the role
        - For skill_tags, prioritize technical skills and core technologies over soft skills
        - Determine experience level based on requirements and responsibilities
        - Keep summary focused and concise

        Return only the JSON object, no additional text."""

    def _get_llm_analysis(self, prompt: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are a job analysis assistant. Extract structured information from job postings."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
            )
            # 解析响应
            result = json.loads(response.choices[0].message.content)
            logger.info(f"LLM analysis result: {result}")
            level_str = result.get('experience_level')
            if level_str:
                result['experience_level'] = ExperienceLevel[level_str.upper()]
            return {
                'salary_min': result.get('salary_min'),
                'salary_max': result.get('salary_max'),
                'salary_fixed': result.get('salary_fixed'),
                'salary_currency': result.get('salary_currency'),
                'skill_tags': result.get('skill_tags', []),
                'experience_level': result.get('experience_level'),
                'summary': result.get('summary')
            }
        except Exception as e:
            print(f"Error in LLM analysis: {str(e)}")
            return None
