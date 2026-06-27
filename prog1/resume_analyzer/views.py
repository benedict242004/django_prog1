import os
import json
from groq import Groq
import pdfplumber
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import AnalysisResult


GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')


def extract_pdf_text(pdf_file) -> str:
    text = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return '\n'.join(text)


def analyze_with_groq(resume_text: str, job_description: str) -> dict:
    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""You are an expert career coach and ATS (Applicant Tracking System) specialist.

Analyze the following resume against the job description provided.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY a valid JSON object (no markdown, no extra text) with this exact structure:
{{
  "job_title": "The job title extracted from the job description",
  "match_score": <integer 0-100 representing how well the resume matches the JD>,
  "matched_skills": ["skill1", "skill2", ...],
  "missing_skills": ["skill1", "skill2", ...],
  "suggestions": [
    "Specific actionable improvement suggestion 1",
    "Specific actionable improvement suggestion 2",
    "Specific actionable improvement suggestion 3",
    "Specific actionable improvement suggestion 4",
    "Specific actionable improvement suggestion 5"
  ],
  "summary": "A 2-3 sentence professional summary of the match analysis"
}}

Be specific, honest, and helpful. Base the match score on skills alignment, experience relevance, and keyword coverage."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


def index(request):
    return render(request, 'analyzer/index.html')


@require_POST
def analyze(request):
    if not GROQ_API_KEY:
        messages.error(request, 'GROQ_API_KEY is not set. Please add it to your environment variables.')
        return redirect('analyzer_index')

    resume_file = request.FILES.get('resume')
    job_description = request.POST.get('job_description', '').strip()

    if not resume_file:
        messages.error(request, 'Please upload a resume PDF.')
        return redirect('analyzer_index')

    if not job_description:
        messages.error(request, 'Please paste a job description.')
        return redirect('analyzer_index')

    if not resume_file.name.endswith('.pdf'):
        messages.error(request, 'Only PDF files are supported.')
        return redirect('analyzer_index')

    try:
        resume_text = extract_pdf_text(resume_file)
        if not resume_text.strip():
            messages.error(request, 'Could not extract text from the PDF. Make sure it is not a scanned image.')
            return redirect('analyzer_index')

        data = analyze_with_groq(resume_text, job_description)

        result = AnalysisResult.objects.create(
            job_title=data.get('job_title', 'Unknown Role'),
            match_score=int(data.get('match_score', 0)),
            matched_skills=json.dumps(data.get('matched_skills', [])),
            missing_skills=json.dumps(data.get('missing_skills', [])),
            suggestions=json.dumps(data.get('suggestions', [])),
            summary=data.get('summary', ''),
        )
        return redirect('result', result_id=result.id)

    except json.JSONDecodeError:
        messages.error(request, 'AI returned an unexpected response. Please try again.')
        return redirect('analyzer_index')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('analyzer_index')


def result(request, result_id):
    r = get_object_or_404(AnalysisResult, id=result_id)
    context = {
        'result': r,
        'matched_skills': json.loads(r.matched_skills),
        'missing_skills': json.loads(r.missing_skills),
        'suggestions': json.loads(r.suggestions),
    }
    return render(request, 'analyzer/result.html', context)


def history(request):
    results = AnalysisResult.objects.all()[:20]
    return render(request, 'analyzer/history.html', {'results': results})
