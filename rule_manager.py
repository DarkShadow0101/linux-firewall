import json

def load_rules(filepath="config/rules.json"):
    with open(filepath, "r") as file:
        return json.load(file)
