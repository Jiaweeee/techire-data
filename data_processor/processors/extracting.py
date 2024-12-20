from .base import Processor
from typing import Dict, Any, Optional
from openai import OpenAI
from data_storage.crud import JobAnalysisCRUD
from data_storage.models import Job, ExperienceLevel, SalaryPeriod
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry
import logging
import json
import backoff
from data_processor.config import load_config

load_dotenv()
logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, config: dict):
        self.client = OpenAI(
            api_key=config.get("api_key"),
            base_url=config.get("base_url")
        )
        self.model = config.get("model")
    
    def get_client(self) -> OpenAI:
        return self.client
    
    def get_model(self) -> str:
        return self.model

class InfoExtractingProcessor(Processor):
    def __init__(self, llm_provider: str = 'deepseek'):
        self.job_analysis_crud = JobAnalysisCRUD()
        llm_config = load_config()['llm']['services'][llm_provider]
        openai_service = OpenAIService(llm_config)
        self.client = openai_service.get_client()
        self.chat_model = openai_service.get_model()
        # log llm config info and model
        logger.info(f"LLM config info: {llm_config}")
        logger.info(f"LLM model: {self.chat_model}")

    def process(self, job: Job) -> Optional[Dict[str, Any]]:
        prompt = self._create_analysis_prompt(
            title=job.title, 
            description=job.full_description, 
            company_name=job.company.name, 
            location=job.location
        ) 
        return self._get_llm_analysis(prompt)

    def _create_analysis_prompt(self, title: str, description: str, company_name: str, location: str) -> str:
        return f"""Analyze the following job posting and extract or estimate key information in JSON format:

        Title: {title}
        Description: {description}
        Company Name: {company_name}
        Location: {location}

        Please extract and return a JSON object with the following structure:
        {{
            "salary_min": number or null,      // Minimum salary amount
            "salary_max": number or null,      // Maximum salary amount
            "salary_fixed": number or null,    // Fixed/exact salary amount
            "salary_currency": string or null, // Currency code (e.g., "USD", "EUR", "GBP")
            "salary_period": string or null,   // One of: "HOUR", "DAY", "WEEK", "MONTH", "YEAR"
            "is_salary_estimated": boolean,    // IMPORTANT: Must be true if salary is estimated
            "skill_tags": [                    // List of 3-7 MOST important required skills
                string,                        // Focus on core technical skills and key technologies
                ...                           // e.g., ["Python", "AWS", "React"]
            ],
            "experience_level": string,        // One of: "ENTRY", "MID", "SENIOR", "LEAD", "EXECUTIVE"
            "summary": string                  // 2-3 concise sentences summarizing key responsibilities
        }}

        IMPORTANT SALARY GUIDELINES:
        1. First, carefully search for EXPLICIT salary information in the job description:
           - Look for specific numbers with currency symbols ($, €, £, etc.)
           - Look for phrases like "salary range", "compensation", "pay", etc.
           - Only set is_salary_estimated = false if you find EXPLICIT salary information

        2. If NO EXPLICIT salary information is found:
           - You MUST set is_salary_estimated = true
           - Estimate salary based on:
             * Job title and seniority level
             * Location and local market rates
             * Company size and industry
             * Required skills and experience
           - Use USD for estimates unless location suggests otherwise
           - Provide a reasonable range (min/max) rather than fixed amount

        3. Double check before responding:
           - If you're providing estimated values, verify is_salary_estimated = true
           - If you found explicit salary in the text, verify is_salary_estimated = false

        Return only the JSON object, no additional text."""
    
    @backoff.on_exception(
        backoff.expo,
        (Exception),  # 可以具体指定要处理的异常类型
        max_tries=5,
        max_time=300
    )
    @sleep_and_retry
    @limits(calls=50, period=60)  # 每分钟最多 50 次调用
    def _get_llm_analysis(self, prompt: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.client.chat.completions.create(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are a job analysis assistant. Extract or estimate structured information from job postings."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
            )
            # 解析响应
            result = json.loads(response.choices[0].message.content)
            logger.info(f"LLM analysis result: {result}")
            level_str = result.get('experience_level')
            period_str = result.get('salary_period')
            
            if level_str:
                result['experience_level'] = ExperienceLevel[level_str.upper()]
            if period_str:
                result['salary_period'] = SalaryPeriod[period_str.upper()]
                
            return {
                'salary_min': result.get('salary_min'),
                'salary_max': result.get('salary_max'),
                'salary_fixed': result.get('salary_fixed'),
                'salary_currency': result.get('salary_currency'),
                'salary_period': result.get('salary_period'),
                'is_salary_estimated': result.get('is_salary_estimated', True),  # 默认为 True
                'skill_tags': ', '.join(result.get('skill_tags', [])),
                'experience_level': result.get('experience_level'),
                'summary': result.get('summary')
            }
        except Exception as e:
            logger.error(f"Error in LLM analysis: {str(e)}")
            return None