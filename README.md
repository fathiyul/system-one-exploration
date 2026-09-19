# System One Exploration

Playground for trying out System 1–style models (fast, intuitive, answer typed questions) from various repos and APIs.

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
