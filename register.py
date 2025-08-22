import json
import subprocess
import socket
import requests
import shutil
import os

def is_speaker_connected(mac):
    if not shutil.which("bluetoothctl"):
        print("⚠️ bluetoothctl not found — skipping speaker check")
        return False
    try:
        output = subprocess.check_output(["bluetoothctl", "info", mac])
        return "Connected: yes" in output.decode()
    except subprocess.CalledProcessError:
        return False

def get_local_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "unknown"

def register_with_server():
    try:
        with open("device.json") as f:
            config = json.load(f)

        # Get server URL from device.json or fall back to default
        base_url = config.get("server_url", "http://10.0.0.1:5050")
        full_url = f"{base_url}/api/register"

        payload = {
            "device_id": config.get("device_id", "").lower(),
            "label": config.get("label"),
            "bluetooth_mac": config.get("bluetooth_mac"),
            "speaker_connected": is_speaker_connected(config.get("bluetooth_mac")),
            "ip": get_local_ip(),
            "sounds": get_sound_files()
        }

        response = requests.post(full_url, json=payload, timeout=5)

        if response.status_code == 200:
            print(f"✅ Registered with central server as {payload['device_id']}")
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ Error in register.py: {e}")

def get_sound_files():
    sound_dir = "sounds"  # or wherever your MP3s are stored
    return [f for f in os.listdir(sound_dir) if f.lower().endswith(".mp3")]

