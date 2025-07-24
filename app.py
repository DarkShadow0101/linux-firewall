from flask import Flask, render_template, request, redirect, url_for
import json
import subprocess
import ipaddress
import os

app = Flask(__name__)
RULES_FILE = "config/rules.json"

# Validate each rule
def validate_rule(rule):
    try:
        if rule.get("action") not in ["block", "allow"]:
            return False
        if rule.get("direction") not in ["input", "output"]:
            return False
        if "protocol" in rule and rule["protocol"] not in ["tcp", "udp", "icmp"]:
            return False
        if "port" in rule:
            port = int(rule["port"])
            if not (1 <= port <= 65535):
                return False
        if "ip" in rule:
            ipaddress.ip_address(rule["ip"])
        if "limit" in rule:
            parts = rule["limit"].split("/")
            int(parts[0])  # e.g. 5/minute → checks "5"
        return True
    except:
        return False

# Load firewall rules from file
def load_rules():
    if not os.path.exists(RULES_FILE):
        return []
    with open(RULES_FILE, "r") as f:
        return json.load(f)

# Save firewall rules to file
def save_rules(rules):
    with open(RULES_FILE, "w") as f:
        json.dump(rules, f, indent=2)

# Apply rules to iptables
def apply_rules(rules):
    subprocess.run(["iptables", "-F"])
    for rule in rules:
        if not validate_rule(rule):
            continue
        direction = rule["direction"]
        chain = "INPUT" if direction == "input" else "OUTPUT"
        jump = "DROP" if rule["action"] == "block" else "ACCEPT"
        cmd = ["iptables", "-A", chain]

        if "protocol" in rule:
            cmd += ["-p", rule["protocol"]]
        if "ip" in rule:
            cmd += ["-s" if direction == "input" else "-d", rule["ip"]]
        if "port" in rule:
            cmd += ["--dport", str(rule["port"])]
        if "limit" in rule:
            cmd += ["-m", "limit", "--limit", rule["limit"]]  # e.g., 5/minute

        cmd += ["-j", jump]
        subprocess.run(cmd)

# Show firewall GUI
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        rule = {
            "action": request.form["action"],
            "direction": request.form["direction"],
            "protocol": request.form.get("protocol") or None,
            "port": int(request.form["port"]) if request.form.get("port") else None,
            "ip": request.form.get("ip") or None,
            "limit": request.form.get("limit") or None
        }

        rules = load_rules()
        rules.append(rule)
        save_rules(rules)
        apply_rules(rules)
        return redirect(url_for("index"))

    rules = load_rules()
    return render_template("index.html", rules=rules)

# Delete a rule by index
@app.route("/delete/<int:rule_index>")
def delete_rule(rule_index):
    rules = load_rules()
    if 0 <= rule_index < len(rules):
        del rules[rule_index]
        save_rules(rules)
        apply_rules(rules)
    return redirect(url_for("index"))

# Reset all iptables rules
@app.route("/reset", methods=["POST"])
def reset_firewall():
    subprocess.run(["iptables", "-F"])
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
