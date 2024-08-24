import PyPDF2 as pdf
import streamlit as st

def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_content = page.extract_text()
            if page_content:
                text += page_content
        return text
    except Exception as e:
        st.error(f"Failed to read PDF file: {str(e)}")
        return ""
