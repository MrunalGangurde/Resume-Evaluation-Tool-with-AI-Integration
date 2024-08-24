import os
import json
import streamlit as st
from src.pdf_utils import input_pdf_text
from src.prompt_builder import build_prompt
from src.ai_utils import get_gemini_response
from src.response_parser import print_response

# Secure API Key Management
API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
if not API_KEY:
    st.error("API Key Not Found")
else:
    genai.configure(api_key=API_KEY)

# Streamlit Frontend
st.title("Resume Evaluation Tool with AI Integration")
st.write("Upload your resume and provide the job description to get AI-generated feedback.")

# File Upload
uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type="pdf")

# Job Description Input
jd = st.text_area("Enter the Job Description (max 500 words)", max_chars=2500)

# Processing and Display
if st.button("Evaluate"):
    if uploaded_file and jd.strip():
        resume_text = input_pdf_text(uploaded_file)
        if resume_text:
            input_prompt = build_prompt(resume_text, jd)
            response_text = get_gemini_response(input_prompt)
            if response_text:
                try:
                    response = json.loads(response_text)
                    print_response(response)
                except json.JSONDecodeError:
                    st.error("Failed to decode the AI response.")
            else:
                st.error("No response received from the AI model.")
    else:
        st.warning("Please upload a resume and enter a job description.")
