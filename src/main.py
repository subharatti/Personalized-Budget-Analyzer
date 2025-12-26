from config import DATA_FILE
from data_loader import load_transactions
from analysis import summarize_by_category
from reports import print_summary

def main():
    transactions = load_transactions(DATA_FILE)
    summary = summarize_by_category(transactions)
    print_summary(summary)

if __name__ == "__main__":
    main()
