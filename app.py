import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Đặt API URL của Hugging Face (ví dụ sử dụng GPT-3.5 hoặc GPT-4 model)
API_URL = "https://huggingface.co/blaze999/Medical-NER"

# Lấy API token từ Hugging Face
API_TOKEN = "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"

# Đặt header cho yêu cầu
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        system_prompt = ""
        user_prompt = ""
        
        # Lấy nội dung từ các messages
        for message in messages:
            if message['role'] == 'system':
                system_prompt = message.get('content', '')
            elif message['role'] == 'user':
                user_prompt = message.get('content', '')
        
        # Tạo payload gửi đến Hugging Face
        payload = {
            "inputs": user_prompt,  # Đầu vào là thông điệp của người dùng
            "parameters": {
                "max_length": 200,  # Tùy chỉnh theo yêu cầu
                "temperature": 0.7
            }
        }
        
        # Gửi yêu cầu đến Hugging Face API
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            model_response = response.json()
            assistant_reply = model_response[0]['generated_text']  # Điều chỉnh theo cấu trúc trả về của Hugging Face model
            return jsonify({
                'choices': [
                    {
                        'message': {
                            'role': 'assistant',
                            'content': assistant_reply
                        }
                    }
                ]
            })
        else:
            return jsonify({"error": "Error from Hugging Face API", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

