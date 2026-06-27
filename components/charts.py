"""
components/charts.py
====================
All Plotly chart renderers for the Resume Analyzer dashboard.
Each function renders one chart directly into Streamlit.

UI ONLY changes in this version:
- Updated color palette to match darker bg (#0a0a0a base)
- Removed margin from PLOTLY_LAYOUT_BASE (was causing duplicate keyword error)
- Each chart now sets its own margin explicitly
- Improved chart typography and grid styling
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ── Color palette (aligned with CSS vars in styles.py) ──────────────────────
BG_PRIMARY     = "#0a0a0a"
BG_CARD        = "#161616"
BG_ELEVATED    = "#1e1e1e"
BORDER         = "#222222"
BORDER_ACTIVE  = "#333333"
TEXT_PRIMARY   = "#f2f2f2"
TEXT_SECONDARY = "#8a8a8a"
TEXT_MUTED     = "#444444"
GREEN          = "#22c55e"
RED            = "#ef4444"
AMBER          = "#f59e0b"
BLUE           = "#3b82f6"
PURPLE         = "#a78bfa"

# Base layout — NO margin here (each chart sets its own to avoid conflicts)
PLOTLY_LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=TEXT_SECONDARY),
)


def _score_color(score: int) -> str:
    if score >= 70:
        return GREEN
    elif score >= 50:
        return AMBER
    return RED


# ══════════════════════════════════════════════════════════════════════════════
# 1. ATS GAUGE
# ══════════════════════════════════════════════════════════════════════════════
def render_ats_gauge(ats_score: int):
    """Render a gauge chart for the ATS score."""
    color = _score_color(ats_score)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ats_score,
        title=dict(
            text="ATS Score",
            font=dict(color=TEXT_MUTED, size=11, family="Inter"),
        ),
        number=dict(
            suffix="%",
            font=dict(color=color, size=38, family="Inter"),
        ),
        gauge=dict(
            axis=dict(
                range=[0, 100],
                tickwidth=1,
                tickcolor=BORDER_ACTIVE,
                tickfont=dict(color=TEXT_MUTED, size=9, family="Inter"),
                nticks=6,
            ),
            bar=dict(color=color, thickness=0.7),
            bgcolor=BG_ELEVATED,
            borderwidth=1,
            bordercolor=BORDER_ACTIVE,
            steps=[
                dict(range=[0,  50],  color="rgba(239,68,68,0.06)"),
                dict(range=[50, 70],  color="rgba(245,158,11,0.06)"),
                dict(range=[70, 100], color="rgba(34,197,94,0.06)"),
            ],
            threshold=dict(
                line=dict(color=TEXT_MUTED, width=1),
                thickness=0.55,
                value=70,
            ),
        ),
    ))
    fig.update_layout(
    paper_bgcolor=PLOTLY_LAYOUT_BASE["paper_bgcolor"],
    plot_bgcolor=PLOTLY_LAYOUT_BASE["plot_bgcolor"],
    font=PLOTLY_LAYOUT_BASE["font"],
    height=220,
    margin=dict(l=20, r=20, t=40, b=20),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
# 2. SKILL RADAR CHART
# ══════════════════════════════════════════════════════════════════════════════
def render_skill_radar(matched_skills: list, missing_skills: list):
    """Render a radar chart comparing matched vs missing skills."""

    all_skills = matched_skills[:5] + missing_skills[:4]
    if not all_skills:
        st.caption("No skills data for radar chart.")
        return

    categories = all_skills[:8]
    matched_vals = [1 if s in matched_skills else 0 for s in categories]
    missing_vals = [1 if s in missing_skills else 0 for s in categories]

    # Close the radar loop
    categories_loop = categories + [categories[0]]
    matched_loop    = matched_vals + [matched_vals[0]]
    missing_loop    = missing_vals + [missing_vals[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=matched_loop,
        theta=categories_loop,
        fill='toself',
        fillcolor="rgba(34,197,94,0.12)",
        line=dict(color=GREEN, width=2),
        name='Matched',
        hoverinfo='skip',
    ))

    fig.add_trace(go.Scatterpolar(
        r=missing_loop,
        theta=categories_loop,
        fill='toself',
        fillcolor="rgba(239,68,68,0.1)",
        line=dict(color=RED, width=1.5),
        name='Missing',
        hoverinfo='skip',
    ))

    fig.update_layout(
        paper_bgcolor=PLOTLY_LAYOUT_BASE["paper_bgcolor"],
        plot_bgcolor=PLOTLY_LAYOUT_BASE["plot_bgcolor"],
        font=PLOTLY_LAYOUT_BASE["font"],
        height=230,
        margin=dict(l=20, r=20, t=40, b=30),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showticklabels=False,
                gridcolor=BORDER_ACTIVE,
                linecolor=BORDER_ACTIVE,
            ),
            angularaxis=dict(
                tickfont=dict(size=9.5, color=TEXT_SECONDARY, family="Inter"),
                gridcolor=BORDER,
                linecolor=BORDER,
            ),
        ),
        legend=dict(
            font=dict(size=10, color=TEXT_SECONDARY, family="Inter"),
            bgcolor="rgba(0,0,0,0)",
            x=0.5,
            xanchor="center",
            y=-0.12,
            orientation="h",
            
        ),
        title=dict(
            text="Skill Coverage",
            font=dict(color=TEXT_MUTED, size=11, family="Inter"),
            x=0.5,
            xanchor="center",
        ),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
# 3. SKILL MATCH BAR CHART
# ══════════════════════════════════════════════════════════════════════════════
def render_skill_match_bar(matched_skills: list, missing_skills: list):
    """Render a horizontal stacked bar showing match % vs gap %."""
    total = len(matched_skills) + len(missing_skills)
    if total == 0:
        st.caption("No skill data available.")
        return

    match_pct   = round(len(matched_skills) / total * 100)
    missing_pct = 100 - match_pct

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Matched',
        x=[match_pct],
        y=[''],
        orientation='h',
        marker=dict(
            color=GREEN,
            line=dict(width=0),
        ),
        text=[f"{match_pct}%"],
        textposition='inside',
        textfont=dict(color="#0a0a0a", size=12, family="Inter"),
        width=0.55,
        hovertemplate="Matched: %{x}%<extra></extra>",
    ))

    fig.add_trace(go.Bar(
        name='Missing',
        x=[missing_pct],
        y=[''],
        orientation='h',
        marker=dict(
            color="rgba(239,68,68,0.55)",
            line=dict(width=0),
        ),
        text=[f"{missing_pct}%"],
        textposition='inside',
        textfont=dict(color=TEXT_PRIMARY, size=12, family="Inter"),
        width=0.55,
        hovertemplate="Missing: %{x}%<extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor=PLOTLY_LAYOUT_BASE["paper_bgcolor"],
        plot_bgcolor=PLOTLY_LAYOUT_BASE["plot_bgcolor"],
        font=PLOTLY_LAYOUT_BASE["font"],
        barmode='stack',
        height=130,
        margin=dict(l=10, r=10, t=45, b=10),
        xaxis=dict(
            range=[0, 100],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        legend=dict(
            orientation='h',
            font=dict(size=10, color=TEXT_SECONDARY, family="Inter"),
            bgcolor="rgba(0,0,0,0)",
            x=0.5,
            xanchor="center",
            y=1.3,
        
        ),
        title=dict(
            text="Match vs Gap",
            font=dict(size=11, color=TEXT_MUTED, family="Inter"),
            x=0.5,
            xanchor="center",
        ),
        bargap=0,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
# 4. MISSING SKILLS TABLE
# ══════════════════════════════════════════════════════════════════════════════
def render_missing_skills_table(missing_skills_detail: list):
    """Render a styled dataframe of missing skills with priority and category."""
    if not missing_skills_detail:
        st.caption("No missing skills detail available.")
        return

    df = pd.DataFrame(missing_skills_detail)

    expected_cols = ["skill", "category", "priority", "why_important"]
    for col in expected_cols:
        if col not in df.columns:
            df[col] = "N/A"

    df = df[expected_cols].rename(columns={
        "skill":         "Skill",
        "category":      "Category",
        "priority":      "Priority",
        "why_important": "Why It Matters",
    })

    def priority_color(val):
        colors = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#22c55e"}
        c = colors.get(val, "#8a8a8a")
        return f"color: {c}; font-weight: 600;"

    styled = df.style.map(priority_color, subset=["Priority"])

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        height=min(260, 44 + 36 * len(df)),
    )
