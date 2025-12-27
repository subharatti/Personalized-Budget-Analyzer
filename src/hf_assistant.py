from transformers import pipeline

qa_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    max_length=180,
    temperature=0.3,
    repetition_penalty=1.2,
)

def ask_finance_question(question, spending_summary, spending_changes):
    prompt = f"""
You are a personal finance assistant.

The user is asking WHY their spending changed.

IMPORTANT RULES:
- Do NOT list category amounts
- Do NOT repeat numbers verbatim
- Explain causes, not data
- Mention ONLY categories that increased or appeared this period
- Give a short explanation (2-4 sentences)

SPENDING SUMMARY (for context only):
{spending_summary}

ACTUAL CHANGES (this is what matters):
{spending_changes}

Question:
{question}

Write a natural explanation in plain English.
"""

    output = qa_pipeline(prompt, do_sample=False)[0]["generated_text"]
    return output.strip()

