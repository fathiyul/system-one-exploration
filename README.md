# System One Exploration

Playground for trying out System 1–style models (fast, intuitive, answer typed questions) from various repos and APIs.

## What "System 1" means

The name comes from Daniel Kahneman's *Thinking, Fast and Slow*: the human mind runs two modes of thinking. System 1 is fast, automatic, and intuitive — it makes quick judgments. System 2 is slow, deliberate, and analytical — it reasons step by step. This repo explores models that are more like the System 1 side: instead of generating responses, they take a piece of state and answer narrow, typed questions (booleans, choices, scores) in a single pass, with calibrated probabilities and confidence.

Each subfolder is its own Python project (managed with uv):

| Folder | What it tries | Local / API |
| --- | --- | --- |
| `jev-openrouter` | Jev model via OpenRouter's decisions API | API |
| `try-laya` | [Laya](https://github.com/LayaAI/laya), a local model from the Hugging Face Hub | Local |

To run a project:

```sh
cd <folder>
uv run main.py
```
