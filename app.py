import os
import json
import streamlit as st
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from src.pdf_utils import input_pdf_text

# Load Spacy Model
nlp = spacy.load("en_core_web_sm")

# Streamlit UI
st.title("🚀 AI Resume Evaluation - Free & Powerful")
st.write("Upload your resume and enter a job description to get evaluation feedback, AI-powered suggestions, and job matches.")

# File Upload
uploaded_file = st.file_uploader("📄 Upload your Resume (PDF only)", type="pdf")
jd = st.text_area("📝 Enter the Job Description (max 500 words)", max_chars=2500)

# Function to extract keywords
def extract_keywords(text, top_n=10):
    doc = nlp(text)
    words = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return list(set(words))[:top_n]  # Return unique top words

# Function to improve resume action words
def enhance_action_words(text):
    doc = nlp(text)
    improved_text = " "
    for token in doc:
        if token.pos_ == "VERB":
            improved_text += TextBlob(token.text).correct() + " "
        else:
            improved_text += token.text + " "
    return improved_text.strip()

# Function to compare resume and job description
def match_resume_with_jd(resume_text, job_desc):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_desc)
    
    missing_skills = set(jd_keywords) - set(resume_keywords)
    score = len(set(resume_keywords) & set(jd_keywords)) / len(jd_keywords) * 100
    return score, missing_skills

# Function to generate a resume summary
def generate_summary(resume_text):
    doc = nlp(resume_text)
    sentences = [sent.text for sent in doc.sents]
    return " ".join(sentences[:3])  # Return first 3 sentences as summary

# Function to generate a basic AI cover letter
def generate_cover_letter(name, job_title, company):
    return f"""Dear Hiring Manager,

I am excited to apply for the {job_title} position at {company}. With my skills and experience, I am confident that I can contribute significantly to your team. My background in [your_field] has equipped me with the necessary expertise to excel in this role.

I welcome the opportunity to discuss how my qualifications align with your needs.

Best Regards,
{name}
"""

# Evaluate Button
if st.button("🚀 Evaluate My Resume"):
    if uploaded_file and jd.strip():
        resume_text = input_pdf_text(uploaded_file)
        if resume_text:
            score, missing_skills = match_resume_with_jd(resume_text, jd)
            enhanced_text = enhance_action_words(resume_text)
            summary = generate_summary(resume_text)
            
            # Display Results
            st.subheader("✅ Evaluation Results")
            st.write(f"**Resume Match Score:** {score:.2f}%")
            st.write("🔴 **Missing Skills:**", ", ".join(missing_skills) if missing_skills else "None")
            
            st.subheader("💡 Enhanced Resume Suggestions")
            st.write(enhanced_text)
            
            st.subheader("📜 AI-Generated Resume Summary")
            st.write(summary)
            
            # Sample Cover Letter
            st.subheader("✉️ AI-Generated Cover Letter")
            st.text_area("Your AI-generated cover letter:", generate_cover_letter("Your Name", "Job Title", "Company Name"), height=200)
            
            # Future Feature: Job Portal Integration (Commented for Now)
            # st.subheader("🌍 Job Match Across Portals")
            # st.write("🚀 Soon, you will be able to upload your resume and our AI will find the best job matches from Indeed, LinkedIn, and more!")
        else:
            st.error("⚠️ Could not extract text from PDF.")
    else:
        st.warning("⚠️ Please upload a resume and enter a job description.")
