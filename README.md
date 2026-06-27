
# 📄 AI Resume Analyzer

A production-ready resume analysis tool powered by Google Gemini AI. Upload a PDF resume, paste a job description, and get instant ATS scoring, skill gap analysis, improvement suggestions, and a personalized 8-week learning roadmap.

Built with Streamlit + Python as a student portfolio project.

---

## 🖼 What It Does

| Feature | Description |
|---------|-------------|
| **ATS Score** | 0–100 compatibility score vs the job description |
| **Skill Matching** | Lists skills your resume has vs what the job needs |
| **Gap Analysis** | Missing skills with priority levels and why they matter |
| **Strengths** | What your resume does well |
| **Suggestions** | Specific, actionable resume improvements |
| **Learning Roadmap** | 8-week plan with real resources to close skill gaps |
| **PDF Report** | Downloadable full analysis as a formatted PDF |
| **JSON Export** | Raw analysis data for your own use |

---

## 🏗 Project Architecture

```
resume_analyzer/
├── app.py                      ← Main Streamlit application (entry point)
├── requirements.txt            ← Python dependencies
├── .env.example                ← Environment variable template
├── .gitignore                  ← Git ignore rules
│
├── .streamlit/
│   └── config.toml             ← Streamlit theme configuration
│
├── components/
│   ├── __init__.py
│   ├── styles.py               ← All custom CSS (dark theme)
│   └── charts.py               ← Plotly visualizations
│
└── utils/
    ├── __init__.py
    ├── pdf_reader.py           ← PDF text extraction
    ├── gemini_client.py        ← Gemini AI API integration
    └── report_generator.py     ← PDF report creation (ReportLab)
```

---

## 🔄 Data Flow

```
User uploads PDF
      │
      ▼
pdf_reader.py
  extract_text_from_pdf()
  └── PyPDF/PyPDF2 → raw text
      │
      ▼
User pastes Job Description
      │
      ▼
gemini_client.py
  analyze_resume()
  └── Build prompt → Gemini API → Parse JSON response
      │
      ▼
app.py
  render_results()
  ├── components/charts.py    ← ATS gauge, radar, bar, table
  ├── Skill tags (matched/missing)
  ├── Strength cards
  ├── Suggestion list
  └── Learning roadmap (expandable)
      │
      ▼
report_generator.py
  generate_pdf_report()
  └── ReportLab → PDF bytes → st.download_button
```

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit 1.35+ | UI framework |
| AI | Google Gemini 2.0 Flash | Resume analysis |
| PDF Read | pypdf / PyPDF2 | Extract resume text |
| PDF Write | ReportLab | Generate analysis report |
| Charts | Plotly | ATS gauge, radar, bar charts |
| Data | Pandas | Missing skills table |
| Config | python-dotenv | API key management |

---

## 🚀 Quick Start (Local)

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

### 2. Create a virtual environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get your Gemini API key
1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API Key**
3. Copy the key

### 5. Set up environment variables
```bash
cp .env.example .env
# Edit .env and paste your API key:
# GEMINI_API_KEY=your_actual_key_here
```

### 6. Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 🌐 Deployment Guide

### Option A: Streamlit Community Cloud (Free, Recommended)

1. Push your code to GitHub (make sure `.env` is in `.gitignore`)
2. Go to https://share.streamlit.io
3. Click **New app** → connect your repo
4. Set **Main file path** to `app.py`
5. Go to **Advanced settings → Secrets** and add:
   ```
   GEMINI_API_KEY = "your_key_here"
   ```
6. Click **Deploy**

> ⚠️ Do NOT commit your `.env` file with real keys to GitHub.

---

### Option B: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add --variable GEMINI_API_KEY=your_key
railway up
```

---

### Option C: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t resume-analyzer .
docker run -e GEMINI_API_KEY=your_key -p 8501:8501 resume-analyzer
```

---

### Option D: Render

1. Push to GitHub
2. Create a new **Web Service** on render.com
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Add environment variable: `GEMINI_API_KEY`

---

## 🔑 API Key Notes

- **Gemini 2.0 Flash** is used by default (fast, capable, has a generous free tier)
- Free tier: 1,500 requests/day, 1M tokens/minute
- To change the model, edit `GEMINI_MODEL` in `.env` or modify `gemini_client.py`

---

## 🧩 Module Reference

### `utils/pdf_reader.py`
- `extract_text_from_pdf(uploaded_file)` → `(text, error)`
- Handles encrypted PDFs, image-only PDFs, size limits
- Cleans extracted text (removes artifacts, extra whitespace)

### `utils/gemini_client.py`
- `analyze_resume(resume_text, job_description, api_key)` → `(analysis_dict, error)`
- Sends carefully engineered prompt to Gemini
- Parses JSON response with validation and fallback defaults
- Retry logic for transient API errors

### `utils/report_generator.py`
- `generate_pdf_report(analysis, resume_text, job_description)` → `bytes`
- Multi-page PDF with dark-ish professional styling
- Includes all sections: score, skills, strengths, suggestions, roadmap

### `components/charts.py`
- `render_ats_gauge(score)` — Plotly indicator gauge
- `render_skill_radar(matched, missing)` — Spider chart
- `render_skill_match_bar(matched, missing)` — Horizontal stacked bar
- `render_missing_skills_table(detail)` — Color-coded Pandas dataframe

### `components/styles.py`
- `inject_styles()` — Injects all custom CSS via `st.markdown`
- Dark theme matching professional tools, not generic SaaS templates

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `GEMINI_API_KEY not found` | Add key to `.env` and restart the app |
| `API key not valid` | Regenerate key at aistudio.google.com |
| `No text found in PDF` | Your PDF is image-only; use a text-based PDF |
| `Analysis failed` | Check API quota at console.cloud.google.com |
| `PDF report failed` | Ensure `reportlab` is installed |
| Charts not showing | Ensure `plotly` is installed |

---

## 📁 Adding Your Own Features

**To add a new chart:**
1. Add the function to `components/charts.py`
2. Import and call it in `app.py`'s `render_results()` function

**To change the AI model:**
1. Edit `model_name` in `utils/gemini_client.py`
2. Available models: `gemini-2.0-flash`, `gemini-1.5-pro`, `gemini-1.5-flash`

**To add a new analysis section:**
1. Add the field to the JSON prompt in `gemini_client.py`
2. Add a renderer in `app.py`'s `render_results()` function
3. Add it to `report_generator.py` if it should appear in the PDF

---

## 📝 License

MIT License — free to use for personal and commercial projects.

---

*Built as a student portfolio project demonstrating AI integration, PDF processing, data visualization, and production Streamlit architecture.*
