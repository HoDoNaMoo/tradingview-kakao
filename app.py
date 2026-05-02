from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "5fua3zbP312nz-4IIAMXsmBO_XGMBHfuAAAAAQoXFp8AAAGd5-IqD9O0RDI69jWm"
REFRESH_TOKEN = "Pb5ibPcNu__RV8dhpw1omg-YhWoCb5dKAAAAAgoXFp8AAAGd5-IqC9O0RDI69jWm"
CLIENT_ID = "7925f1bec75b6712859631339210441d"
CLIENT_SECRET = "elU9tgpvg6BKdtSl3Heee5UCxLy2FUsw"

def refresh_access_token():
    global ACCESS_TOKEN
    res = requests.post("https://kauth.kakao.com/oauth/token", data={
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
    })
    ACCESS_TOKEN = res.json().get("access_token", ACCESS_TOKEN)

def send_kakao(message):
    res = requests.post(
        "https://kapi.kakao.com/v2/api/talk/memo/default/send",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        data={"template_object": f'{{"object_type":"text","text":"{message}","link":{{"web_url":"https://www.tradingview.com"}}}}'}
    )
    if res.status_code == 401:
        refresh_access_token()
        send_kakao(message)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}
    message = data.get("text", str(data))
    send_kakao(message)
    return "OK", 200

@app.route("/health", methods=["GET"])
def health():
    return "alive", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)