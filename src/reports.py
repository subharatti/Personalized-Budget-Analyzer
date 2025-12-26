def print_summary(expenses, income_total):
    print("\nSpending Summary\n")

    for category, total in expenses.items():
        print(f"{category:<18}: ${total:.2f}")

    if income_total > 0:
        print("\nIncome\n")
        print(f"{'Total Income':<18}: ${income_total:.2f}")
