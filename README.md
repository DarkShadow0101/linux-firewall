# Linux Firewall – Python-Based Personal Firewall (Web GUI + CLI)

This project is a **custom personal firewall** built using Python and Linux `iptables`, with a clean web-based interface for rule management. It provides both **command-line** and **web GUI (Flask + HTML)** controls to filter incoming/outgoing network traffic.

---

## Features

- **Traffic Filtering:** Supports blocking/allowing traffic by IP address, port, protocol, and direction.
- **Rule Config File:** Uses `rules.json` for persistent firewall rules.
- **Web Interface:** Built with Flask + HTML for managing firewall rules.
- **Reset Button:** Allows resetting the firewall to a clean state.
- **Rate Limiting:** Prevents abuse by limiting the number of rule changes per IP per minute.
- **Logging:** Actions are logged via `logger.py` and stored in `logs/`.
- **Rule Validation:** Only well-formed rules (valid IPs, ports, protocols) are accepted.
- **Authentication (Basic):** Protects web access with simple credentials (extendable).

---

## Folder Structure

```
linux-firewall/
├── app.py               # Flask app for web interface
├── firewall.py          # CLI-based rule engine using iptables
├── rule_manager.py      # Handles rule operations (add/edit/delete/load)
├── logger.py            # Logs rule applications
├── config/
│   └── rules.json       # Firewall rule definitions
├── logs/
│   └── firewall.log     # Log of rule applications
├── templates/
│   └── index.html       # Web GUI template
```

---

## Getting Started

### Prerequisites

- Linux OS
- Python 3.x
- `iptables` installed
- Flask: `pip install flask`

---

### Run via Terminal (CLI)

```bash
cd linux-firewall
sudo python3 firewall.py
```

You’ll be prompted whether to reset existing rules or not. Then, rules from `config/rules.json` are applied.

---

### Run Web Interface (GUI)

```bash
cd linux-firewall
sudo python3 app.py
```

Then open your browser:

```
http://127.0.0.1:5000/
```

> Log in with username and password defined in `app.py`

---

## Firewall Rule Format (`config/rules.json`)

```json
[
  { "action": "allow", "port": 22, "protocol": "tcp", "direction": "input" },
  { "action": "block", "ip": "192.168.1.100", "direction": "input" }
]
```

- `action`: "allow" or "block"
- `port`: Optional (1-65535)
- `ip`: Optional (IPv4)
- `protocol`: Optional ("tcp", "udp", "icmp")
- `direction`: "input" or "output"

---

## Security Notes

- You can enhance authentication using Flask-Login or OAuth for multi-user login.
- Consider restricting access to localhost only or adding HTTPS using a reverse proxy like Nginx
