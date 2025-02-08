# AdvanceSpyware---ETH-Project
This repository contains an advanced spyware project developed for an Ethical Hacking course. It is designed for educational and research purposes only and demonstrates various keylogging, system monitoring, and data exfiltration techniques while ensuring encryption for security.  

⚖️ Advanced Spyware (For Educational Purposes Only)

📄 Description

This project is a proof-of-concept keylogger and system monitoring tool, developed as part of my Ethical Hacking coursework. It demonstrates how attackers use spyware for data exfiltration and how security professionals can detect and mitigate such threats.

🚨 This tool is for educational and research purposes only. Unauthorized use is strictly prohibited.

⚡ Features

✔️ Keylogging: Captures keystrokes using pynput
✔️ System Information Extraction: Records IP address, OS details, and hardware information
✔️ Clipboard Data Extraction: Reads copied text from the clipboard
✔️ Microphone Audio Recording: Records a short audio clip
✔️ Screenshot Capture: Periodic screenshots for monitoring
✔️ Encryption: Logs are securely encrypted using cryptography.fernet
✔️ Automated Email Sending: Encrypted logs are sent via email
✔️ Decryption Support: Provided decryption script for analysis

🛠️ Installation & Setup

1️⃣ Prerequisites

Ensure you have Python 3.x installed. Install required dependencies using:

pip install -r requirements.txt

2️⃣ Configuring Gmail SMTP for Sending Logs

Enable Less Secure Apps (or use an App Password) in your Gmail account.

Edit the spyware.py script and update:

email_address = "your_email@gmail.com"
password = "your_app_password"
toaddr = "your_email@gmail.com"

Save the file.

3️⃣ Running the Spyware (For Ethical Testing Only)

To start data collection, run:

python spyware.py

Press ESC to stop keylogging.

4️⃣ Decrypting Captured Data

To decrypt and access logs:

python decrypt.py

⚠ Disclaimer

This project is strictly for educational purposes as part of an Ethical Hacking course.

❌ Unauthorized use is illegal and violates cybersecurity laws.

🚫 I do not hold responsibility for any misuse.

🔐 Deploy only in controlled environments for ethical cybersecurity research.

🌟 Use responsibly. Stay ethical. Protect cybersecurity.

📜 License

This project is intended for academic use only and should not be used for malicious activities. Ensure compliance with cybersecurity laws before executing the script.
