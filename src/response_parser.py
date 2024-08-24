import streamlit as st

def add_newlines(text):
    sentences = text.split('. ')
    return '.\n'.join(sentences) + '.'

def print_response(response):
    st.write(f"**JD Match:** {response.get('JD Match', 'N/A')}")
    st.write(f"**Profile Summary:**\n{add_newlines(response.get('Profile Summary', 'N/A'))}")
    st.write(f"**Skill Match:**\n{add_newlines(response.get('Skill Match', 'N/A'))}")
    st.write(f"**Experience Alignment:**\n{add_newlines(response.get('Experience Alignment', 'N/A'))}")
    st.write("**Strengths:**")
    strengths = response.get("Strengths", [])
    for strength in strengths:
        st.write(f"- {add_newlines(strength)}")
    st.write("**Weaknesses:**")
    weaknesses = response.get("Weaknesses", [])
    for weakness in weaknesses:
        st.write(f"- {add_newlines(weakness)}")
    st.write("**Suggestions:**")
    suggestions = response.get("Suggestions", [])
    for suggestion in suggestions:
        st.write(f"- {add_newlines(suggestion)}")