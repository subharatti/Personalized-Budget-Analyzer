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

def compare_periods(current_tx, previous_tx, min_change=50):
    from collections import defaultdict

    def summarize(transactions):
        totals = defaultdict(float)
        for t in transactions:
            if t["amount"] < 0: 
                totals[t["category"]] += abs(t["amount"])
        return totals

    current = summarize(current_tx)
    previous = summarize(previous_tx)

    comparison = {}

    for category in current:
        curr_amt = current.get(category, 0)
        prev_amt = previous.get(category, 0)
        delta = curr_amt - prev_amt

        if curr_amt == 0:
            continue
        if abs(delta) < min_change:
            continue

        comparison[category] = {
            "current": curr_amt,
            "previous": prev_amt,
            "delta": delta,
        }

    return comparison

def detect_lifestyle_inflation(comparison):
    discretionary = {
        "Food And Drink",
        "Shopping",
        "Entertainment",
        "Personal Care",
        "Travel",
        "Transportation"
    }

    increased = []
    total_increase = 0.0

    for category, data in comparison.items():
        delta = data.delta if hasattr(data, "delta") else data.get("delta", 0)

        if category in discretionary and delta > 0:
            increased.append((category, float(delta)))
            total_increase += float(delta)

    increased.sort(key=lambda x: x[1], reverse=True)

    flagged = (len(increased) >= 1 and total_increase >= 1)

    return {
        "flag": flagged,
        "count": len(increased),
        "total_increase": round(total_increase, 2),
        "top_drivers": increased[:3], 
    }

def detect_spending_anomalies(comparison, threshold=1.8):
    anomalies = []

    for category, data in comparison.items():
        current = data.current if hasattr(data, "current") else data.get("current", 0)
        previous = data.previous if hasattr(data, "previous") else data.get("previous", 0)

        if previous == 0 and current > 0:
            anomalies.append({
                "category": category,
                "reason": "appeared for the first time",
                "severity": "medium"
            })

        elif previous > 0 and current / previous >= threshold:
            anomalies.append({
                "category": category,
                "reason": "spiked significantly",
                "severity": "high"
            })

    return anomalies
