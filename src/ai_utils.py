import google.generativeai as genai
import streamlit as st

def get_gemini_response(input_text):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        st.error(f"Failed to generate response: {str(e)}")
        return None