import requests
from flask import Flask, request, jsonify
from huggingface_hub import InferenceClient

app = Flask(__name__)

# Lấy API token từ Hugging Face
API_TOKEN = "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"

# Tạo InferenceClient
client = InferenceClient(repo_id="blaze999/Medical-NER", token=API_TOKEN)

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
        
        # Sử dụng InferenceClient để gọi Hugging Face API
        response = client.text_generation(user_prompt, parameters={"max_length": 200, "temperature": 0.7})
        
        # Kiểm tra phản hồi từ mô hình
        if response:
            assistant_reply = response[0]['generated_text']  # Truy cập nội dung trả về từ mô hình
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
            return jsonify({"error": "Error from Hugging Face API", "details": "No response from model."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


