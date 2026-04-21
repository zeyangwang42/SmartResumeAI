def build_resume_analysis_prompt(resume_text: str, job_description: str) -> str:
    return f"""
You are an expert resume reviewer and career assistant.

Analyze the resume against the job description.

Return your answer in the exact structure below:

Match Score:
- A number from 0 to 100
- A 1-2 sentence explanation

Strengths:
- 3 to 5 bullet points showing what matches well

Missing Skills / Gaps:
- 3 to 8 bullet points listing important missing skills, keywords, or experiences

Improvement Suggestions:
- 3 to 6 bullet points with practical suggestions to improve the resume for this role

Rewritten Resume Bullets:
- Rewrite 3 to 5 resume bullet points to better align with the job description
- Keep them realistic
- Use concise professional resume language
- Do not invent experiences that are not supported by the resume

Resume:
{resume_text}

Job Description:
{job_description}
"""


def build_resume_rewrite_prompt(resume_text: str, job_description: str) -> str:
    return f"""
You are an expert resume writer.

Using the original resume and the target job description, generate a tailored one-page style resume draft.

Rules:
- Keep the content realistic
- Do not invent degrees, jobs, dates, or certifications not supported by the original resume
- You may rewrite, reorganize, and improve wording
- Prioritize relevance to the target job description
- Keep the language concise and professional
- Output in the exact structure below
- Output should be a one page resume (Can not be too long)

OUTPUT FORMAT:

NAME
One-line professional headline

CONTACT
Email | Phone | LinkedIn | GitHub | Location

SUMMARY
2-4 lines

SKILLS
- skill category: items

EXPERIENCE
Job Title | Company | Dates
- bullet
- bullet
- bullet

Job Title | Company | Dates
- bullet
- bullet
- bullet

PROJECTS
Project Name
- bullet
- bullet

EDUCATION
Degree | School | Graduation Date

Original Resume:
{resume_text}

Target Job Description:
{job_description}
"""