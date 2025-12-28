from transformers import pipeline

qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    max_length=180,
    temperature=0.3,
    repetition_penalty=1.2,
)

def ask_finance_question(question, spending_summary, spending_changes, inflation):
    inflation_status = (
        "Lifestyle inflation has been detected."
        if inflation["flag"]
        else "No clear lifestyle inflation was detected."
    )

    inflation_details = ""

    if inflation["flag"]:
        drivers = ", ".join(cat for cat, _ in inflation["top_drivers"])
        inflation_details = (
            f"Discretionary spending increased across multiple categories. "
            f"Main drivers: {drivers}. "
            f"Total discretionary increase: ${inflation['total_increase']}."
        )

    prompt = f"""
You are a personal finance assistant.

Answer the user's question using the information below.

IMPORTANT RULES:
- Do NOT list raw category totals
- Explain causes, not tables
- If lifestyle inflation is detected, explain it clearly
- If not detected, say so

SPENDING SUMMARY (high level):
{spending_summary}

RECENT SPENDING CHANGES:
{spending_changes}

LIFESTYLE INFLATION STATUS:
{inflation_status}
{inflation_details}

USER QUESTION:
{question}

Respond in 2-4 sentences of plain English.
"""
    output = qa_pipeline(prompt, do_sample=False)[0]["generated_text"]
    return output.strip()

