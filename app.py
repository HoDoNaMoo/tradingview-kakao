from flask import Flask, request
import requests
import json

app = Flask(__name__)

ACCESS_TOKEN = "Ns02uy-de7VV5Imh4-O8R8Ym2SnbiUmrAAAAAQoXE08AAAGd614z9dQORDI69jWm"
REFRESH_TOKEN = "IRf-RuzvVm7nASTlg3Ej7pyreOxQuoS4AAAAAgpXE08AAAGd614z7NQORDI69jWm"
CLIENT_ID = "7925f1bec75b6712859631339210441d"
CLIENT_SECRET = "elU9tgpvg6BKdtSl3Heee5UCxLy2FUsw"

def refresh_access_token():
    global ACCESS_TOKEN
    try:
        res = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "refresh_token",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "refresh_token": REFRESH_TOKEN
            },
            timeout=10
        )
        new_token = res.json().get("access_token")
        if new_token:
            ACCESS_TOKEN = new_token
    except Exception as e:
        print(f"Token refresh failed: {e}")

def send_kakao(message):
    global ACCESS_TOKEN
    try:
        res = requests.post(
            "https://kapi.kakao.com/v2/api/talk/memo/default/send",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
            data={"template_object": json.dumps({
                "object_type": "text",
                "text": message,
                "link": {"web_url": "https://www.tradingview.com"}
            })},
            timeout=10
        )
        print(f"Kakao response: {res.status_code} {res.text}")
        if res.status_code == 401:
            refresh_access_token()
            res2 = requests.post(
                "https://kapi.kakao.com/v2/api/talk/memo/default/send",
                headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
                data={"template_object": json.dumps({
                    "object_type": "text",
                    "text": message,
                    "link": {"web_url": "https://www.tradingview.com"}
                })},
                timeout=10
            )
            print(f"Kakao retry response: {res2.status_code} {res2.text}")
    except Exception as e:
        print(f"Kakao send failed: {e}")

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

    send_kakao(message)
    return "OK", 200

@app.route("/health", methods=["GET"])
def health():
    return "alive", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
