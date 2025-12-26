def print_summary(summary):
    print("\n   Spending Summary\n")
    for category, total in summary.items():
        print(f"{category:<15}: ${total:.2f}")
