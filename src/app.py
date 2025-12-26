from flask import Flask, render_template
from datetime import datetime, timedelta

from data_loader import load_transactions
from analysis import calculate_spending_summary, compare_periods
from charts import plot_spending_pie, plot_spending_bar

app = Flask(__name__)


def normalize_date(d):
    if isinstance(d, datetime):
        return d
    return datetime.combine(d, datetime.min.time())


@app.route("/")
def index():
    transactions = load_transactions()

    expenses, income_total = calculate_spending_summary(transactions)

    today = datetime.now()
    start_current = today - timedelta(days=30)
    start_previous = today - timedelta(days=60)

    current_period = [
        t for t in transactions
        if start_current <= normalize_date(t["date"]) <= today
    ]

    previous_period = [
        t for t in transactions
        if start_previous <= normalize_date(t["date"]) < start_current
    ]

    comparison = compare_periods(current_period, previous_period)

    plot_spending_pie(expenses)
    plot_spending_bar(expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        income_total=income_total,
        comparison=comparison
    )


if __name__ == "__main__":
    app.run(debug=True)
