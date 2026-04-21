import streamlit as st
from analyzer import analyze_resume_against_jd, generate_tailored_resume
from resume_builder import (
    build_resume_docx_from_sections,
    extract_match_summary,
    parse_generated_resume_sections,
    parse_match_score,
    score_label,
)
from utils import extract_text_from_pdf, clean_text

st.set_page_config(
    page_title="SmartResume AI",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main > div {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 28px 32px;
        border-radius: 20px;
        color: white;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #dbeafe;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    .pill-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 8px;
    }

    .pill {
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.15);
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 0.88rem;
        color: #f8fafc;
    }

    .section-label {
        font-size: 0.95rem;
        font-weight: 700;
        margin-top: 0.3rem;
        margin-bottom: 0.65rem;
        color: #0f172a;
    }

    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        color: #111827;
    }

    .card-subtitle {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 0.75rem;
    }

    .empty-box {
        height: 420px;
        border: 1px dashed #cbd5e1;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        background: #f8fafc;
        color: #64748b;
        padding: 24px;
    }

    .empty-box h4 {
        margin: 0 0 8px 0;
        color: #334155;
        font-size: 1.05rem;
    }

    .small-note {
        color: #64748b;
        font-size: 0.88rem;
        margin-top: 0.35rem;
    }

    .result-header {
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0.4rem 0 0.8rem 0;
        color: #0f172a;
    }

    .score-card {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
        border: 1px solid #dbeafe;
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 14px;
    }

    .score-label {
        font-size: 0.9rem;
        color: #475569;
        margin-bottom: 8px;
        font-weight: 600;
    }

    .score-badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
        background: #e0e7ff;
        color: #3730a3;
        margin-top: 6px;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 14px !important;
        padding: 14px !important;
        font-size: 0.94rem !important;
        line-height: 1.5 !important;
    }

    div[data-testid="stFileUploader"] section {
        border-radius: 14px !important;
    }

    div.stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding-top: 0.6rem !important;
        padding-bottom: 0.6rem !important;
    }

    div[data-testid="stDownloadButton"] > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding-top: 0.65rem !important;
        padding-bottom: 0.65rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

default_state = {
    "analysis_result": "",
    "generated_resume": "",
    "resume_name": "",
    "resume_headline": "",
    "resume_contact": "",
    "resume_summary": "",
    "resume_skills": "",
    "resume_experience": "",
    "resume_projects": "",
    "resume_education": "",
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value


def load_generated_resume_into_editor(generated_text: str):
    sections = parse_generated_resume_sections(generated_text)
    st.session_state.resume_name = sections["name"]
    st.session_state.resume_headline = sections["headline"]
    st.session_state.resume_contact = sections["contact"]
    st.session_state.resume_summary = sections["summary"]
    st.session_state.resume_skills = sections["skills"]
    st.session_state.resume_experience = sections["experience"]
    st.session_state.resume_projects = sections["projects"]
    st.session_state.resume_education = sections["education"]


st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">SmartResume AI</div>
        <div class="hero-subtitle">
            Upload your resume, paste a target job description, analyze the fit, and generate a stronger tailored resume draft.
        </div>
        <div class="pill-row">
            <div class="pill">Resume Match Analysis</div>
            <div class="pill">Skill Gap Detection</div>
            <div class="pill">Editable Resume Builder</div>
            <div class="pill">Word Download</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">INPUT</div>', unsafe_allow_html=True)

input_col1, input_col2 = st.columns([1, 1], gap="large")

with input_col1:
    with st.container(border=True):
        st.markdown('<div class="card-title">Upload Resume</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-subtitle">Upload a PDF resume to extract and analyze its content.</div>',
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF)",
            type=["pdf"],
            label_visibility="collapsed",
        )

with input_col2:
    with st.container(border=True):
        st.markdown('<div class="card-title">Paste Job Description</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-subtitle">Paste the target role description you want to match.</div>',
            unsafe_allow_html=True,
        )
        job_description = st.text_area(
            "Paste Job Description",
            height=180,
            placeholder="Paste the target job description here...",
            label_visibility="collapsed",
        )

resume_text = ""

if uploaded_file is not None:
    try:
        resume_text = extract_text_from_pdf(uploaded_file)
        resume_text = clean_text(resume_text)
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")

st.markdown("")
st.markdown('<div class="section-label">PREVIEW</div>', unsafe_allow_html=True)

preview_col1, preview_col2 = st.columns(2, gap="large")

