import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Configuración limpia de API
BOT_TOKEN = "7618389972:AAFe4Nsrn79M4aNatYLmn0CGfIfcDRK7eIo"
FLOWISE_URL = "https://cloud.flowiseai.com/api/v1/prediction/01f2874a-db1b-4ac5-805b-723973ac0d83"

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    
    if not data or "message" not in data:
        return "OK", 200
        
    chat_id = data["message"]["chat"]["id"]
    user_message = data["message"].get("text", "")
    
    if not user_message:
        return "OK", 200

    # Enviamos la pregunta con el formato oficial de la API
    try:
        flowise_response = requests.post(
            FLOWISE_URL, 
            json={"question": user_message},
            headers={"Content-Type": "application/json"}
        )
        
        try:
            # La API devuelve un JSON y la respuesta de la IA viene en 'text'
            roxy_reply = flowise_response.json().get("text", "¡Uh gordi, me colapsé! Hablame de nuevo.")
        except:
            roxy_reply = "Perdón gordi, me devolvieron datos raros de la base."
            
    except Exception as e:
        roxy_reply = "Perdón che, ando con algunos problemas de comunicación con mi cerebro."

    # Enviamos la respuesta limpia a Telegram
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": roxy_reply
    }
    
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print(f"Error al enviar a Telegram: {e}")

    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
