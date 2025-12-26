def summarize_by_category(transactions):
    summary = {}

    for t in transactions:
        cat = t["category"]
        summary[cat] = summary.get(cat, 0) + t["amount"]

    return summary
