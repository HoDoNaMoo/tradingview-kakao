from flask import Flask, request
import requests
import json

app = Flask(__name__)

BOT_TOKEN = "8743038044:AAEyd4qSaAY1kNB1VrLKoPZcYqIjoD8VoBQ"
CHAT_ID = "7173974185"

def send_telegram(message):
    try:
        res = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": message},
            timeout=10
        )
        print(f"Telegram response: {res.status_code} {res.text}")
    except Exception as e:
        print(f"Telegram send failed: {e}")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True, silent=True)
        if data:
            message = data.get("text", str(data))
        else:
            message = request.get_data(as_text=True)
    except:
        message = request.get_data(as_text=True)
    send_telegram(message)
    return "OK", 200

@app.route("/health", methods=["GET"])
def health():
    return "alive", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
