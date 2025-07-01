import os
import json
import openai
import pandas as pd
from utils import extract_text_from_file
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load API key from environment
assert os.getenv("OPENAI_API_KEY"), "Set OPENAI_API_KEY"
openai.api_key = os.getenv("OPENAI_API_KEY")

def score_resume_llm(jd_text, resume_text, model="gpt-3.5-turbo"):
    prompt = [
        {"role": "system", "content": "You are a recruiter. Rate how well this resume fits the job description on a scale 0–100. Return JSON {\"score\": <int>}."},
        {"role": "user", "content": jd_text},
        {"role": "user", "content": resume_text},
    ]
    resp = openai.ChatCompletion.create(model=model, messages=prompt, temperature=0)
    content = resp.choices[0].message.content.strip()
    try:
        return int(json.loads(content)["score"])
    except:
        return int(''.join(filter(str.isdigit, content)) or 0)

def prefilter(jd_text, resume_texts, top_n=5):
    """Pick top_n resumes by cosine similarity to JD."""
    vec = TfidfVectorizer(stop_words='english')
    all_texts = [jd_text] + resume_texts
    tfidf = vec.fit_transform(all_texts)
    jd_vec = tfidf[0]
    res_vecs = tfidf[1:]
    sims = cosine_similarity(res_vecs, jd_vec).flatten()
    ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
    return [i for i, _ in ranked[:top_n]]

def main():
    os.makedirs("output", exist_ok=True)
    jd = extract_text_from_file("job_description.txt")
    resumes = os.listdir("resumes")
    texts = [extract_text_from_file(f"resumes/{r}") for r in resumes]

    # Pre-filter to top 5 resumes
    idxs = prefilter(jd, texts, top_n=min(5, len(texts)))
    # :contentReference[oaicite:1]{index=1}

    results = []
    for i in idxs:
        fname = resumes[i]
        txt = texts[i]
        score = score_resume_llm(jd, txt)
        results.append({"resume": fname, "score": score})

    df = pd.DataFrame(results).sort_values("score", ascending=False)
    df.to_csv("output/results.csv", index=False)
    print(df)

if __name__ == "__main__":
    main()