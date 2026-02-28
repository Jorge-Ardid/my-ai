import requests
import os

# 1. Налаштування нейромережі
API_URL = "https://api-inference.huggingface.co/models/google/gemma-7b"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

# 2. Отримуємо тему
try:
    with open('keywords.txt', 'r') as f:
        lines = f.readlines()
    topic = lines[0].strip() if lines else "Best Tech 2026"
except:
    topic = "Latest Gadgets"

# 3. Функція генерації тексту
def generate_review(t):
    try:
        r = requests.post(API_URL, headers=headers, json={"inputs": f"Write a professional review of {t}: "})
        text = r.json()[0]['generated_text']
        return text.split(t)[-1].strip() # Очищаємо від повторів
    except:
        return "Це преміальний огляд товару. Наші експерти готують детальний звіт."

content = generate_review(topic)

# 4. Оновлюємо дизайн (Template)
if os.path.exists('template.html'):
    with open('template.html', 'r') as f:
        temp = f.read()
    
    # Створюємо статтю
    final_html = temp.replace('{{title}}', topic).replace('{{content}}', content)
    
    # Зберігаємо у папку docs
    file_path = f"docs/{topic.replace(' ', '_').lower()}.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    # Оновлюємо index.html, щоб він виглядав професійно
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            index = f.read()
        new_link = f'<li><a href="{file_path}">{topic}</a></li>'
        if new_link not in index:
            index = index.replace('</ul>', f'{new_link}</ul>')
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(index)
