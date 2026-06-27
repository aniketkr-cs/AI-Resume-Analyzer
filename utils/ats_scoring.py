"""
utils/ats_scoring.py

Deterministic ATS Scoring Engine
"""

from typing import Dict


def calculate_ats_score(analysis: Dict) -> int:
    """
    Calculate a deterministic ATS score.

    Uses:
    - matched skills
    - missing skills
    - strengths
    - improvement suggestions
    """

    matched = analysis.get("matched_skills", [])
    missing = analysis.get("missing_skills", [])
    strengths = analysis.get("strengths", [])
    suggestions = analysis.get("improvement_suggestions", [])

    score = 40

    # --------------------------
    # Skill Match (40 marks)
    # --------------------------
    total = len(matched) + len(missing)

    if total > 0:
        score += round((len(matched) / total) * 40)

    # --------------------------
    # Resume Strengths (20 marks)
    # --------------------------
    score += min(len(strengths) * 4, 20)

    # --------------------------
    # Improvement Suggestions (20 marks)
    # Fewer suggestions = better score
    # --------------------------
    deduction = min(len(suggestions) * 2, 20)

    score += (20 - deduction)
    print("=" * 40)
    return max(0, min(score, 100))