from flask import Flask, render_template
from datetime import datetime, timedelta

from data_loader import load_transactions
from analysis import calculate_spending_summary, compare_periods, detect_lifestyle_inflation
from charts import plot_spending_pie, plot_spending_bar

from hf_assistant import ask_finance_question
from flask import jsonify, request

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
    inflation = detect_lifestyle_inflation(comparison)

    plot_spending_pie(expenses)
    plot_spending_bar(expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        income_total=income_total,
        comparison=comparison,
        inflation=inflation
    )

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question."}), 400

    transactions = load_transactions()
    expenses, _ = calculate_spending_summary(transactions)

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
    inflation = detect_lifestyle_inflation(comparison)

    q = question.lower()

    if "lifestyle inflation" in q:
        if inflation["flag"]:
            return jsonify({
                "answer": (
                    "Yes, your spending pattern shows signs of lifestyle inflation. "
                    f"Spending increased across {inflation['count']} categories, "
                    "suggesting a upward shift rather than a one-time expense."
                )
            })
        else:
            return jsonify({
                "answer": (
                    "No clear lifestyle inflation was detected. "
                    "Recent increases appear limited to one or two categories rather than a broad trend."
                )
            })


    if "concern" in q or "worried" in q or "problem" in q:
        if inflation["flag"]:
            return jsonify({
                "answer": (
                    "It may be worth paying attention. Your discretionary spending has increased across "
                    "multiple categories, which could affect savings if the trend continues."
                )
            })
        else:
            return jsonify({
                "answer": (
                    "There is no immediate cause for concern. "
                    "Your spending changes do not appear widespread or sustained."
                )
            })

    if "least" in q or "smallest" in q:
        category = min(expenses, key=expenses.get)
        return jsonify({
            "answer": f"You spend the least on {category}."
        })

    if "most" in q or "largest" in q:
        category = max(expenses, key=expenses.get)
        return jsonify({
            "answer": f"You spend the most on {category}."
        })

    if "bigger part" in q or "percentage" in q or "percent" in q:
        food = expenses.get("Food And Drink", 0)
        total = sum(expenses.values())

        if total == 0:
            return jsonify({"answer": "There is not enough data to determine this."})

        share = (food / total) * 100

        return jsonify({
            "answer": f"Food spending currently makes up about {share:.1f}% of your total spending. To determine whether it is becoming a bigger part of your budget, we would need data from previous periods."
        })

    if "not change" in q or "unchanged" in q:
        unchanged = []

        for cat, data in comparison.items():
            delta = data.delta if hasattr(data, "delta") else data.get("delta", 0)
            if delta == 0:
                unchanged.append(cat)

        if not unchanged:
            return jsonify({
                "answer": "Most categories experienced some change during this period."
            })

        return jsonify({
            "answer": "The following categories remained relatively stable: " + ", ".join(unchanged) + "."
        })

    if any(word in q for word in ["why", "increase", "decrease", "trend", "change"]):
        answer = ask_finance_question(
            question=question,
            spending_summary=format_dict(expenses),
            spending_changes=format_dict(comparison),
            inflation=inflation
        )

    else:
        answer = "That question is better answered with direct calculations."


    return jsonify({"answer": answer})


def format_dict(d):
    if not d:
        return "No data available."

    lines = []

    for key, value in d.items():

        if hasattr(value, "current") and hasattr(value, "previous") and hasattr(value, "delta"):
            curr = float(value.current)
            prev = float(value.previous)
            delta = float(value.delta)

            if delta > 0:
                direction = "increased"
            elif delta < 0:
                direction = "decreased"
            else:
                direction = "did not change"

            lines.append(
                f"{key}: {direction} from ${prev:.2f} to ${curr:.2f} (change of ${abs(delta):.2f})"
            )

        elif isinstance(value, (int, float)):
            lines.append(f"{key}: ${value:.2f}")

        else:
            lines.append(f"{key}: {value}")

    return "\n".join(lines)

def format_changes(comparison):
    if not comparison:
        return "No notable changes."

    lines = []

    for category, data in comparison.items():

        if isinstance(data, dict):
            delta = data.get("delta", 0)

        elif hasattr(data, "delta"):
            delta = data.delta

        else:
            continue

        if delta != 0:
            direction = "increased" if delta > 0 else "decreased"
            lines.append(f"{category} {direction} compared to last period.")

    if not lines:
        return "No significant category changes."

    return " ".join(lines)


if __name__ == "__main__":
    app.run(debug=True)
