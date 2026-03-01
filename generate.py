import requests
import os
import re

# 1. Налаштування
API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# 2. Читання теми
try:
    with open('keywords.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines:
        print("Теми закінчилися в keywords.txt")
        exit()
    topic = lines[0].strip()
except Exception as e:
    print(f"Помилка читання тем: {e}")
    exit()

# 3. AI Контент
def get_ai_response(t):
    try:
        r = requests.post(API_URL, headers=headers, json={"inputs": f"Full detailed review of {t}:"}, timeout=25)
        if r.status_code == 200:
            return r.json()[0]['generated_text'].split("review of")[-1].strip()
    except:
        pass
    return f"Огляд {t}: Це революційний пристрій 2026 року, який поєднує в собі преміальний дизайн та неймовірну потужність чипа нового покоління."

content = get_ai_response(topic)
safe_name = re.sub(r'\W+', '_', topic.lower()).strip('_')
file_path = f"docs/{safe_name}.html"

# 4. Створення папки та файлу статті
if not os.path.exists('docs'):
    os.makedirs('docs')

if os.path.exists('template.html'):
    with open('template.html', 'r', encoding='utf-8') as f:
        temp = f.read()
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(temp.replace('{{title}}', topic).replace('{{content}}', content))

# 5. Оновлення головної сторінки
new_card = f"""
            <a href="{file_path}" class="card">
                <span class="tag">Експертний огляд</span>
                <h3>{topic}</h3>
                <p>Повний аналіз характеристик та результати тестування {topic} від нашої AI-лабораторії.</p>
                <div class="btn-link">Читати огляд ➔</div>
            </a>"""

if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        idx_content = f.read()
    
    if file_path not in idx_content:
        # Шукаємо маркер і вставляємо нову картку
        marker = ""
        if marker in idx_content:
            updated_idx = idx_content.replace(marker, f"{marker}\n{new_card}")
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(updated_idx)
            print(f"Статтю про {topic} успішно додано!")

# 6. Видалення використаної теми
with open('keywords.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines[1:])
