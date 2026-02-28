import os
import requests
import random
from datetime import datetime

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "google/flan-t5-large"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

AFFILIATE_LINK = "https://example.com/?ref=yourid"

def generate_article(keyword):
    prompt = f"Write a detailed SEO blog post about {keyword}. Include introduction, benefits, comparison, and conclusion."
    
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"inputs": prompt}
    )

    data = response.json()
    
    if isinstance(data, list):
        return data[0]["generated_text"]
    return "Content generation failed."

def create_html(title, content):
    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()

    return template.replace("{{TITLE}}", title)\
                   .replace("{{CONTENT}}", content)\
                   .replace("{{AFFILIATE}}", AFFILIATE_LINK)

def main():
    with open("keywords.txt", "r", encoding="utf-8") as f:
        keywords = f.readlines()

    keyword = random.choice(keywords).strip()
    article = generate_article(keyword)

    html_content = create_html(keyword, article)

    os.makedirs("docs", exist_ok=True)

    filename = f"docs/{keyword.replace(' ', '_')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Generated:", filename)

if __name__ == "__main__":
    main()
