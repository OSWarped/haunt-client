# 🎃 Haunt Client (Raspberry Pi Node)

This is the software that runs on each Raspberry Pi Zero 2 node in your haunted trail setup. Each Pi:

- Connects to a Bluetooth speaker
- Hosts a local HTTP server using Flask
- Plays MP3 sound effects on demand
- Reads its identity and pairing config from a `device.json` file
- Is fully headless and powered by USB battery packs

---

## 🧱 Project Structure

haunt-client/
├── bluetooth_pair.py # Handles Bluetooth speaker pairing
├── device.json # Per-Pi config (ignored by git)
├── main.py # Flask server for triggering sounds
├── requirements.txt # Python dependencies
├── sounds/ # Folder of MP3 files (ignored by git)
├── startup.py # Boot sequence (pair + Flask start)
├── .gitignore # Excludes device.json, sounds/


---

## 🧪 Local Development (Mac)

You can test this code on your Mac (minus Bluetooth pairing):

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate


2. Install Flask
bash
Copy
Edit
pip install Flask
3. Add test files
Add a device.json:

json
Copy
Edit
{
  "device_id": "pi01",
  "bluetooth_mac": "00:11:22:33:44:55",
  "label": "Graveyard Left",
  "volume": 85
}
Place a small test.mp3 file into the sounds/ folder

4. Run the server
bash
Copy
Edit
python main.py

🚀 Pi Deployment Instructions

Once you're ready to move this onto a Pi Zero 2, follow these steps:

📦 1. Install Required Packages (on each Pi)
sudo apt update
sudo apt install -y \
  python3-pip \
  mpg123 \
  bluetooth \
  bluez \
  bluez-tools \
  git

sudo apt update
sudo apt install python3-rpi.gpio

📁 2. Clone the Repository
cd /home/pi
git clone https://github.com/YOUR_USERNAME/haunt-client.git
cd haunt-client
mkdir sounds

🔗 3. Add device.json and MP3s

Copy device.json from the /boot partition (if it exists)

Add your sound files to the sounds/ folder

🔌 4. Enable Auto-Boot with systemd

Create a systemd unit file:

sudo nano /etc/systemd/system/haunt.service


Paste:

[Unit]
Description=Haunt Trail Pi Node
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/haunt-client/startup.py
WorkingDirectory=/home/pi/haunt-client
Restart=always
User=pi

[Install]
WantedBy=multi-user.target


Then enable it:

sudo systemctl daemon-reexec
sudo systemctl enable haunt.service
sudo systemctl start haunt.service



🔄 5. Files to Add to /boot (Before Booting a Pi)

device.json — per-device identity + Bluetooth MAC

ssh — (empty file) enables SSH

wpa_supplicant.conf — for WiFi config (optional)

✅ At Boot, Each Pi Will:

Copy device.json from /boot (if needed)

Pair with the correct Bluetooth speaker

Start the Flask server on port 5001

Be ready to play sounds via /play?file=filename.mp3

📡 Endpoints
Method	Endpoint	Description
GET	/	Basic status string
GET	/status	Returns device info and list of sounds
POST	/play?file=name.mp3	Plays the selected sound
GET	/test	Plays a test file (uses file=test.mp3)


🚧 To Do / Future Features

 Self-registration to central server via /register

 Sensor integration (e.g. PIR motion detection)

 Scene sequencing support

 WLED / lighting trigger support

 Logging + retry on Bluetooth failure

🔒 Git Ignore Notes

This repo intentionally excludes:

device.json — contains MAC addresses and per-Pi identity

sounds/ — large media files stored locally per device

See .gitignore for details.

🧙 Author

Blake Milam
GitHub: OSWarped