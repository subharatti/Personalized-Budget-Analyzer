# 📊 Personalized Budget Analyzer

A full-stack personal finance dashboard that analyzes spending data, detects trends and anomalies, and lets users ask questions about their finances using an AI assistant.

**Live Demo:**  
[https://huggingface.co/spaces/subharatti/personalized-budget-analyzer](https://huggingface.co/spaces/subharatti/personalized-budget-analyzer)


## Overview

Is it difficult to understand your finances through long statements packed-full with information? Do you ever have questions about your finances but never know where to direct them to?

The Personalized Budget Analyzer helps users understand where their money is going, why spending changes over time, and whether their habits suggest lifestyle inflation or unusual activity.
It combines transaction analysis, statistical trend detection, data visualization, and AI-driven explanations, with a lightweight mobile companion built using **React Native**.


## Features

- **Transaction intake & categorization**
  - Designed around the **Plaid API** for real bank transaction data
  - Uses official Plaid category metadata
  - Groups spending into clear, human-readable categories

- **Spending summary & breakdown**
  - Splits expenses by category
  - Separates income from spending
  - Presents totals in a clean table

- **Visual analytics**
  - Automatically generates a spending distribution pie chart
  - Category-level bar chart for side-by-side comparison
  - Charts are rendered using **Matplotlib**

- **Time-based spending comparison**
  - Compares the most recent 30-day period against the previous 30 days
  - Identifies increases, decreases, and stable spending categories

- **Lifestyle inflation detection**
  - Detects increases in spending
  - Helps distinguish habits from one-time expenses
  - Supports questions like “Should I be concerned about this trend?”

- **AI-powered financial Q&A**
  - Ask questions such as:
    - “Why did my spending increase this month?”
    - “Which category did I spend the least in?”
    - “Did anything stay the same?”
    - “Is this lifestyle inflation?”
  - Created using Hugging Face LLM
  - Combines rule-based logic with generative explanations
  - Produces concise, plain-English answers instead of raw data

- **Polished UI**
  - Clean and understandable theme that does not make the data seem "scary"
  - Loading indicators, animations, and disabled features

- **Mini mobile companion**
  - Lightweight mobile version built with **React Native**
  - Displays spending summaries and AI Q&A
  - Shares the same backend API design as the web app

## Technologies Used

**Backend**
- Python
- Flask
- Gunicorn
- Hugging Face LLM
- Plaid API
- Matplotlib, NumPy

**Frontend**
- HTML
- CSS
- JavaScript

**Mobile**
- React Native
- TypeScript
