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
    return response.json()[0]['generated_text']

if __name__ == "__main__":
    trend = sys.argv[1] if len(sys.argv) > 1 else "AI in Web Development"
    print(generate_post(trend))
