import subprocess
import json
import time

# Load the device config
with open("device.json") as f:
    config = json.load(f)

mac = config.get("bluetooth_mac")

if not mac:
    print("❌ No bluetooth_mac found in device.json")
    exit(1)

print(f"🔗 Attempting to pair with Bluetooth device: {mac}")

commands = [
    "power on",
    "agent on",
    "default-agent",
    f"trust {mac}",
    f"connect {mac}"
]

# Use bluetoothctl to send commands
process = subprocess.Popen(["bluetoothctl"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

for cmd in commands:
    process.stdin.write(f"{cmd}\n".encode())
    process.stdin.flush()
    time.sleep(1)  # give it a moment between commands

print("✅ Pairing script completed.")
