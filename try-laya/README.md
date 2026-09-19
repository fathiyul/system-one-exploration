# Try-Laya

Trying out [Laya](https://github.com/LayaAI/laya) — a System 1 model loaded from the Hugging Face Hub that answers typed questions (choice, score, noul) in one forward pass.

## Requirements

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/)

## Run

```sh
uv run main.py
```

## What it does

Loads the fine-tuned `convaiinnovations/laya` model, feeds it a support email as state, and asks four typed questions (department, urgency, churn risk, phishing) in a single forward pass, then prints the answers with their confidence.
