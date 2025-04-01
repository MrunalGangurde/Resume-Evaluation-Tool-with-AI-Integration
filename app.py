import os
import json
import streamlit as st
import spacy
import requests
import pdfplumber
import subprocess
import ollama
from tenacity import retry, stop_after_attempt, wait_fixed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys

# Ensure spaCy model is available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Streamlit UI Setup
st.set_page_config(page_title="hiremedamnit", page_icon="🚀")
st.sidebar.title("Job Portal Filters")
portal_options = st.sidebar.multiselect("Select Job Portals", ["QuickJSearch", "Jooble", "Adzuna"], default=["QuickJSearch", "Jooble", "Adzuna"])
st.title("hiremedamnit - AI Resume Evaluation")

# Job Filters
remote_only = st.sidebar.checkbox("Remote Only")
salary_range = st.sidebar.slider("Salary Range ($)", 30000, 200000, (50000, 100000))
experience_level = st.sidebar.selectbox("Experience Level", ["Entry", "Mid", "Senior"])

st.write("Upload your resume and enter a job description to get AI-powered suggestions and job matches.")

# File Upload
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF only)", type="pdf")
jd = st.text_area("📝 Enter the Job Description (max 500 words)", max_chars=2500)

# Extract text from PDF
def input_pdf_text(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        return text if text.strip() else None
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

# TF-IDF Matching
def match_resume_with_jd(resume_text, job_desc):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
    return round(score, 2)

# Generate AI Cover Letter using Local LLaMA/Mistral Model
def generate_cover_letter(name, job_title, company, resume_summary):
    prompt = f"""
    Write a professional cover letter for {name} applying for the {job_title} position at {company}.
    Use the following resume summary:
    "{resume_summary}"
    The tone should be engaging and professional.
    """
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Job Fetching with Retry Mechanism
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_jobs_from_apis(query, location="USA"):
    jobs = []
    headers = {'Content-Type': 'application/json'}
    
    if "QuickJSearch" in portal_options:
        quickjsearch_url = f"https://api.quickjsearch.com/jobs?query={query}&location={location}"
        response = requests.get(quickjsearch_url)
        if response.status_code == 200:
            jobs.extend(response.json().get("results", []))
    
    if "Jooble" in portal_options:
        jooble_url = "https://jooble.org/api/YOUR_JOOBLE_API_KEY"
        payload = json.dumps({"keywords": query, "location": location})
        response = requests.post(jooble_url, headers=headers, data=payload)
        if response.status_code == 200:
            jobs.extend(response.json().get("jobs", []))
    
    if "Adzuna" in portal_options:
        adzuna_url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id=YOUR_ADZUNA_APP_ID&app_key=YOUR_ADZUNA_APP_KEY&what={query}&where={location}"
        response = requests.get(adzuna_url)
        if response.status_code == 200:
            jobs.extend(response.json().get("results", []))
    
    return jobs

# Evaluate Button
if st.button("🚀 Evaluate My Resume"):
    if uploaded_file and jd.strip():
        resume_text = input_pdf_text(uploaded_file)
        if resume_text:
            with st.spinner("Analyzing your resume..."):
                score = match_resume_with_jd(resume_text, jd)
                summary = " ".join(resume_text.split(". ")[:3])  # Simple Summary Extraction
                cover_letter = generate_cover_letter("Your Name", "Job Title", "Company Name", summary)
            
            # Display Results
            st.subheader("✅ Evaluation Results")
            st.write(f"**Resume Match Score:** {score:.2f}%")
            
            st.subheader("📜 AI-Generated Resume Summary")
            st.write(summary)
            
            st.subheader("✉️ AI-Generated Cover Letter")
            st.text_area("Your AI-generated cover letter:", cover_letter, height=200)
            
            # Job Matching Feature
            st.subheader("🌍 Job Matches from Portals")
            jobs = fetch_jobs_from_apis(jd)
            if jobs:
                for job in jobs[:5]:  # Show top 5 job results
                    if remote_only and "remote" not in job.get("title", "").lower():
                        continue
                    if "salary" in job and not (salary_range[0] <= job["salary"] <= salary_range[1]):
                        continue
                    if experience_level.lower() not in job.get("title", "").lower():
                        continue
                    
                    st.write(f"**{job.get('title', 'No Title')}** - {job.get('company', 'Unknown Company')} ({job.get('location', 'Unknown Location')})")
                    st.write(f"🔗 [Apply Here]({job.get('url', '#')})")
            else:
                st.warning("⚠️ No jobs found. Try refining your search query.")
        else:
            st.error("⚠️ Could not extract text from PDF.")
    else:
        st.warning("⚠️ Please upload a resume and enter a job description.")
