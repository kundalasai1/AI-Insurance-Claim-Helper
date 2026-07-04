import json

def load_checklist():

    with open("data/insurance_data.json", "r") as file:
        return json.load(file)