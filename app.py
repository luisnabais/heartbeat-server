from flask import Flask, jsonify, request
import threading
import time
import requests
import os

app = Flask(__name__)

NTFY_TOPIC = os.getenv("NTFY_TOPIC", "your_topic")
NTFY_TOKEN = os.getenv("NTFY_TOKEN", "")
HEARTBEAT_TIMEOUT = int(os.getenv("HEARTBEAT_TIMEOUT", "600"))  # 10 minutos

# Dictionary: client_id -> last heartbeat timestamp
last_heartbeats = {}
alerted = set()  # To avoid spam

@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    data = request.get_json() or {}
    client_id = data.get("client_id") or request.args.get("client_id")
    if not client_id:
        return "Missing client_id", 400
    last_heartbeats[client_id] = time.time()
    alerted.discard(client_id)  # Reset alert if heartbeat received
    print(f"Heartbeat received from '{client_id}' em {time.strftime('%Y-%m-%d %H:%M:%S')}")
    return "OK", 200

@app.route("/status", methods=["GET"])
def status():
    now = time.time()
    data = {
        client_id: {
            "last_heartbeat": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts)),
            "seconds_since_last": int(now - ts)
        }
        for client_id, ts in last_heartbeats.items()
    }
    return jsonify(data)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


def monitor():
    while True:
        now = time.time()
        for client_id, last in last_heartbeats.items():
            if now - last > HEARTBEAT_TIMEOUT and client_id not in alerted:
                send_alert(client_id)
                alerted.add(client_id)
        time.sleep(10)

def send_alert(client_id):
    msg = f"🚨 [ALERT] Heartbeat not received from '{client_id}' in the last {HEARTBEAT_TIMEOUT//60} minutes!"
    headers = {}
    if NTFY_TOKEN:
        headers["Authorization"] = f"Bearer {NTFY_TOKEN}"
    try:
        requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=msg, headers=headers)
    except Exception as e:
        print(f"Error while sending ntfy alert: {e}")

if __name__ == "__main__":
    threading.Thread(target=monitor, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)