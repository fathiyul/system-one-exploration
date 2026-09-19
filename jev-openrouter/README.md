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
