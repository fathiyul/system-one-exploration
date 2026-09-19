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

## Read the story

Worth reading: [*I Built Non-Autoregressive Decision Models with RL a Year Ago. Then a Frontier Lab Called It a "Breakthrough"*](https://laya.convaiinnovations.com/) — the Laya vs TypeSafe Jev comparison behind this repo. It shows benchmarks on the public datasets where Jev exists, and how Laya stacks up (7.8x faster, 3x better calibrated, 45/51 languages usable, Apache 2.0, and zero emoji regression).
