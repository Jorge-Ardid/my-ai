import os
import requests
import random
from datetime import datetime

# Отримуємо ключ, який ви вже додали в Secrets
HF_TOKEN = os.getenv("HF_TOKEN")
# Використовуємо модель, яка краще пише англійською для Google
MODEL = "google/flan-t5-large"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# Сюди ви потім вставите своє реальне партнерське посилання
AFFILIATE_LINK = "https://example.com/?ref=yourid"

def generate_article(keyword):
    prompt = f"Write a detailed blog post about {keyword}. Include benefits and conclusion."
    
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt, "parameters": {"max_length": 500}}
        )
        data = response.json()
        
        # Перевірка на успішну відповідь від нейромережі
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        return "Content is being updated, please refresh in a few minutes."
    except Exception as e:
        return f"Generation pause: {str(e)}"

def create_html(title, content):
    # Читаємо ваш шаблон
    with open("template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # ВАЖЛИВО: замінюємо маленькі літери, як у вашому template.html
    return template.replace("{{title}}", title)\
                   .replace("{{content}}", content)\
                   .replace("{{AFFILIATE}}", AFFILIATE_LINK)

def main():
    # Читаємо теми зі списку
    if not os.path.exists("keywords.txt"):
        print("Error: keywords.txt not found")
        return

    with open("keywords.txt", "r", encoding="utf-8") as f:
        keywords = [line.strip() for line in f.readlines() if line.strip()]

    if not keywords:
        print("Error: keywords.txt is empty")
        return

    # Обираємо випадкову тему
    keyword = random.choice(keywords)
    print(f"Generating article for: {keyword}")
    
    article = generate_article(keyword)

    # Створюємо фінальний HTML
    html_content = create_html(keyword, article)

    # Зберігаємо в папку docs для сайту
    os.makedirs("docs", exist_ok=True)
    
    # Робимо назву файлу зручною для посилань
    safe_name = keyword.lower().replace(' ', '_')
    filename = f"docs/{safe_name}.html"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    main()
