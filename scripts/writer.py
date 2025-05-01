import sys
import requests
import os
import time

def generate_ai_content(trend):
    """Generate content using free Hugging Face API"""
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
    
    prompt = f"""
    Write a 500-word technical blog post about '{trend}' with:
    - 1 executable code example
    - 3 key benefits with real-world examples
    - Future industry applications
    - SEO-friendly subheadings
    Format in Markdown with ## headings
    """
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=30)
            response.raise_for_status()
            return response.json()[0]['generated_text']
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return f"# {trend}\n\n⚠️ Failed to generate content: {str(e)}"
            time.sleep(2 ** attempt)  # Exponential backoff

if __name__ == "__main__":
    trend = sys.argv[1] if len(sys.argv) > 1 else "Modern Web Development"
    print(generate_ai_content(trend))
