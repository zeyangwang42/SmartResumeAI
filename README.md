# SmartResume AI

SmartResume AI is a lightweight AI-powered web application that helps users analyze how well their resume matches a target job description and generate a tailored resume draft for that role.

The app supports resume PDF upload, job description matching, AI-generated resume analysis, editable resume sections, and Word document export.

## Features

- Upload a resume in PDF format
- Paste a target job description
- Extract and preview resume text
- Generate resume-to-job match analysis
- Estimate a match score
- Identify strengths and missing skills
- Generate a tailored resume draft
- Edit resume sections directly in the app
- Download the final resume as a Word document

## Demo Workflow

1. Upload a resume PDF
2. Paste a target job description
3. Click **Analyze Match**
4. Review the match score and analysis summary
5. Click **Generate New Resume**
6. Edit the generated resume sections
7. Download the final resume as a `.docx` file

## Tech Stack

- Python
- Streamlit
- OpenAI API
- pdfplumber
- python-docx
- python-dotenv

## Project Structure

```text
smartresume-ai/
├── app.py
├── analyzer.py
├── prompts.py
├── resume_builder.py
├── utils.py
├── requirements.txt
├── .gitignore
├── .env
├── README.md
├── LICENSE
└── assets/
