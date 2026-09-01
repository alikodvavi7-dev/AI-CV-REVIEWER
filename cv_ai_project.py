import streamlit as st
from google import genai
from pypdf import PdfReader 
import re

st.title("📄 AI CV Reviewer")
st.caption("Compare your CV against a job description and get an AI-powered feedback in seconds")

st.divider()


api_key = st.secrets["GEMINI_API_KEY"]


file = st.file_uploader("Upload your CV PDF", type = ['pdf'])

job_title = st.text_input("Job Title")
job_description = st.text_area("Paste the Job Description", height = 250)
job_level = st.selectbox(
    "Experience Level",
    [
        "Graduate",
        "Junior",
        "Mid-Level",
        "Senior"
    ]
)

generate = st.button("Review my CV")

if generate:

    if not api_key:
        st.error("Please enter your Gemini API Key")

    elif file is None:
        st.error("Please upload your PDF File first")

    elif not job_title.strip():
        st.error("Please enter the job title.")

    elif not job_description.strip():
        st.error("Please paste the job description")

    else:
        client = genai.Client(api_key = api_key)

        try:
            reader = PdfReader(file)
            cv_text = ''

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    cv_text += text + "\n"

        except Exception:
            st.error("Couldnt read this PDF. Please upload a readable PDF File.")
            st.stop()

        if not cv_text.strip():
            st.error("No readable text was found in this PDF")
            st.stop()


        st.subheader("Extracted CV")
        st.write(cv_text[:1000])

        
        with st.spinner("Analyzing your CV..."):

           response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents = f"""
        You are an experienced recruitment consultant and CV reviewer.

Analyse the candidate's CV against the supplied job title,
job description and expected experience level.

Important rules:

- Base your assessment only on evidence present in the CV.
- Do not invent qualifications, experience, achievements or skills.
- Treat the ATS score as an informed estimate, not an official score.
- Clearly distinguish between missing information and confirmed weaknesses.
- Give practical and specific recommendations.
- Use concise professional language.

TARGET ROLE

Job title:
{job_title}

Expected experience level:
{job_level}

Job description:
{job_description}

CANDIDATE CV

{cv_text}

Return the review using exactly these headings:

## Estimated ATS Match Score
Give a score from 0 to 100 and explain the score in 2–3 sentences.

## Candidate Summary
Briefly summarise the candidate's suitability for the role.

## Strong Matches
List the candidate's strongest relevant skills, experience and qualifications.

## Missing or Weakly Demonstrated Requirements
Identify important requirements that are absent or insufficiently demonstrated.

## Important Matching Keywords
List relevant keywords already present in the CV.

## Missing Keywords
List important job-description keywords that are not clearly present in the CV.
Only suggest keywords that would be truthful for the candidate to use.

## CV Improvement Recommendations
Provide specific changes that would improve the CV for this role.

## Experience-Level Assessment
Explain whether the CV matches the selected experience level.

## Interview Recommendation
State whether you would recommend:
- Interview
- Consider
- Do not interview

Explain your decision.

## Final Match
Classify the application as:
- Strong match
- Moderate match
- Weak match
        """
        
    )


        st.success("Analysis Complete!")  

        score_match = re.search(
            r"(\d+)/100",
            response.text
        ) 

        if score_match:
            score = score_match.group(1)
            st.metric("Estimated ATS Match Score", f"{score}/100")

        st.subheader("Feedback from AI")
        st.markdown(response.text)

        