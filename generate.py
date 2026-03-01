import requests
import os

# 1. Налаштування
API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# Читаємо тему
try:
    with open('keywords.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if not lines:
        print("Список тем порожній!")
        exit()
    topic = lines[0].strip()
except Exception as e:
    topic = "Сучасний гаджет 2026"

# 2. Отримання тексту (з перевіркою на помилку)
def get_ai_text(t):
    try:
        r = requests.post(API_URL, headers=headers, json={"inputs": f"Write a long review about {t} in 2026: "}, timeout=10)
        text = r.json()[0]['generated_text'].split(t)[-1].strip()
        if len(text) < 50: raise Exception("Too short")
        return text
    except:
        # Якщо AI підвів, даємо якісну заготовку, щоб сайт не був пустим
        return f"Це один із найкращих пристроїв у категорії {t}. Він поєднує в собі інноваційний дизайн та неймовірну потужність, яка буде актуальною весь 2026 рік. Рекомендуємо до покупки!"

content = get_ai_text(topic)
safe_name = topic.replace(' ', '_').lower()
file_path = f"docs/{safe_name}.html"

# 3. Створення сторінки (Template)
if os.path.exists('template.html'):
    with open('template.html', 'r', encoding='utf-8') as f:
        temp = f.read()
    final_article = temp.replace('{{title}}', topic).replace('{{content}}', content)
    if not os.path.exists('docs'): os.makedirs('docs')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_article)

# 4. Додавання на головну (Index)
new_card = f"""
<a href="{file_path}" class="card">
    <div class="card-content">
        <h3>{topic}</h3>
        <div class="price">Детальний огляд</div>
        <p>Дізнайтеся все про характеристики та ціну {topic} у нашому новому AI-огляді.</p>
    </div>
</a>
"""

if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # Додаємо картку тільки якщо її ще немає
    if file_path not in index_html:
        updated_index = index_html.replace('', f'\n{new_card}')
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(updated_index)

# Видаляємо використану тему зі списку
with open('keywords.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines[1:])