with preview_col1:
    with st.container(border=True):
        st.markdown('<div class="card-title">Resume Preview</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-subtitle">Extracted text from the uploaded resume PDF.</div>',
            unsafe_allow_html=True,
        )

        if resume_text:
            st.text_area(
                "Resume Content",
                value=resume_text,
                height=420,
                label_visibility="collapsed",
                key="resume_preview",
            )
        else:
            st.markdown(
                """
                <div class="empty-box">
                    <div>
                        <h4>No resume uploaded yet</h4>
                        <div>Upload a PDF resume and the extracted content will appear here.</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

with preview_col2:
    with st.container(border=True):
        st.markdown('<div class="card-title">Job Description Preview</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="card-subtitle">Your target role content for matching and rewriting.</div>',
            unsafe_allow_html=True,
        )

        if job_description.strip():
            st.text_area(
                "JD Content",
                value=job_description,
                height=420,
                label_visibility="collapsed",
                key="jd_preview",
            )
        else:
            st.markdown(
                """
                <div class="empty-box">
                    <div>
                        <h4>No job description yet</h4>
                        <div>Paste a job description and it will appear here for review.</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("")
st.markdown('<div class="section-label">ACTIONS</div>', unsafe_allow_html=True)

action_col1, action_col2, action_col3 = st.columns([1.2, 1.2, 3.6], gap="medium")

with action_col1:
    analyze_clicked = st.button("Analyze Match", use_container_width=True)

with action_col2:
    generate_clicked = st.button("Generate New Resume", use_container_width=True)

with action_col3:
    st.markdown(
        '<div class="small-note">Tip: analyze first, then generate a tailored resume draft and fine-tune it in the editor below.</div>',
        unsafe_allow_html=True,
    )

if analyze_clicked:
    if not resume_text:
        st.warning("Please upload a valid resume PDF first.")
    elif not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        with st.spinner("Analyzing resume against the job description..."):
            try:
                st.session_state.analysis_result = analyze_resume_against_jd(
                    resume_text, job_description
                )
            except Exception as e:
                st.error(f"Analysis failed: {e}")

if generate_clicked:
    if not resume_text:
        st.warning("Please upload a valid resume PDF first.")
    elif not job_description.strip():
        st.warning("Please paste a job description.")
    else:
        with st.spinner("Generating a tailored resume draft..."):
            try:
                generated = generate_tailored_resume(resume_text, job_description)
                st.session_state.generated_resume = generated
                load_generated_resume_into_editor(generated)
            except Exception as e:
                st.error(f"Resume generation failed: {e}")

if st.session_state.analysis_result or st.session_state.generated_resume:
    st.markdown("")
    st.divider()
    st.markdown('<div class="result-header">Results</div>', unsafe_allow_html=True)

result_col1, result_col2 = st.columns([0.9, 1.6], gap="large")

with result_col1:
    if st.session_state.analysis_result:
        score = parse_match_score(st.session_state.analysis_result)
        summary = extract_match_summary(st.session_state.analysis_result)
        label = score_label(score)

        with st.container(border=True):
            st.markdown('<div class="card-title">Match Score</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="card-subtitle">A quick overview of how well the current resume matches the target role.</div>',
                unsafe_allow_html=True,
            )

            st.markdown('<div class="score-card">', unsafe_allow_html=True)
            st.metric("Resume Match", f"{score}/100")
            st.markdown(f'<div class="score-badge">{label}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("**Summary**")
            st.write(summary)

            with st.expander("View full analysis", expanded=True):
                st.markdown(st.session_state.analysis_result)

with result_col2:
    if st.session_state.generated_resume:
        with st.container(border=True):
            st.markdown('<div class="card-title">Editable Resume Builder</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="card-subtitle">Edit the generated draft before downloading the final Word document.</div>',
                unsafe_allow_html=True,
            )

            top_col1, top_col2 = st.columns([1.2, 1.2], gap="medium")

            with top_col1:
                st.text_input("Name", key="resume_name")
            with top_col2:
                st.text_input("Professional Headline", key="resume_headline")

            st.text_input("Contact", key="resume_contact")

            st.text_area("Summary", key="resume_summary", height=120)
            st.text_area("Skills", key="resume_skills", height=140)
            st.text_area("Experience", key="resume_experience", height=220)
            st.text_area("Projects", key="resume_projects", height=140)
            st.text_area("Education", key="resume_education", height=100)

            edited_sections = {
                "name": st.session_state.resume_name,
                "headline": st.session_state.resume_headline,
                "contact": st.session_state.resume_contact,
                "summary": st.session_state.resume_summary,
                "skills": st.session_state.resume_skills,
                "experience": st.session_state.resume_experience,
                "projects": st.session_state.resume_projects,
                "education": st.session_state.resume_education,
            }

            resume_docx = build_resume_docx_from_sections(edited_sections)

            st.download_button(
                label="Download Edited Resume as Word (.docx)",
                data=resume_docx,
                file_name="tailored_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )