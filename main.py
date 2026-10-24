import os
import requests
from flask import Flask, request, jsonify
from database import init_db, create_kingdom, get_status

app = Flask(__name__)

init_db()

GREEN_API_URL = "https://api.green-api.com"
INSTANCE_ID = os.environ.get("INSTANCE_ID")
API_TOKEN = os.environ.get("API_TOKEN")

def send_whatsapp_message(chat_id, text):
    url = f"{GREEN_API_URL}/waInstance{INSTANCE_ID}/sendMessage/{API_TOKEN}"
    payload = {
        "chatId": chat_id,
        "message": text
    }
    requests.post(url, json=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    if data and data.get('typeWebhook') == 'incomingMessageReceived':
        message_data = data.get('messageData', {})
        sender_data = data.get('senderData', {})
        
        chat_id = sender_data.get('chatId')
        sender_id = sender_data.get('sender')
        
        text_message = ""
        if 'textMessageData' in message_data:
            text_message = message_data['textMessageData'].get('textMessage', '').strip()
        
        if text_message.startswith('!انشاء'):
            parts = text_message.split(maxsplit=1)
            name = parts[1] if len(parts) > 1 else "المملكة المجهولة"
            response = create_kingdom(sender_id, name)
            send_whatsapp_message(chat_id, response)
            
        elif text_message == '!مملكتي':
            response = get_status(sender_id)
            send_whatsapp_message(chat_id, response)
            
        elif text_message == '!اوامر':
            help_text = "📜 *أوامر لعبة الممالك:*\n\n🔹 `!انشاء [اسم المملكة]`\n🔹 `!مملكتي`"
            send_whatsapp_message(chat_id, help_text)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
