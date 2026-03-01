import requests
import os
import re

API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

try:
    with open('keywords.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines: exit()
    topic = lines[0].strip()
except:
    exit()

def get_ai_text(t):
    try:
        r = requests.post(API_URL, headers=headers, json={"inputs": f"Professional review of {t}:"}, timeout=20)
        return r.json()[0]['generated_text'].split("review of")[-1].strip()
    except:
        return f"Експертний огляд {t} показує, що це флагман 2026 року з потужними характеристиками."

content = get_ai_text(topic)
safe_name = re.sub(r'\W+', '_', topic.lower()).strip('_')
file_path = f"docs/{safe_name}.html"

# Створення статті
if os.path.exists('template.html'):
    with open('template.html', 'r', encoding='utf-8') as f:
        temp = f.read()
    if not os.path.exists('docs'): os.makedirs('docs')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(temp.replace('{{title}}', topic).replace('{{content}}', content))

# Оновлення головної
new_card = f"""
            <a href="{file_path}" class="card">
                <span class="tag">Експертний огляд</span>
                <h3>{topic}</h3>
                <p>Аналіз функцій та можливостей {topic} у реальних умовах використання.</p>
                <div class="btn-link">Читати огляд ➔</div>
            </a>"""

if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()
    if file_path not in idx:
        marker = ""
        if marker in idx:
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(idx.replace(marker, f"{marker}\n{new_card}"))

with open('keywords.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines[1:])
