import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from utils import extract_text_from_file
from matcher import score_resume_llm, prefilter
import openai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        jd_file = request.files['jd']
        resumes = request.files.getlist('resumes')

        jd_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(jd_file.filename))
        jd_file.save(jd_path)
        jd_txt = extract_text_from_file(jd_path)

        texts = []
        names = []
        for r in resumes:
            path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(r.filename))
            r.save(path)
            names.append(r.filename)
            texts.append(extract_text_from_file(path))

        idxs = prefilter(jd_txt, texts, top_n=len(texts))
        scored = []
        for i in idxs:
            score = score_resume_llm(jd_txt, texts[i])
            scored.append((names[i], score))

        results = sorted(scored, key=lambda x: x[1], reverse=True)

    return render_template('index.html', results=results)

if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    app.run(debug=True)