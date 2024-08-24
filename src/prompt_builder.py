def build_prompt(resume_text, job_description):
    input_prompt = f"""
    Hello, act as a highly skilled and experienced Resume Reviewer
    with deep expertise in technology fields such as software engineering, data science, data analysis,
    and big data engineering. Your task is to rigorously evaluate the resume based on the provided job description.
    Considering the competitive job market, provide the most accurate and helpful advice for improving the resume.
    Evaluate the resume on the following aspects:

    1. JD Match: Calculate the percentage match between the resume and the job description.
    2. Profile Summary: Summarize the candidate's qualifications, experience, and skills.
    3. Skill Match: Assess the alignment between the candidate's skills and the job requirements.
    4. Experience Alignment: Evaluate how well the candidate's experience matches the job role.
    5. Strengths and Weaknesses: Identify key strengths and any gaps or weaknesses.
    6. Suggestions: Provide actionable recommendations to enhance the resume's effectiveness.

    Resume: {resume_text}
    Job Description: {job_description}

    I want the response in one single structured string with the format:
    {{
      "JD Match": "percentage",
      "Profile Summary": "summary",
      "Skill Match": "skill_match",
      "Experience Alignment": "experience_alignment",
      "Strengths": ["strength_1", "strength_2"],
      "Weaknesses": ["weakness_1", "weakness_2"],
      "Suggestions": ["suggestion_1", "suggestion_2"]
    }}
    """
    return input_prompt
