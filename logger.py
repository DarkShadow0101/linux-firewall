from datetime import datetime

def log_event(message):
    with open("logs/firewall.log", "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")
