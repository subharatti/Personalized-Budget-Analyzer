import matplotlib.pyplot as plt
import numpy as np


def plot_spending_pie(expenses):
    if not expenses:
        return

    labels = list(expenses.keys())
    values = list(expenses.values())

    if not labels:
        return

    labels, values = zip(*sorted(
        zip(labels, values),
        key=lambda x: x[1],
        reverse=True
    ))

    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(values)))

    def autopct_if_large(pct):
        return f"{pct:.1f}%" if pct >= 4 else ""

    plt.figure(figsize=(9, 9))
    wedges, _, _ = plt.pie(
        values,
        autopct=autopct_if_large,
        startangle=140,
        colors=colors,
        wedgeprops={"edgecolor": "white"},
    )

    plt.legend(
        wedges,
        labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
    )

    plt.title("Spending by Category", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("src/static/spending_pie.png", bbox_inches="tight")
    plt.close()


def plot_spending_bar(expenses):
    if not expenses:
        return

    labels = list(expenses.keys())
    values = list(expenses.values())

    if not labels:
        return

    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(values)))

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color=colors)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Amount ($)")
    plt.title("Spending by Category", fontsize=14, fontweight="bold")

    plt.tight_layout()
    plt.savefig("src/static/spending_bar.png")
    plt.close()
