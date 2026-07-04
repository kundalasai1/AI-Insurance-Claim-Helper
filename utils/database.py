import json

def get_claim_status(claim_id):

    with open("data/claim_status.json", "r") as file:
        data = json.load(file)

    return data.get(claim_id.upper())