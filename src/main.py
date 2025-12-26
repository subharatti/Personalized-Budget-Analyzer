from config import DATA_FILE
from data_loader import load_transactions
from analysis import calculate_spending_summary
from reports import print_summary
from charts import plot_spending_pie, plot_spending_bar

def main():
    transactions = load_transactions(DATA_FILE)
    expenses, income_total = calculate_spending_summary(transactions)
    print_summary(expenses, income_total)

    plot_spending_pie(expenses)
    plot_spending_bar(expenses)


if __name__ == "__main__":
    main()
