CATEGORY_REMAP = {
    "Transfer Out": "Transfers",
    "Loan Payments": "Bills",
    "Rent And Utilities": "Housing",
    "General Merchandise": "Shopping",
}

def calculate_spending_summary(transactions):
    expenses = {}
    income_total = 0.0

    for t in transactions:
        amount = t["amount"]
        category = t["category"]

        category = CATEGORY_REMAP.get(category, category)

        if amount < 0:
            income_total += abs(amount)
            continue

        expenses[category] = expenses.get(category, 0) + amount

    expenses = {
        cat: total
        for cat, total in expenses.items()
        if total > 0
    }

    return expenses, income_total
