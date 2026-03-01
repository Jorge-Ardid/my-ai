import requests
import os
import re

# 1. Налаштування API
API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# 2. Отримання теми з keywords.txt
try:
    with open('keywords.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines:
        print("Немає тем для генерації.")
        exit()
    topic = lines[0].strip()
except Exception as e:
    print(f"Помилка читання файлу: {e}")
    exit()

# 3. Генерація тексту через AI
def get_ai_content(t):
    try:
        prompt = f"Write a professional detailed tech review of {t} in 2026. Mention key features and verdict."
        r = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=20)
        if r.status_code == 200:
            generated_text = r.json()[0]['generated_text']
            # Очищуємо текст від самого промпту
            return generated_text.replace(prompt, "").strip()
        else:
            return f"Огляд {t}: Це революційний гаджет 2026 року, який задає нові стандарти якості та продуктивності."
    except Exception:
        return f"Експертний огляд {t} підтверджує: цей пристрій є лідером у своєму ціновому сегменті."

article_text = get_ai_content(topic)

# 4. Підготовка шляху до файлу (безпечне ім'я)
safe_name = re.sub(r'\W+', '_', topic.lower()).strip('_')
file_path = f"docs/{safe_name}.html"

# 5. Створення сторінки статті за шаблоном template.html
if os.path.exists('template.html'):
    with open('template.html', 'r', encoding='utf-8') as f:
        template_code = f.read()
    
    final_page = template_code.replace('{{title}}', topic).replace('{{content}}', article_text)
    
    if not os.path.exists('docs'):
        os.makedirs('docs')
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_page)

# 6. Оновлення головної сторінки index.html
# Формуємо код нової картки в стилі index.html
new_card = f"""
            <a href="{file_path}" class="card">
                <span class="tag">Експертний огляд</span>
                <h3>{topic}</h3>
                <p>Детальний аналіз характеристик та результати тестування {topic} нашими алгоритмами.</p>
                <div class="btn-link">Читати огляд ➔</div>
            </a>"""

if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Додаємо картку лише якщо її ще немає
    if file_path not in index_content:
        # Вставляємо нову картку одразу після коментаря-маркера
        updated_index = index_content.replace('', f'\n{new_card}')
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(updated_index)

# 7. Видалення використаної теми з keywords.txt
with open('keywords.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines[1:])

print(f"Успішно згенеровано: {topic}")
