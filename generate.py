import requests
import os

# 1. Налаштування
API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b"
token = os.getenv('HF_TOKEN')
headers = {"Authorization": f"Bearer {token}"} if token else {}

# Читаємо тему
try:
    with open('keywords.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    topic = lines[0].strip() if lines else "Новий гаджет 2026"
except:
    topic = "Smart Tech 2026"

# 2. Отримання тексту
def get_content(t):
    try:
        r = requests.post(API_URL, headers=headers, json={"inputs": f"Review of {t}: "}, timeout=10)
        return r.json()[0]['generated_text'].split(t)[-1].strip()
    except:
        return f"Це детальний огляд {t}. Ми протестували пристрій і готові підтвердити його якість."

content = get_content(topic)
safe_name = topic.replace(' ', '_').lower()
file_path = f"docs/{safe_name}.html"

# 3. Створення сторінки (якщо є шаблон)
if os.path.exists('template.html'):
    with open('template.html', 'r', encoding='utf-8') as f:
        temp = f.read()
    if not os.path.exists('docs'): os.makedirs('docs')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(temp.replace('{{title}}', topic).replace('{{content}}', content))

# 4. Додавання картки на головну (index.html)
new_card = f"""
<a href="{file_path}" class="card">
    <div class="card-content">
        <h3>{topic}</h3>
        <p>Дізнайтеся більше про можливості {topic} у нашому огляді.</p>
        <div class="price-tag">Читати огляд ➔</div>
    </div>
</a>
"""

if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        index_data = f.read()
    
    if file_path not in index_data:
        # Шукаємо мітку і вставляємо ПІСЛЯ неї
        updated_index = index_data.replace('', f'\n{new_card}')
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(updated_index)

# Очищення списку тем
if 'lines' in locals() and len(lines) > 0:
    with open('keywords.txt', 'w', encoding='utf-8') as f:
        f.writelines(lines[1:])
