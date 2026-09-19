# Jev-OpenRouter

Trying out the [Jev model from OpenRouter](https://openrouter.ai/~typesafe/jev-latest) with a first request in `main.py`.

## Requirements

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/)

## Setup

```sh
cp .env.example .env
# edit .env and add your OpenRouter API key
```

## Run

```sh
uv run main.py
```

## What it does

Sends a sample support message to the Jev model and asks it typed questions (urgency, department, frustration score), then prints the answers and shows how to act on them (e.g. escalate when urgent and billing-related).

## Extraction examples

Python ports of the TS examples from [OpenRouter's Jev extract lab](https://openrouter.ai/labs/jev/extract). Each one posts a document to the Jev model and extracts structured fields:

```sh
uv run agreement.py    # master services agreement
uv run invoice.py      # invoice
uv run lease.py        # commercial lease
uv run offer-letter.py # offer letter
```
