# CS238: Intro to Generative AI

Walla Walla University, instructor Chiké Abuah (chike.abuah@wallawalla.edu).

This course grew out of CS450 Modern Software Engineering, which folded in generative AI content one quarter at a time until GenAI was the course. CS238 is the result: a 10-week quarter that teaches generative AI as its own subject, hands-on, using locally-run open models via [Ollama](https://ollama.com).

The companion reading is the instructor's own textbook, *Illustrating Generative AI*, whose chapter structure the course follows closely.

This directory is the public course repository: everything students use. Answer keys, quizzes, and the instructor's archive live in the instructor's private directory alongside it, and never in this one.

## Structure

- Labs live in their own repository, [cs238-labs](https://github.com/abuach/cs238-labs), released one week at a time during the quarter
- `resources/` — standing course resources not tied to a specific week (Ollama server etiquette, setup notes)
- `util/` — shared `ollama_client.py` helper imported across labs

## Week-by-week map

| Week | Topic | IGAI chapter |
|---|---|---|
| 1 | Introduction to Generative AI | Introduction |
| 2 | Prompting | Prompting |
| 3 | Tokens | Tokens |
| 4 | Semantics (meaning as distance) | Semantics |
| 5 | Responsible AI | Responsible |
| 6 | Augmentation (RAG) | Augmentation |
| 7 | Agentic (tool calling & multi-agent) | Agentic |
| 8 | Multimodal | Multimodal |
| 9 | Efficiency | Efficiency |
| 10 | Thinking (reasoning models) | Thinking |


## Setup

This repository uses [uv](https://docs.astral.sh/uv/) and a local [Ollama](https://ollama.com) install.

```bash
uv sync
ollama serve
```

Labs default to `http://localhost:11434`. If the course instead points at a shared class server, only the `host` argument in `util/ollama_client.py` needs to change; everything else in the labs stays the same. See `resources/ollama-server-guidelines.md` for etiquette on a shared server.
