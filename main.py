from flask import Flask, request, jsonify
import subprocess
import os
import json
import socket

app = Flask(__name__)
SOUND_FOLDER = "./sounds"

# Load device config
with open("device.json") as f:
    config = json.load(f)

@app.route("/")
def home():
    return f"🎃 Pi {config['device_id']} is online!"

@app.route("/status")
def status():
    # Count MP3s
    mp3s = [f for f in os.listdir(SOUND_FOLDER) if f.endswith(".mp3")]
    ip_address = socket.gethostbyname(socket.gethostname())
    # Check if speaker is connected
    try:
        bt_output = subprocess.check_output(["bluetoothctl", "info", config["bluetooth_mac"]])
        connected = "Connected: yes" in bt_output.decode()
    except subprocess.CalledProcessError:
        connected = False

    return jsonify({
        "device_id": config.get("device_id"),
        "ip": ip_address,
        "label": config.get("label"),
        "bluetooth_mac": config.get("bluetooth_mac"),
        "speaker_connected": connected,
        "mp3_count": len(mp3s),
        "files": mp3s
    })


@app.route("/play", methods=["POST"])
def play():
    mp3 = request.args.get("file")
    path = os.path.join(SOUND_FOLDER, mp3)
    if not os.path.exists(path):
        return f"File not found: {mp3}", 404

    subprocess.call(["pkill", "mpg123"])  # stop current audio
    subprocess.Popen(["mpg123", "-f", str(config["volume"] * 100), path])
    return f"Playing {mp3}", 200

@app.route("/test")
def test():
    return play()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
