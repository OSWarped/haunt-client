import os
import shutil
import subprocess
import register
import motion_monitor


BOOT_CONFIG = "/boot/device.json"
LOCAL_CONFIG = "device.json"

# Step 1: Copy device.json from /boot if not already present
if os.path.exists(BOOT_CONFIG) and not os.path.exists(LOCAL_CONFIG):
    shutil.copy(BOOT_CONFIG, LOCAL_CONFIG)
    print("📁 Copied device.json from /boot")

# Step 2: Pair with Bluetooth speaker
print("🔗 Pairing with Bluetooth speaker...")
#subprocess.call(["python3", "bluetooth_pair.py"])

# Step 3: Setup motion monitors
print("📡 Starting Motion Sensor Monitoring...")
motion_monitor.start_motion_thread()


# Step 4: Register with central server
print("📡 Registering with central server...")
register.register_with_server()

# Step 5: Start the Flask server
print("🚀 Starting Flask server...")
subprocess.call(["python3", "main.py"])
