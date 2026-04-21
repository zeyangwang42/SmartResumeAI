import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import build_resume_analysis_prompt, build_resume_rewrite_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_resume_against_jd(resume_text: str, job_description: str) -> str:
    prompt = build_resume_analysis_prompt(resume_text, job_description)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text


def generate_tailored_resume(resume_text: str, job_description: str) -> str:
    prompt = build_resume_rewrite_prompt(resume_text, job_description)

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text