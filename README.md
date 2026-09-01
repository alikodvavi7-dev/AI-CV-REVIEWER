# 📄 AI CV Reviewer

A simple AI-powered CV reviewer built with Python, Streamlit and the Gemini API.

The app compares an uploaded CV with a job description and gives feedback on how well the candidate matches the role.

## Features

- Upload a CV as a PDF
- Enter a job title and job description
- Get an estimated ATS match score
- Find strengths and weaknesses in the CV
- Identify missing skills and keywords
- Get suggestions for improving the CV
- Get an interview recommendation

## Technologies

- Python
- Streamlit
- Gemini API
- PyPDF

## How it works

The app extracts text from the uploaded CV using PyPDF. It then sends the CV, job description and experience level to Gemini, which analyses the match and generates feedback.

## Run locally

Install the requirements:

pip install -r requirements.txt

Then run:

streamlit run cv_ai_project.py

You will also need to add your Gemini API key to .streamlit/secrets.toml