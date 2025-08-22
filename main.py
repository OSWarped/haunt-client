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


@app.route("/api/play", methods=["POST"])
def play_sound():
    data = request.json
    sound_file = data.get("sound_file")
    sound_path = os.path.join("sounds", sound_file)

    if os.path.exists(sound_path):
        print(f"🔊 Playing sound: {sound_file}")
        os.system(f"mpg123 '{sound_path}' &")
        return jsonify({"status": "playing"}), 200
    else:
        return jsonify({"error": "Sound not found"}), 404

@app.route("/test")
def test():
    return play()
    
def check_for_commands():
    try:
        url = f"{SERVER_URL}/api/commands/{DEVICE_ID}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            commands = response.json().get("commands", [])
            for cmd in commands:
                if cmd["command"] == "play":
                    play_sound(cmd["filename"])
    except Exception as e:
        print(f"❌ Error checking for commands: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
