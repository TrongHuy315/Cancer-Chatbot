from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Địa chỉ API của LM Studio (giả sử nó là một API RESTful)
LM_API_URL = "http://127.0.0.1:1234/v1/chat/completions"  # Địa chỉ API thực tế từ LM Studio

# Thông tin xác thực API (nếu có)
#API_KEY = "your_api_key"  # API key bạn nhận được từ LM Studio

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
        
        # Gửi yêu cầu đến API của LM Studio
        headers = {
            #'Authorization': f'Bearer {API_KEY}',  # Nếu cần API Key
            'Content-Type': 'application/json'
        }

        payload = {
            'model': 'medical_llm',  # Tên model bạn đã tải về
            'messages': [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }

        # Gửi yêu cầu POST đến LM Studio API
        response = requests.post(LM_API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            response_data = response.json()
            model_response = response_data['choices'][0]['message']['content']
            return jsonify({
                'choices': [
                    {
                        'message': {
                            'role': 'assistant',
                            'content': model_response
                        }
                    }
                ]
            })
        else:
            return jsonify({"error": "Failed to get response from LM Studio API"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
