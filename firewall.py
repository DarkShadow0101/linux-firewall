import json
import subprocess
import ipaddress

# ✅ Reset firewall
def reset_firewall():
    print("[*] Flushing existing iptables rules...")
    subprocess.run(["iptables", "-F"])

# ✅ Validate each rule before applying
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
            ipaddress.ip_address(rule["ip"])  # Throws ValueError if invalid
        return True
    except:
        return False

# ✅ Apply valid rules
def apply_rules(file_path):
    with open(file_path, 'r') as file:
        rules = json.load(file)

    for rule in rules:
        if not validate_rule(rule):
            print("[!] Skipping invalid rule:", rule)
            continue

        direction = rule.get("direction")
        chain = "INPUT" if direction == "input" else "OUTPUT"
        action = rule.get("action")
        jump = "DROP" if action == "block" else "ACCEPT"

        cmd = ["iptables", "-A", chain]

        if "protocol" in rule:
            cmd += ["-p", rule["protocol"]]
        if "ip" in rule:
            cmd += ["-s" if direction == "input" else "-d", rule["ip"]]
        if "port" in rule:
            cmd += ["--dport", str(rule["port"])]

        cmd += ["-j", jump]

        print("[+] Applying rule:", " ".join(cmd))
        subprocess.run(cmd)

# ✅ View applied rules
def show_rules():
    print("\n[*] Current iptables rules:")
    subprocess.run(["iptables", "-L", "-n", "-v"])

# ✅ Main
if __name__ == "__main__":
    choice = input("Reset firewall before applying new rules? (y/n): ").lower()
    if choice == 'y':
        reset_firewall()

    apply_rules("rules.json")
    show_rules()
