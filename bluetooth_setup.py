import subprocess
import time
import json
import os



def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"[Error] Failed to run command: {cmd}\n{e}")
        return ""

def start_pulseaudio():
    print("🌀 Starting PulseAudio service...")
    run_command("pulseaudio --start")

def wait_for_bluetooth(timeout=30):
    print("⏳ Waiting for Bluetooth interface...")
    for i in range(timeout):
        output = run_command("hciconfig")
        if "hci0" in output and "UP RUNNING" in output:
            print(f"✅ Bluetooth interface ready after {i + 1}s")
            return True
        time.sleep(1)
    print("❌ Bluetooth interface not found or not running.")
    return False

def connect_speaker(mac):
    print(f"🔗 Trying to connect to Bluetooth speaker {mac}...")
    cmds = [
        f"echo -e 'connect {mac}\nexit' | bluetoothctl",
    ]
    for cmd in cmds:
        result = run_command(cmd)
        if "Connection successful" in result or "Connection setup succeeded" in result:
            print("✅ Connected to Bluetooth speaker.")
            return True
    print("❌ Failed to connect to Bluetooth speaker.")
    return False

def set_default_sink(mac):
    print("🔊 Setting default audio sink...")
    sink_list = run_command("pactl list short sinks")
    for line in sink_list.splitlines():
        if mac.replace(":", "_").lower() in line.replace("-", "_").lower():
            sink_name = line.split()[1]
            set_cmd = f"pactl set-default-sink {sink_name}"
            run_command(set_cmd)
            print(f"✅ Default sink set to {sink_name}")
            return True
    print("❌ Could not find matching sink for MAC:", mac)
    return False

def wait_for_pulseaudio(timeout=30):
    print("⏳ Waiting for PulseAudio...")
    for i in range(timeout):
        info = run_command("pactl info")
        if "Server Name" in info:
            print(f"✅ PulseAudio is ready after {i + 1}s")
            return True
        time.sleep(1)
    print("❌ PulseAudio not ready.")
    return False

def setup_bluetooth_speaker():
    if not os.path.exists("device.json"):
        print("❌ Missing device.json")
        return

    with open("device.json") as f:
        config = json.load(f)
        mac = config.get("bluetooth_mac")
        if not mac:
            print("❌ No Bluetooth MAC address found in device.json")
            return

    if not wait_for_bluetooth():
        return
    start_pulseaudio()  
    if not wait_for_pulseaudio():
        return
    if connect_speaker(mac):
        set_default_sink(mac)

if __name__ == "__main__":
    setup_bluetooth_speaker()