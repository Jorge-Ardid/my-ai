import requests
import os

# 1. Читаємо тему
try:
    with open('keywords.txt', 'r') as f:
        topic = f.readline().strip()
    if not topic: topic = "Best Tech Gadgets 2026"
except:
    topic = "Smart Home Devices"

# 2. Потужніша нейромережа (Mistral)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def get_text(topic):
    prompt = f"Write a professional product review about {topic}. Focus on benefits."
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 250}})
        result = response.json()
        if isinstance(result, list):
            return result[0]['generated_text'].split(prompt)[-1].strip()
        return "Expert review is being updated. Stay tuned!"
    except:
        return "Check out the best deals on this product below."

# 3. Генеруємо контент
article_text = get_text(topic)

# 4. Оновлюємо дизайн
if os.path.exists('template.html'):
    with open('template.html', 'r') as f:
        html = f.read()
    
    html = html.replace('{{title}}', topic)
    html = html.replace('{{content}}', article_text)
    
    # Зберігаємо результат
    file_path = f"docs/{topic.replace(' ', '_').lower()}.html"
    with open(file_path, 'w') as f:
        f.write(html)
    print(f"Done! Created: {file_path}")
