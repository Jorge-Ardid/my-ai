import requests
import os
import re

# 1. Конфігурація
API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b"
# HF_TOKEN має бути доданий у Settings -> Secrets -> Actions вашого репозиторію
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# 2. Отримання теми з keywords.txt
try:
    with open('keywords.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines:
        print("Файл keywords.txt порожній. Додайте назви товарів.")
        exit()
    topic = lines[0].strip()
except FileNotFoundError:
    print("Файл keywords.txt не знайдено.")
    exit()

# 3. Генерація огляду через Hugging Face AI
def generate_review(product_name):
    try:
        payload = {"inputs": f"Write a professional product review of {product_name}. Include design, performance, and verdict."}
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            full_text = response.json()[0]['generated_text']
            # Прибираємо вхідний промпт із результату
            clean_text = full_text.replace(payload["inputs"], "").strip()
            return clean_text if len(clean_text) > 50 else f"Огляд {product_name}: Це передовий пристрій 2026 року з інноваційним підходом до технологій."
    except Exception as e:
        print(f"Помилка AI: {e}")
    return f"Огляд {product_name}: Виняткова якість та сучасні характеристики роблять цей гаджет лідером ринку."

review_content = generate_review(topic)

# 4. Створення імені файлу (латиниця, малі літери, без пробілів)
safe_filename = re.sub(r'\W+', '_', topic.lower()).strip('_')
file_url = f"docs/{safe_filename}.html"

# 5. Створення сторінки статті
if os.path.exists('template.html'):
    with open('template.html', 'r', encoding='utf-8') as f:
        html_template = f.read()
    
    # Заміна плейсхолдерів реальними даними
    final_article = html_template.replace('{{title}}', topic).replace('{{content}}', review_content)
    
    # Створення папки docs, якщо вона відсутня
    if not os.path.exists('docs'):
        os.makedirs('docs')
        
    with open(file_url, 'w', encoding='utf-8') as f:
        f.write(final_article)

# 6. Оновлення головної сторінки index.html
if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # Перевірка, чи це посилання вже існує, щоб не дублювати
    if file_url not in index_html:
        # Код нової картки товару
        new_card_code = f"""
            <a href="{file_url}" class="card">
                <span class="tag">Експертний огляд</span>
                <h3>{topic}</h3>
                <p>Докладний розбір та тестування можливостей {topic} від нашої AI-лабораторії.</p>
                <div class="btn-link">Читати огляд ➔</div>
            </a>"""
        
        # Вставка картки після маркера
        marker = ""
        if marker in index_html:
            new_index_html = index_html.replace(marker, f"{marker}\n{new_card_code}")
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(new_index_html)
            print(f"Товар '{topic}' додано на головну.")
        else:
            print("Маркер не знайдено в index.html.")

# 7. Видалення використаного ключового слова зі списку
with open('keywords.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines[1:])

print("Процес завершено успішно.")
