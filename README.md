# README: Resume Evaluation Tool with AI Integration

## Overview
The **Resume Evaluation Tool with AI Integration** is a Streamlit-based web application designed to help job seekers enhance their resumes. It leverages AI to evaluate resumes against specific job descriptions and provides actionable feedback to improve the chances of landing the desired job.

---

## Features
- Upload resumes in PDF format for evaluation.
- Input job descriptions (up to 500 words) to tailor the evaluation.
- Leverages AI to compare the resume content with the job description.
- Generates actionable insights to optimize the resume.
- User-friendly interface built with Streamlit.

---

## Requirements

### Prerequisites
- Python 3.8 or higher
- API Key for Google Generative AI (`GOOGLE_GENAI_API_KEY`)

### Libraries
The following libraries are required to run the application:
- `streamlit`
- `os`
- `json`
- Custom modules:
  - `src.pdf_utils`
  - `src.prompt_builder`
  - `src.ai_utils`
  - `src.response_parser`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/MrunalGangurde/Resume-Evaluation-Tool-with-AI-Integration.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Resume-Evaluation-Tool-with-AI-Integration
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set the `GOOGLE_GENAI_API_KEY` environment variable:
   ```bash
   export GOOGLE_GENAI_API_KEY=your_api_key
   ```

---

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```
2. Open the application in your browser (typically at `http://localhost:8501`).
3. Upload your resume (PDF format only).
4. Enter the job description in the provided text area.
5. Click the "Evaluate" button to receive AI-generated feedback.

---

## Directory Structure
```
.
├── app.py                 # Main application file
├── src/
│   ├── pdf_utils.py       # PDF text extraction utilities
│   ├── prompt_builder.py  # Constructs prompts for AI
│   ├── ai_utils.py        # Handles AI integration
│   ├── response_parser.py # Parses and displays AI responses
├── requirements.txt       # Dependency list
└── README.md              # Project documentation
```

---

## License
This project is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

### Terms
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

---

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the tool.

---

## Author
[Mrunal Gangurde](https://github.com/MrunalGangurde)

---

## Acknowledgments
- Streamlit for providing an excellent framework for building data-driven web applications.
- Google Generative AI for enabling the core AI functionality of the tool.
