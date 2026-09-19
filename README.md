# Jevploration

Playground for trying out Jev-like models (System 1: fast, intuitive, answers typed questions) from various repos and APIs.

Each subfolder is its own Python project (managed with uv):

| Folder | What it tries |
| --- | --- |
| `jev-openrouter` | Jev model via OpenRouter's decisions API |
| `try-laya` | Scaffold with the [Laya](https://github.com/LayaAI) dependency |

To run a project:

```sh
cd <folder>
uv run main.py
```

### Extraction examples (`jev-openrouter`)

Python ports of the TS examples from [OpenRouter's Jev extract lab](https://openrouter.ai/labs/jev/extract). Each one posts a document to the Jev model and extracts structured fields:

```sh
uv run agreement.py    # master services agreement
uv run invoice.py      # invoice
uv run lease.py        # commercial lease
uv run offer-letter.py # offer letter
```
