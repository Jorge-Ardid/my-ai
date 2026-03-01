import requests
import os
import re

# 1. Налаштування
API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

try:
    with open('keywords.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines: exit()
    topic = lines[0].strip()
except:
    exit()

# 2. Текст від AI
def get_ai_text(t):
    try:
        r = requests.post(API_URL, headers=headers, json={"inputs": f"Full tech review of {t}:"}, timeout=15)
        text = r.json()[0]['generated_text'].split(t)[-1].strip()
        return text if len(text) > 50 else f"Детальний аналіз {t} показує високий потенціал пристрою у 2026 році."
    except:
        return f"Цей пристрій — справжній прорив. Ми зібрали всі факти про {t} для вашої зручності."

content = get_ai_text(topic)
safe_name = re.sub(r'\W+', '_', topic.lower()).strip('_')
file_path = f"docs/{safe_name}.html"

# 3. Сторінка статті (template.html має бути наповненим!)
if os.path.exists('template.html'):
    with open('template.html', 'r', encoding='utf-8') as f:
        temp = f.read()
    if not os.path.exists('docs'): os.makedirs('docs')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(temp.replace('{{title}}', topic).replace('{{content}}', content))

# 4. Додавання "Багатої" картки в index.html
new_card = f"""
            <a href="{file_path}" class="card">
                <span class="tag">Експертний огляд</span>
                <h3>{topic}</h3>
                <p>Докладне тестування та аналіз ключових переваг {topic} від нашої нейромережі.</p>
                <div class="btn-link">Читати огляд ➔</div>
            </a>"""

if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()
    if file_path not in idx:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(idx.replace('', f'\n{new_card}'))

# Очищення списку тем
with open('keywords.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines[1:])
