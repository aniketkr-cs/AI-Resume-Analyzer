"""
utils/gemini_client.py
=======================
Handles all communication with the Google Gemini API.
Sends resume + job description, receives structured JSON analysis.

The prompt is carefully engineered to get consistent, parseable JSON back.
"""

import json
import re
import time
from typing import Tuple, Optional
from google import genai
from google.genai import types


# ── Prompt Engineering ────────────────────────────────────────────────────────
ANALYSIS_PROMPT_TEMPLATE = """
You are an expert ATS (Applicant Tracking System) analyzer and career coach.

Analyze the following resume against the provided job description. 
Return ONLY a valid JSON object — no markdown, no explanation, no backticks.

RESUME TEXT:
{resume_text}

JOB DESCRIPTION:
{job_description}
IMPORTANT:

Be deterministic and consistent.

If the same resume and same job description are analyzed multiple times,
return the same matched skills, missing skills, priorities,
ATS summary, and learning roadmap whenever possible.

Do not invent new skills.
Do not randomly reorder skills.
Use only evidence found in the resume and job description.

Return this exact JSON structure:

{{
  "ats_summary": "<2-3 sentence summary of overall match quality>",
  
  "matched_skills": ["skill1", "skill2", ...],
  "missing_skills": ["skill1", "skill2", ...],
  
  "missing_skills_detail": [
    {{
      "skill": "<skill name>",
      "category": "<Technical|Soft Skill|Tool|Domain|Certification>",
      "priority": "<High|Medium|Low>",
      "why_important": "<one sentence explanation>"
    }}
  ],
  
  "strengths": [
    "<strength 1>",
    "<strength 2>",
    "<strength 3>"
  ],
  
  "improvement_suggestions": [
    "<specific, actionable suggestion 1>",
    "<specific, actionable suggestion 2>",
    "<specific, actionable suggestion 3>",
    "<specific, actionable suggestion 4>",
    "<specific, actionable suggestion 5>"
  ],
  
  "learning_roadmap": [
    {{
      "week": 1,
      "topic": "<skill or topic to learn>",
      "goal": "<what you will be able to do after this week>",
      "resources": [
        "<resource 1: course, book, or practice project>",
        "<resource 2>",
        "<resource 3>"
      ]
    }},
    {{
      "week": 2,
      "topic": "<next skill>",
      "goal": "<weekly goal>",
      "resources": ["<resource 1>", "<resource 2>", "<resource 3>"]
    }},
    {{
      "week": 3,
      "topic": "<next skill>",
      "goal": "<weekly goal>",
      "resources": ["<resource 1>", "<resource 2>", "<resource 3>"]
    }},
    {{
      "week": 4,
      "topic": "<next skill>",
      "goal": "<weekly goal>",
      "resources": ["<resource 1>", "<resource 2>", "<resource 3>"]
    }},
    {{
      "week": 5,
      "topic": "<next skill>",
      "goal": "<weekly goal>",
      "resources": ["<resource 1>", "<resource 2>", "<resource 3>"]
    }},
    {{
      "week": 6,
      "topic": "<next skill>",
      "goal": "<weekly goal>",
      "resources": ["<resource 1>", "<resource 2>", "<resource 3>"]
    }},
    {{
      "week": 7,
      "topic": "<next skill>",
      "goal": "<weekly goal>",
      "resources": ["<resource 1>", "<resource 2>", "<resource 3>"]
    }},
    {{
      "week": 8,
      "topic": "Portfolio & Application Prep",
      "goal": "Build a project showcasing newly learned skills and update resume",
      "resources": [
        "Build a GitHub portfolio project using the skills learned",
        "Update resume with new skills and certifications",
        "Practice behavioral + technical interview questions"
      ]
    }}
  ]
}}
Base the learning roadmap on the missing skills, prioritizing High-priority skills first.
Be specific and actionable. Mention real courses (Coursera, Udemy, YouTube, docs), not vague advice.
Return ONLY the JSON. No other text.
"""


