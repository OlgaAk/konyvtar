import json
import os

DATA_FILE = "./data.json"

def load_from_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_to_file(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)