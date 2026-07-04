import json

FILE = "data.json"


def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {"sessions": []}


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)