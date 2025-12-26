from plaid_client import fetch_transactions
from datetime import datetime

def load_transactions(_=None):
    raw_transactions = fetch_transactions()
    transactions = []

    for t in raw_transactions:
        data = t.to_dict()
        name = data["name"].lower()
        amount = float(data["amount"])

        pfc = data.get("personal_finance_category")

        if pfc and pfc.get("primary") and pfc["primary"] != "OTHER":
            category = pfc["primary"].title().replace("_", " ")

        else:
            if any(x in name for x in ["rent", "lease", "utility", "hydro"]):
                category = "Housing"
            elif any(x in name for x in ["payment", "credit", "loan"]):
                category = "Bills"
            elif any(x in name for x in ["uber", "lyft", "taxi", "bus"]):
                category = "Transportation"
            elif any(x in name for x in ["shop", "store", "market"]):
                category = "Shopping"
            elif any(x in name for x in ["food", "restaurant", "kfc", "mcdonald"]):
                category = "Food And Drink"
            else:
                category = "Other"

        transactions.append({
            "name": data["name"],
            "amount": amount,
            "date": data["date"],
            "category": category
        })

    return transactions

