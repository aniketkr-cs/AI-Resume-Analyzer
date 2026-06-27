"""
AI Resume Analyzer - Main Application
======================================
A production-ready Streamlit app that analyzes resumes against job descriptions
using the Gemini AI API. Provides ATS scoring, skill matching, and improvement tips.

Author: Student AI Engineer Project
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ── Page configuration (must be first Streamlit call) ──────────────────────
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Import project modules ──────────────────────────────────────────────────
from utils.pdf_reader import extract_text_from_pdf
from utils.gemini_client import analyze_resume
from utils.report_generator import generate_pdf_report
from components.charts import (
    render_ats_gauge,
    render_skill_radar,
    render_skill_match_bar,
    render_missing_skills_table,
)
from components.styles import inject_styles
from utils.ats_scoring import calculate_ats_score

# ── Inject custom CSS ───────────────────────────────────────────────────────
inject_styles()


# ══════════════════════════════════════════════════════════════════════════════
# HEADER SECTION
# ══════════════════════════════════════════════════════════════════════════════
def render_header():
    st.markdown("""
    <div class="app-header">
        <div class="header-badge">AI-POWERED TOOL</div>
        <h1 class="app-title">Resume Analyzer</h1>
        <p class="app-subtitle">
            Upload your resume · Paste a job description · Get actionable insights
        </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# INPUT SECTION
