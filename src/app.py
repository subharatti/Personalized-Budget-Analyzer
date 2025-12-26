from flask import Flask, render_template
from data_loader import load_transactions
from analysis import calculate_spending_summary
from charts import plot_spending_pie, plot_spending_bar

app = Flask(__name__)

@app.route("/")
def index():
    transactions = load_transactions()
    expenses, income_total = calculate_spending_summary(transactions)

    plot_spending_pie(expenses)
    plot_spending_bar(expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        income_total=income_total
    )

if __name__ == "__main__":
    app.run(debug=True)
