"""
components/styles.py
====================
Injects all custom CSS for the dark professional theme.
Keeps styling centralized and separate from logic.
"""

import streamlit as st


def inject_styles():
    """Call this once at the top of app.py to apply the full theme."""
    st.markdown("""
    <style>
    /* ═══════════════════════════════════════════════════════
       GLOBAL BASE
    ═══════════════════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        /* Backgrounds */
        --bg-primary:     #0a0a0a;
        --bg-secondary:   #111111;
        --bg-card:        #161616;
        --bg-elevated:    #1e1e1e;
        --bg-hover:       #242424;

        /* Borders */
        --border:         #222222;
        --border-active:  #333333;
        --border-hover:   #444444;

        /* Text */
        --text-primary:   #f2f2f2;
        --text-secondary: #8a8a8a;
        --text-muted:     #444444;
        --text-dim:       #666666;

        /* Accents */
        --accent-green:   #22c55e;
        --accent-green-dim: rgba(34,197,94,0.12);
        --accent-green-border: rgba(34,197,94,0.28);
        --accent-red:     #ef4444;
        --accent-red-dim: rgba(239,68,68,0.12);
        --accent-red-border: rgba(239,68,68,0.28);
        --accent-amber:   #f59e0b;
        --accent-blue:    #3b82f6;
        --accent-blue-dim: rgba(59,130,246,0.12);
        --accent-purple:  #a78bfa;
        --accent-purple-dim: rgba(167,139,250,0.1);

        /* Typography */
        --font-sans:      'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-mono:      'JetBrains Mono', 'Fira Code', monospace;

        /* Spacing */
        --space-xs:  0.25rem;
        --space-sm:  0.5rem;
        --space-md:  1rem;
        --space-lg:  1.5rem;
        --space-xl:  2rem;
        --space-2xl: 3rem;

        /* Radii */
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;

        /* Shadows */
        --shadow-sm:  0 1px 3px rgba(0,0,0,0.4);
        --shadow-md:  0 4px 12px rgba(0,0,0,0.5);
        --shadow-lg:  0 8px 24px rgba(0,0,0,0.6);
        --shadow-glow-green: 0 0 20px rgba(34,197,94,0.12);
        --shadow-glow-red:   0 0 20px rgba(239,68,68,0.10);

        /* Transitions */
        --transition-fast:   0.12s ease;
        --transition-normal: 0.2s ease;
        --transition-slow:   0.35s ease;
    }

    /* ── Keyframe Animations ───────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse-green {
        0%, 100% { box-shadow: 0 0 0 0 rgba(34,197,94,0.4); }
        50%       { box-shadow: 0 0 0 4px rgba(34,197,94,0); }
    }

    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-6px); }
        to   { opacity: 1; transform: translateX(0); }
    }

    /* ── Global Resets ─────────────────────────────────── */
    html {
        scroll-behavior: smooth;
    }

    html, body, [class*="css"] {
        font-family: var(--font-sans) !important;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    .stApp {
        background-color: var(--bg-primary) !important;
    }

    /* Main content max width for better readability */
    .main .block-container {
        max-width: 1200px !important;
        padding-top: 0 !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }

    /* Hide default Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stDecoration"] { display: none; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: var(--border-active);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--border-hover); }

    /* ── Section headings (h3) ─────────────────────────── */
    h1, h2, h3, h4 { color: var(--text-primary) !important; }

    h3 {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
        color: var(--text-primary) !important;
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    hr {
        border: none !important;
        border-top: 1px solid var(--border) !important;
        margin: 2rem 0 !important;
        opacity: 1 !important;
    }

    /* Spinner */
    .stSpinner > div { border-top-color: var(--accent-green) !important; }

    /* ═══════════════════════════════════════════════════════
       HEADER
    ═══════════════════════════════════════════════════════ */
    .app-header {
        padding: 3.5rem 0 2.5rem 0;
        margin-bottom: 2.5rem;
        position: relative;
        animation: fadeInUp 0.5s ease;
    }

    .app-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent 0%,
            var(--border-active) 20%,
            var(--border-active) 80%,
            transparent 100%
        );
    }

    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-family: var(--font-mono);
        font-size: 0.62rem;
        font-weight: 600;
        letter-spacing: 0.16em;
        color: var(--accent-green);
        background: var(--accent-green-dim);
        border: 1px solid var(--accent-green-border);
        padding: 4px 12px 4px 10px;
        border-radius: 20px;
        margin-bottom: 1.25rem;
        text-transform: uppercase;
        animation: pulse-green 3s ease infinite;
    }

    .header-badge::before {
        content: '';
        display: inline-block;
        width: 6px;
        height: 6px;
        background: var(--accent-green);
        border-radius: 50%;
        box-shadow: 0 0 6px var(--accent-green);
    }

    .app-title {
        font-size: 2.75rem;
        font-weight: 800;
        color: var(--text-primary);
        letter-spacing: -0.03em;
        margin: 0 0 0.5rem 0;
        line-height: 1.05;
        background: linear-gradient(135deg, #f2f2f2 0%, #8a8a8a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .app-subtitle {
        color: var(--text-secondary);
        font-size: 0.95rem;
        font-weight: 400;
        letter-spacing: 0.01em;
        margin: 0;
        line-height: 1.6;
    }

    .app-subtitle span {
        color: var(--text-dim);
        margin: 0 0.4rem;
    }

    /* ═══════════════════════════════════════════════════════
       SECTION LABELS
    ═══════════════════════════════════════════════════════ */
    .section-label {
        font-family: var(--font-mono);
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.18em;
        color: var(--text-muted);
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }

    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    .field-label {
        font-size: 0.82rem;
        font-weight: 500;
        color: var(--text-secondary);
        margin-bottom: 0.6rem !important;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        letter-spacing: 0.01em;
    }

    /* ═══════════════════════════════════════════════════════
       FILE UPLOADER
    ═══════════════════════════════════════════════════════ */
    [data-testid="stFileUploader"] {
        border: 1px dashed var(--border-active) !important;
        border-radius: var(--radius-md) !important;
        background: var(--bg-secondary) !important;
        transition: border-color var(--transition-normal) !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: var(--border-hover) !important;
    }

    [data-testid="stFileUploader"] section {
        background: transparent !important;
        border: none !important;
        padding: 1.75rem !important;
    }

    [data-testid="stFileUploader"] section p {
        color: var(--text-secondary) !important;
        font-size: 0.85rem !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: var(--text-secondary) !important;
    }

    .file-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--accent-green-dim);
        border: 1px solid var(--accent-green-border);
        border-radius: 20px;
        padding: 5px 14px 5px 10px;
        font-size: 0.78rem;
        font-weight: 500;
        color: var(--accent-green);
        margin-top: 0.6rem;
        animation: slideIn 0.25s ease;
    }

    .chip-icon {
        font-weight: 700;
        font-size: 0.9rem;
    }

    .chip-size {
        color: var(--text-muted);
        font-size: 0.7rem;
        font-family: var(--font-mono);
    }

    /* ═══════════════════════════════════════════════════════
       TEXT AREA
    ═══════════════════════════════════════════════════════ */
    .stTextArea textarea {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-active) !important;
        border-radius: var(--radius-md) !important;
        color: var(--text-primary) !important;
        font-size: 0.855rem !important;
        font-family: var(--font-sans) !important;
        line-height: 1.65 !important;
        transition: border-color var(--transition-normal) !important;
        resize: vertical !important;
    }

    .stTextArea textarea:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px var(--accent-blue-dim) !important;
        outline: none !important;
    }

    .stTextArea textarea::placeholder {
        color: var(--text-muted) !important;
        font-size: 0.83rem !important;
    }

    /* ═══════════════════════════════════════════════════════
       BUTTONS
    ═══════════════════════════════════════════════════════ */
    .stButton > button[kind="primary"] {
        background: var(--text-primary) !important;
        color: var(--bg-primary) !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        font-weight: 700 !important;
        font-size: 0.875rem !important;
        letter-spacing: 0.01em !important;
        padding: 0.7rem 2rem !important;
        transition: all var(--transition-fast) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #e0e0e0 !important;
        box-shadow: var(--shadow-md) !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button[kind="primary"]:active {
        transform: translateY(0) !important;
    }

    .stDownloadButton > button {
        background: var(--bg-elevated) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-active) !important;
        border-radius: var(--radius-md) !important;
        font-size: 0.83rem !important;
        font-weight: 500 !important;
        transition: all var(--transition-normal) !important;
        padding: 0.55rem 1rem !important;
    }

    .stDownloadButton > button:hover {
        background: var(--bg-hover) !important;
        border-color: var(--border-hover) !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* ═══════════════════════════════════════════════════════
       ATS BANNER
    ═══════════════════════════════════════════════════════ */
    .ats-banner {
        display: flex;
        align-items: center;
        gap: 2.5rem;
        background: var(--bg-card);
        border: 1px solid var(--border-active);
        border-radius: var(--radius-lg);
        padding: 2rem 2.5rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.4s ease;
        box-shadow: var(--shadow-md);
    }

    /* Subtle left accent bar */
    .ats-banner::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: var(--score-color, var(--accent-green));
        border-radius: var(--radius-lg) 0 0 var(--radius-lg);
    }

    /* Very subtle background glow */
    .ats-banner::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(
            ellipse at 0% 50%,
            rgba(34,197,94,0.04) 0%,
            transparent 60%
        );
        pointer-events: none;
    }

    .ats-left {
        min-width: 160px;
    }

    .ats-label {
        font-family: var(--font-mono);
        font-size: 0.6rem;
        font-weight: 600;
        letter-spacing: 0.18em;
        color: var(--text-muted);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
    }

    .ats-score {
        font-size: 4.5rem;
        font-weight: 800;
        line-height: 1;
        letter-spacing: -0.04em;
    }

    .ats-percent {
        font-size: 2rem;
        font-weight: 300;
        opacity: 0.6;
    }

    .ats-status {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        font-family: var(--font-mono);
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        padding: 4px 12px;
        border-radius: 20px;
        margin-top: 0.65rem;
        text-transform: uppercase;
    }

    .ats-divider {
        width: 1px;
        height: 80px;
        background: var(--border);
        flex-shrink: 0;
    }

    .ats-right {
        flex: 1;
    }

    .ats-desc {
        color: var(--text-secondary);
        font-size: 0.9rem;
        line-height: 1.75;
        margin: 0;
        font-weight: 400;
    }

    /* ═══════════════════════════════════════════════════════
       SKILL TAGS
    ═══════════════════════════════════════════════════════ */
    .skill-section-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.5rem;
        height: 100%;
        transition: border-color var(--transition-normal);
    }

    .skill-section-card:hover {
        border-color: var(--border-active);
    }

    .skill-box-header {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        padding-bottom: 0.65rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        text-transform: uppercase;
    }

    .skill-count-badge {
        font-family: var(--font-mono);
        font-size: 0.65rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 10px;
    }

    .matched-header { color: var(--accent-green); }
    .matched-header .skill-count-badge {
        background: var(--accent-green-dim);
        color: var(--accent-green);
        border: 1px solid var(--accent-green-border);
    }

    .missing-header { color: var(--accent-red); }
    .missing-header .skill-count-badge {
        background: var(--accent-red-dim);
        color: var(--accent-red);
        border: 1px solid var(--accent-red-border);
    }

    .skill-tags-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
    }

    .skill-tag {
        display: inline-flex;
        align-items: center;
        font-size: 0.75rem;
        font-weight: 500;
        padding: 5px 13px;
        border-radius: 20px;
        transition: all var(--transition-fast);
        cursor: default;
        letter-spacing: 0.01em;
    }

    .matched-tag {
        background: var(--accent-green-dim);
        border: 1px solid var(--accent-green-border);
        color: #86efac;
    }

    .matched-tag:hover {
        background: rgba(34,197,94,0.18);
        border-color: rgba(34,197,94,0.45);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(34,197,94,0.15);
    }

    .missing-tag {
        background: var(--accent-red-dim);
        border: 1px solid var(--accent-red-border);
        color: #fca5a5;
    }

    .missing-tag:hover {
        background: rgba(239,68,68,0.18);
        border-color: rgba(239,68,68,0.45);
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(239,68,68,0.15);
    }

    .empty-state {
        color: var(--text-muted);
        font-size: 0.83rem;
        font-style: italic;
        padding: 0.5rem 0;
    }

    /* ═══════════════════════════════════════════════════════
       STRENGTH CARDS
    ═══════════════════════════════════════════════════════ */
    .strength-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.1rem 1.25rem;
        margin-bottom: 0.75rem;
        transition: all var(--transition-normal);
        position: relative;
        overflow: hidden;
    }

    .strength-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-green), transparent);
        opacity: 0;
        transition: opacity var(--transition-normal);
    }

    .strength-card:hover {
        border-color: var(--border-active);
        box-shadow: var(--shadow-sm);
        transform: translateY(-1px);
    }

    .strength-card:hover::before {
        opacity: 1;
    }

    .strength-icon {
        font-size: 1rem;
        margin-bottom: 0.45rem;
        display: block;
    }

    .strength-card p {
        color: var(--text-secondary);
        font-size: 0.845rem;
        line-height: 1.65;
        margin: 0;
    }

    /* ═══════════════════════════════════════════════════════
       SUGGESTION ITEMS
    ═══════════════════════════════════════════════════════ */
    .suggestion-item {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        padding: 1rem 1.1rem;
        border-left: 2px solid var(--border-active);
        margin-bottom: 0.5rem;
        background: var(--bg-secondary);
        border-radius: 0 var(--radius-md) var(--radius-md) 0;
        transition: all var(--transition-normal);
    }

    .suggestion-item:hover {
        border-left-color: var(--accent-blue);
        background: var(--bg-elevated);
        transform: translateX(2px);
    }

    .suggestion-num {
        font-family: var(--font-mono);
        font-size: 0.65rem;
        font-weight: 600;
        color: var(--text-muted);
        padding-top: 3px;
        min-width: 22px;
        flex-shrink: 0;
    }

    .suggestion-item p {
        color: var(--text-secondary);
        font-size: 0.865rem;
        line-height: 1.65;
        margin: 0;
    }

    .suggestion-item:hover p {
        color: var(--text-primary);
    }

    /* ═══════════════════════════════════════════════════════
       LEARNING ROADMAP
    ═══════════════════════════════════════════════════════ */
    .roadmap-subtitle {
        color: var(--text-secondary);
        font-size: 0.865rem;
        margin-bottom: 1.25rem;
        line-height: 1.6;
    }

    .week-goal {
        background: var(--accent-purple-dim);
        border: 1px solid rgba(167,139,250,0.22);
        border-radius: var(--radius-sm);
        padding: 0.65rem 1rem;
        color: #c4b5fd;
        font-size: 0.845rem;
        margin-bottom: 0.75rem;
        line-height: 1.6;
    }

    /* Expander styling */
    [data-testid="stExpander"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        margin-bottom: 0.5rem !important;
        transition: border-color var(--transition-normal) !important;
        overflow: hidden !important;
    }

    [data-testid="stExpander"]:hover {
        border-color: var(--border-active) !important;
    }

    [data-testid="stExpander"] summary {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        padding: 0.8rem 1rem !important;
    }

    [data-testid="stExpander"] summary:hover {
        background: var(--bg-elevated) !important;
    }

    [data-testid="stExpanderDetails"] {
        padding: 0.5rem 1rem 1rem 1rem !important;
        border-top: 1px solid var(--border) !important;
    }

    /* ═══════════════════════════════════════════════════════
       DATAFRAME / TABLE
    ═══════════════════════════════════════════════════════ */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        overflow: hidden !important;
    }

    /* ═══════════════════════════════════════════════════════
       ALERTS & MESSAGES
    ═══════════════════════════════════════════════════════ */
    [data-testid="stAlert"] {
        border-radius: var(--radius-md) !important;
        border: 1px solid !important;
        font-size: 0.875rem !important;
    }

    .stSuccess {
        background: rgba(34,197,94,0.08) !important;
        border-color: rgba(34,197,94,0.25) !important;
    }

    .stError {
        background: rgba(239,68,68,0.08) !important;
        border-color: rgba(239,68,68,0.25) !important;
    }

    .stWarning {
        background: rgba(245,158,11,0.08) !important;
        border-color: rgba(245,158,11,0.25) !important;
    }

    /* ═══════════════════════════════════════════════════════
       FOOTER
    ═══════════════════════════════════════════════════════ */
    .app-footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.72rem;
        font-family: var(--font-mono);
        padding: 2rem 0 1.5rem 0;
        margin-top: 2.5rem;
        letter-spacing: 0.04em;
        position: relative;
    }

    .app-footer::before {
        content: '';
        position: absolute;
        top: 0; left: 10%; right: 10%;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            var(--border-active) 30%,
            var(--border-active) 70%,
            transparent
        );
    }


    /* ═══════════════════════════════════════════════════════
       ATS BANNER ADDITIONS (Section 2)
    ═══════════════════════════════════════════════════════ */
    .ats-summary-label {
        font-family: var(--font-mono);
        font-size: 0.6rem;
        font-weight: 600;
        letter-spacing: 0.18em;
        color: var(--text-muted);
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    /* ═══════════════════════════════════════════════════════
       CHARTS CARD CONTAINER (Section 2)
    ═══════════════════════════════════════════════════════ */
    .charts-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1.5rem 0.75rem 1.5rem;
        margin: 1.5rem 0 1rem 0;
        box-shadow: var(--shadow-sm);
        transition: border-color var(--transition-normal);
    }

    .charts-card:hover {
        border-color: var(--border-active);
    }

    .charts-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border);
    }

    .charts-card-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text-secondary);
        letter-spacing: 0.02em;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Tighten Plotly chart spacing inside the card */
    .charts-card [data-testid="stPlotlyChart"] {
        margin-bottom: 0 !important;
    }

    .charts-card [data-testid="column"] {
        padding: 0 0.25rem !important;
    }

    </style>
    """, unsafe_allow_html=True)
