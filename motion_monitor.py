import RPi.GPIO as GPIO
import json
import time
import threading
import requests
from datetime import datetime

# Load config
with open("device.json") as f:
    config = json.load(f)

DEVICE_ID = config.get("device_id")
SERVER_URL = config.get("server_url", "http://10.0.0.1:5000")
SENSOR_PINS = config.get("sensor_pins", [])

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in SENSOR_PINS:
    GPIO.setup(pin, GPIO.IN)

def send_motion_event(pin):
    timestamp = datetime.now().isoformat()
    data = {
        "device_id": DEVICE_ID,
        "gpio": pin,
        "timestamp": timestamp
    }

    try:
        url = f"{SERVER_URL}/api/motion"
        response = requests.post(url, json=data, timeout=3)
        if response.status_code == 200:
            print(f"📡 Motion detected on GPIO {pin} — reported successfully.")
        else:
            print(f"⚠️ Failed to report motion on GPIO {pin}: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending motion event: {e}")

def motion_detected_callback(pin):
    print(f"👻 Motion detected on GPIO {pin}")
    send_motion_event(pin)

def start_monitoring():
    for pin in SENSOR_PINS:
        GPIO.add_event_detect(pin, GPIO.RISING, callback=motion_detected_callback, bouncetime=500)
    print("👂 Motion sensor monitoring started.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Stopping motion monitoring...")
    finally:
        GPIO.cleanup()

# Run as a thread if imported
def start_motion_thread():
    thread = threading.Thread(target=start_monitoring, daemon=True)
    thread.start()