# ══════════════════════════════════════════════════════════════════════════════
def render_inputs():
    """Render the resume upload and job description input fields."""
    st.markdown('<div class="section-label">01 — INPUT</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<p class="field-label">📄 Upload Resume (PDF)</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            label="Upload Resume",
            type=["pdf"],
            label_visibility="collapsed",
            help="Upload your resume in PDF format. Max 10MB."
        )
        if uploaded_file:
            st.markdown(f"""
            <div class="file-chip">
                <span class="chip-icon">✓</span>
                <span>{uploaded_file.name}</span>
                <span class="chip-size">{uploaded_file.size // 1024} KB</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown('<p class="field-label">💼 Job Description</p>', unsafe_allow_html=True)
        job_description = st.text_area(
            label="Job Description",
            placeholder="Paste the full job description here...\n\nInclude:\n• Required skills\n• Responsibilities\n• Qualifications",
            height=160,
            label_visibility="collapsed",
        )

    return uploaded_file, job_description


# ══════════════════════════════════════════════════════════════════════════════
# RESULTS DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def render_results(analysis: dict, resume_text: str, job_description: str):
    """Render the full analysis results dashboard."""

    st.markdown("---")
    st.markdown('<div class="section-label">02 — ANALYSIS RESULTS</div>', unsafe_allow_html=True)

    # ── ATS Score Banner ────────────────────────────────────────────────────
    ats_score = calculate_ats_score(analysis)
    score_color = (
    "#22c55e" if ats_score >= 70
    else "#f59e0b" if ats_score >= 50
    else "#ef4444"
    )

    score_label = (
    "Strong Match" if ats_score >= 70
    else "Moderate Match" if ats_score >= 50
    else "Needs Work"
    )
    left_col, right_col = st.columns([1, 2], gap="large")

    
    with left_col:
      st.markdown(f"""
      <div class="ats-left-card">
        <div class="ats-label">ATS COMPATIBILITY SCORE</div>
        <div class="ats-score" style="color:{score_color};">
            {ats_score}<span class="ats-percent">%</span>
        </div>
        <div class="ats-status"
            style="background:{score_color}18;
                   color:{score_color};
                   border:1px solid {score_color}35;">
            {score_label}
        </div>
    </div>
       """, unsafe_allow_html=True)

    with right_col:
      st.markdown(f"""
      <div class="ats-summary-card">
        <div class="ats-summary-label">SUMMARY</div>
        <p class="ats-desc">
            {analysis.get("ats_summary", "Analysis complete.")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Charts Row ──────────────────────────────────────────────────────────
    st.markdown("### 📊 Visual Analysis")
    chart_col1, chart_col2, chart_col3 = st.columns([1, 1.2, 0.8], gap="medium")

    with chart_col1:
        render_ats_gauge(ats_score)

    with chart_col2:
        matched = analysis.get("matched_skills", [])
        missing = analysis.get("missing_skills", [])
        render_skill_radar(matched, missing)

    with chart_col3:
        render_skill_match_bar(matched, missing)

    st.markdown("---")

    # ── Skill Columns ───────────────────────────────────────────────────────
    st.markdown("### 🧩 Skill Breakdown")
    skill_col1, skill_col2 = st.columns(2, gap="large")

    with skill_col1:
        st.markdown('<div class="skill-box-header matched-header">✅ Matched Skills</div>', unsafe_allow_html=True)
        if matched:
            for skill in matched:
                st.markdown(f'<span class="skill-tag matched-tag">{skill}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="empty-state">No matched skills found.</p>', unsafe_allow_html=True)

    with skill_col2:
        st.markdown('<div class="skill-box-header missing-header">❌ Missing Skills</div>', unsafe_allow_html=True)
        if missing:
            for skill in missing:
                st.markdown(f'<span class="skill-tag missing-tag">{skill}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="empty-state">No critical gaps found!</p>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Missing Skills Table ────────────────────────────────────────────────
    if missing:
        st.markdown("### 📋 Missing Skills — Priority Table")
        render_missing_skills_table(analysis.get("missing_skills_detail", []))
        st.markdown("---")

    # ── Strengths ───────────────────────────────────────────────────────────
    st.markdown("### 💪 Resume Strengths")
    strengths = analysis.get("strengths", [])
    s_cols = st.columns(min(len(strengths), 3)) if strengths else [st.container()]
    for i, strength in enumerate(strengths):
        with s_cols[i % 3]:
            st.markdown(f"""
            <div class="strength-card">
                <div class="strength-icon">⚡</div>
                <p>{strength}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Improvement Suggestions ─────────────────────────────────────────────
    st.markdown("### 🛠 Improvement Suggestions")
    suggestions = analysis.get("improvement_suggestions", [])
    for i, suggestion in enumerate(suggestions, 1):
        st.markdown(f"""
        <div class="suggestion-item">
            <span class="suggestion-num">{i:02d}</span>
            <p>{suggestion}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Learning Roadmap ────────────────────────────────────────────────────
    st.markdown("### 🗺 Personalized Learning Roadmap")
    st.markdown('<p class="roadmap-subtitle">Based on your missing skills, here is a structured 8-week learning plan.</p>', unsafe_allow_html=True)

    roadmap = analysis.get("learning_roadmap", [])
    for week_data in roadmap:
        week_num = week_data.get("week", "")
        topic = week_data.get("topic", "")
        resources = week_data.get("resources", [])
        goal = week_data.get("goal", "")

        with st.expander(f"Week {week_num} — {topic}", expanded=(week_num == 1)):
            st.markdown(f'<p class="week-goal">🎯 Goal: {goal}</p>', unsafe_allow_html=True)
            if resources:
                st.markdown("**Resources:**")
                for r in resources:
                    st.markdown(f"- {r}")

    st.markdown("---")

    # ── Download Report ─────────────────────────────────────────────────────
    st.markdown("### 📥 Download Analysis Report")
    dl_col1, dl_col2, dl_col3 = st.columns([1, 1, 2])

    with dl_col1:
        try:
            pdf_bytes = generate_pdf_report(analysis, resume_text, job_description)
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name="resume_analysis_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Could not generate PDF: {e}")

    with dl_col2:
        import json
        json_data = json.dumps(analysis, indent=2)
        st.download_button(
            label="⬇️ Download JSON Data",
            data=json_data,
            file_name="resume_analysis_data.json",
            mime="application/json",
            use_container_width=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION FLOW
# ══════════════════════════════════════════════════════════════════════════════
def main():
    render_header()

    # ── API Key Check ───────────────────────────────────────────────────────
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error(
            "⚠️ **Gemini API key not found.** "
            "Please add `GEMINI_API_KEY=your_key` to your `.env` file and restart the app."
        )
        st.info("Get your free API key at: https://aistudio.google.com/app/apikey")
        st.stop()

    # ── Inputs ──────────────────────────────────────────────────────────────
    uploaded_file, job_description = render_inputs()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Analyze Button ──────────────────────────────────────────────────────
    _, btn_col, _ = st.columns([2, 1, 2])
    with btn_col:
        analyze_btn = st.button(
            "🔍 Analyze Resume",
            use_container_width=True,
            type="primary",
        )

    # ── Validation & Processing ─────────────────────────────────────────────
    if analyze_btn:
        # Validate inputs
        if not uploaded_file:
            st.warning("⚠️ Please upload a PDF resume before analyzing.")
            st.stop()
        if not job_description or len(job_description.strip()) < 50:
            st.warning("⚠️ Please paste a more detailed job description (at least 50 characters).")
            st.stop()

        # Extract PDF text
        with st.spinner("📄 Extracting text from resume..."):
            resume_text, error = extract_text_from_pdf(uploaded_file)

        if error:
            st.error(f"❌ Failed to read PDF: {error}")
            st.stop()

        if not resume_text or len(resume_text.strip()) < 100:
            st.error("❌ The PDF appears to be empty or image-only. Please use a text-based PDF.")
            st.stop()

        # Run AI analysis
        with st.spinner("🤖 Running AI analysis with Gemini... This may take 10–20 seconds."):
            analysis, error = analyze_resume(resume_text, job_description, api_key)

        if error:
            st.error(f"❌ AI analysis failed: {error}")
            st.info("Check your API key and ensure you have quota remaining.")
            st.stop()

        # Store results in session state so they persist across reruns
        st.session_state["analysis"] = analysis
        st.session_state["resume_text"] = resume_text
        st.session_state["job_description"] = job_description
        st.success("✅ Analysis complete!")

    # ── Render Results if available ─────────────────────────────────────────
    if "analysis" in st.session_state:
        render_results(
            st.session_state["analysis"],
            st.session_state["resume_text"],
            st.session_state["job_description"],
        )

    # ── Footer ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="app-footer">
        Built with Streamlit + Gemini AI · Resume Analyzer v1.0 · Student Portfolio Project
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
