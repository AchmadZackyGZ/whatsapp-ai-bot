from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env
load_dotenv()

# Ambil API Key OpenRouter dari .env
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Inisialisasi Flask App
app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    """Handle incoming WhatsApp messages and respond with AI from OpenRouter"""
    
    incoming_msg = request.form.get("Body")  # Ambil isi pesan dari WhatsApp
    response = MessagingResponse()

    # Buat response dari OpenRouter
    ai_reply = generate_ai_response(incoming_msg)

    # Balas ke WhatsApp
    response.message(ai_reply)
    return str(response)

def generate_ai_response(user_input):
    """Mengambil response dari OpenRouter API"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",  # atau domain kamu
            "X-Title": "WhatsappBot"
        }

        data = {
            "model": "mistralai/mixtral-8x7b-instruct",  # kamu bisa ganti model di sini
            "messages": [
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            print("OpenRouter Error:", response.status_code, response.text)
            return "Maaf, bot sedang sibuk atau error."
    except Exception as e:
        print("OpenRouter Exception:", e)
        return "Maaf, saya tidak bisa merespons saat ini."

if __name__ == "__main__":
    app.run(debug=True)
