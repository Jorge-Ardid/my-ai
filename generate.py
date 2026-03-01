import requests
import os
import re

# 1. Налаштування
API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# 2. Отримання теми
try:
    if not os.path.exists('keywords.txt'):
        print("Файл keywords.txt відсутній!")
        exit()
        
    with open('keywords.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        print("Список тем порожній.")
        exit()
        
    topic = lines[0].strip()
except Exception as e:
    print(f"Помилка читання тем: {e}")
    exit()

# 3. Генерація тексту через AI
def get_ai_text(product):
    try:
        payload = {"inputs": f"Write a professional technical review of {product} in 2026. Focus on specs and design."}
        r = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        if r.status_code == 200:
            return r.json()[0]['generated_text'].split("2026.")[-1].strip()
    except Exception as e:
        print(f"Помилка API: {e}")
    return f"Огляд {product}: Це флагманський пристрій 2026 року з підтримкою AI та інноваційним дисплеєм."

text_content = get_ai_text(topic)
safe_name = re.sub(r'\W+', '_', topic.lower()).strip('_')

# КРИТИЧНО: Шлях до файлу всередині docs
if not os.path.exists('docs'):
    os.makedirs('docs')
    print("Папку docs створено примусово.")

file_path = f"docs/{safe_name}.html"

# 4. Створення сторінки статті
if os.path.exists('template.html'):
    with open('template.html', 'r', encoding='utf-8') as f:
        temp = f.read()
    
    final_html = temp.replace('{{title}}', topic).replace('{{content}}', text_content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Файл {file_path} створено.")

# 5. Оновлення головної сторінки index.html
if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()
    
    if file_path not in idx:
        new_card = f"""
            <a href="{file_path}" class="card">
                <span class="tag">Експертний огляд</span>
                <h3>{topic}</h3>
                <p>Аналіз характеристик та можливостей {topic} від нашої AI-лабораторії.</p>
                <div class="btn-link">Читати огляд ➔</div>
            </a>"""
            
        marker = ""
        if marker in idx:
            updated_idx = idx.replace(marker, f"{marker}\n{new_card}")
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(updated_idx)
            print(f"Додано посилання на головну.")

# 6. Видалення використаного ключового слова
with open('keywords.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines[1:])
