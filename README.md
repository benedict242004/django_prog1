# ResumeIQ — AI Resume Analyzer

A Django web application that analyzes your resume against a job description using AI, providing an instant match score, skill gap analysis, and tailored improvement suggestions.

## Features

- Upload your resume as a PDF
- Paste any job description
- Get an instant **match score (0–100%)**
- See **matched skills** and **missing skills** at a glance
- Receive **5 actionable improvement suggestions** powered by AI
- View your **analysis history** anytime

## Tech Stack

- **Backend:** Django 4.2, Python
- **AI:** Groq API (Llama 3.3 70B)
- **PDF Parsing:** pdfplumber
- **Database:** SQLite
- **Frontend:** Vanilla HTML/CSS/JS (no frameworks)

## Screenshots

> Add screenshots here after running the project locally.

## Getting Started

### Prerequisites

- Python 3.10+
- A free [Groq API key](https://console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/django_prog1.git
cd django_prog1/prog1

# Install dependencies
pip install -r requirements.txt

# Set your API key
# On Windows CMD:
set GROQ_API_KEY=your_groq_api_key_here

# Run migrations
python manage.py makemigrations resume_analyzer
python manage.py migrate

# Start the server
python manage.py runserver
```

Then open [http://127.0.0.1:8000/analyzer/](http://127.0.0.1:8000/analyzer/) in your browser.

## Project Structure

```
prog1/
├── resume_analyzer/       # Main app
│   ├── views.py           # PDF parsing + AI analysis logic
│   ├── models.py          # AnalysisResult model
│   ├── urls.py            # URL routing
│   └── migrations/
├── templates/
│   └── analyzer/
│       ├── index.html     # Upload form
│       ├── result.html    # Analysis results page
│       └── history.html   # Past analyses
├── manage.py
└── db.sqlite3
```

## Usage

1. Navigate to `/analyzer/`
2. Upload your resume PDF and paste the job description
3. Click **Analyze My Resume**
4. View your match score, skill gaps, and suggestions

## Notes

- Only PDF resumes are supported
- Make sure your PDF contains selectable text (not a scanned image)
- The `GROQ_API_KEY` environment variable must be set before starting the server

## License

MIT
