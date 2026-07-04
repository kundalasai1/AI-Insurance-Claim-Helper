import json

def load_checklist():
    with open("data/insurance_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

def get_documents(claim_type):
    data = load_checklist()

    if claim_type in data:
        return data[claim_type]["documents"]

    return []