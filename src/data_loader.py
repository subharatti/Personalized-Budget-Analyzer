import json
from categories import categorize

def load_transactions(filepath):
    with open(filepath, "r") as f:
        raw = json.load(f)

    transactions = []
    for t in raw:
        transactions.append({
            "name": t["name"],
            "amount": float(t["amount"]),
            "date": t["date"],
            "category": categorize(t["name"])
        })

    return transactions