def analyze_resume(
    resume_text: str,
    job_description: str,
    api_key: str,
    max_retries: int = 2,
) -> Tuple[Optional[dict], Optional[str]]:
    """
    Send resume and job description to Gemini for analysis.

    Args:
        resume_text:     Extracted text from the PDF resume
        job_description: Job description pasted by the user
        api_key:         Google Gemini API key
        max_retries:     Number of retry attempts on failure

    Returns:
        Tuple of (analysis_dict, error_message)
        On success: (dict_with_results, None)
        On failure: (None, error_string)
    """
    # Trim inputs to avoid hitting token limits
    resume_trimmed = resume_text[:6000] if len(resume_text) > 6000 else resume_text
    jd_trimmed     = job_description[:3000] if len(job_description) > 3000 else job_description

    # Build the full prompt
    prompt = ANALYSIS_PROMPT_TEMPLATE.format(
        resume_text=resume_trimmed,
        job_description=jd_trimmed,
    )

    # Initialize the new google-genai client
    client = genai.Client(api_key=api_key)

    # Retry loop (handles transient API errors)
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                    max_output_tokens=8192,
                ),
            )
            raw_text = response.text

            # Parse the JSON response
            raw_text = response.text

            if raw_text is None:
             raise ValueError("Gemini returned an empty response.")
            analysis = parse_gemini_response(raw_text)
            return analysis, None

        except json.JSONDecodeError as e:
            last_error = f"AI returned invalid JSON (attempt {attempt+1}): {e}"
            if attempt < max_retries:
                time.sleep(1)  # Brief pause before retry

        except Exception as e:
            error_str = str(e)

            # Handle specific API errors with friendly messages
            if "API_KEY_INVALID" in error_str or "API key not valid" in error_str:
                return None, "Invalid Gemini API key. Please check your .env file."
            elif "QUOTA_EXCEEDED" in error_str or "quota" in error_str.lower():
                return None, "Gemini API quota exceeded. Please wait or upgrade your plan."
            elif "SAFETY" in error_str:
                return None, "Content was flagged by safety filters. Please check your inputs."
            elif "404" in error_str and "model" in error_str.lower():
                return None, "Gemini model not available. Try updating the model name in gemini_client.py."
            else:
                last_error = f"API error (attempt {attempt+1}): {error_str}"
                if attempt < max_retries:
                    time.sleep(2)

    return None, last_error or "Analysis failed after all retries."


def parse_gemini_response(raw_text: str) -> dict:
    """
    Parse the JSON from Gemini's response.

    Gemini sometimes wraps JSON in markdown code blocks (```json ... ```),
    so we strip those before parsing. Also validates required fields.

    Args:
        raw_text: Raw string from Gemini API response

    Returns:
        Parsed dict with analysis results

    Raises:
        json.JSONDecodeError: If the response isn't valid JSON after cleanup
        ValueError: If required fields are missing
    """
    # Strip markdown code block wrappers if present
    text = raw_text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)
    text = text.strip()

    # Sometimes models add a preamble before the JSON
    # Find the first '{' to start parsing from there
    first_brace = text.find('{')
    if first_brace > 0:
        text = text[first_brace:]

    # Parse JSON
    data = json.loads(text)

    # Validate and normalize required fields with safe defaults
    data.setdefault("ats_score", 0)
    data.setdefault("ats_summary", "Analysis complete.")
    data.setdefault("matched_skills", [])
    data.setdefault("missing_skills", [])
    data.setdefault("missing_skills_detail", [])
    data.setdefault("strengths", [])
    data.setdefault("improvement_suggestions", [])
    data.setdefault("learning_roadmap", [])

    # Ensure ATS score is an integer in valid range
    try:
        data["ats_score"] = max(0, min(100, int(data["ats_score"])))
    except (TypeError, ValueError):
        data["ats_score"] = 0

    # Ensure all list fields are actually lists
    for field in ["matched_skills", "missing_skills", "strengths", "improvement_suggestions"]:
        if not isinstance(data[field], list):
            data[field] = []

    return data
