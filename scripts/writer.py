import sys
import requests
import os

def generate_post(trend):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
    
    prompt = f"""Write a 500-word technical blog post about '{trend}' with:
    - 1 executable code example
    - 3 key benefits
    - Future applications
    Format in Markdown with ## headings"""
    
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code != 200:
        print(f"API error: {response.status_code} - {response.text}")
        return None
    try:
        data = response.json()
        if not data or not isinstance(data, list) or 'generated_text' not in data[0]:
            print("API returned invalid data:", data)
            return None
        return data[0]['generated_text']
    except Exception as e:
        print("Error parsing API response:", e)
        print("Raw response:", response.text)
        return None

if __name__ == "__main__":
    trend = sys.argv[1] if len(sys.argv) > 1 else "AI in Web Development"
    result = generate_post(trend)
    if result:
        print(result)
    else:
        print("Blog post generation failed.")
