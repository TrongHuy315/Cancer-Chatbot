import requests
import json

API_URL = "https://cancer-chatbot-fdg3.onrender.com/v1/chat/completions"

payload = {
    "model": "medical_llm",
    "messages": [
        {"role": "system", "content": "You are a helpful and friendly assistant. Please answer briefly."},
        {"role": "user", "content": "What is hepatitis?"}
    ],
    "temperature": 0.7,
    "max_tokens": 500,
    "stream": False
}

headers = {"Content-Type": "application/json"}

response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    print("Model:", response.json()["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code} - {response.text}")
