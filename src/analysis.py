from collections import defaultdict

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

def compare_periods(current_tx, previous_tx):
    def summarize(transactions):
        totals = defaultdict(float)
        for t in transactions:
            # STRICT: expenses only
            if t["amount"] >= 0:
                continue
            if t["category"].lower() == "income":
                continue

            totals[t["category"]] += abs(t["amount"])
        return totals


    current = summarize(current_tx)
    previous = summarize(previous_tx)

    comparison = {}
    all_categories = set(current) | set(previous)

    for category in all_categories:
        curr_amt = current.get(category, 0)
        prev_amt = previous.get(category, 0)
        delta = curr_amt - prev_amt

        comparison[category] = {
            "current": curr_amt,
            "previous": prev_amt,
            "delta": delta,
        }

    return comparison
