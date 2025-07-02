# JD-RESUME Matcher
A smart AI python-based web application that matches a **Job Description(JD)** against multiple resumes and returns the **match percentage** for each resume. Powered by **OpenAI GPT-4** for intelligent text comparison and scoring.

-----

## Features

-Upload a Job Description File.
-Upload multiple resume files (PDF/TXT).
-Automatically compares each resume with JD.
-simple web interface (HTML/CSS + Flask backend)
- Built Using OpenAI's GPT model GPT-4 

-----

## Tech Stack

-**Backend** : Python, Flask
-**Frontend**: HTML, CSS
-**AI**      : OPENAI GPT-4
-**Other**   : PDF/TXT parsing, Resume-JD matching logic

## Project structure

jd_resume_matcher/
├── pycache/
│ ├── matcher.cpython-313.pyc
│ └── utils.cpython-313.pyc
├── static/
│ └── style.css
├── templates/
│ └── index.html
├── app.py # Flask app and route handling
├── matcher.py # Core logic for matching JD with resumes
├── utils.py # File processing utilities
├── requirements.txt # List of Python dependencies


---

## How to Run the App

1. **Install dependencies**:

pip install -r requirements.txt

2. **Set your OpenAI API Key**: 

setx OPENAI_API_KEY "your-openai-api-key" (the key is set globally)
or
set the key in local environment: $env:OPENAI_API_KEY = "openai-api-key"

3. **start the app**:

python app.py

4. **Open the server**:

Open your browser and go to http://127.0.0.1:5000

## Notes

-Ensure your OpenAI API key has access to gpt-4. Other models like gpt-4o and gpt-3.5 can also be used
-Match logic is based on semantic analysis of JD and resume content using OpenAI's models.
-Currently no database is used; all matching is done in-memory.

