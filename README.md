# CS238: Intro to Generative AI

Walla Walla University, instructor Chiké Abuah (chike.abuah@wallawalla.edu).

This course grew out of CS450 Modern Software Engineering, which folded in generative AI content one quarter at a time until GenAI was the course. CS238 is the result: a 10-week quarter that teaches generative AI as its own subject, hands-on, using locally-run open models via [Ollama](https://ollama.com).

The companion reading is the instructor's own textbook, *Illustrating Generative AI*, whose chapter structure the course follows closely.

This directory is the public course repository: everything students use. Answer keys, quizzes, and the instructor's archive live in the instructor's private directory alongside it, and never in this one.

## Structure

- Slides and labs are released week by week during the quarter.
- `project/` — the quarter-long project: overview, ten weekly milestones, guides, rubric, idea bank, and the two starter tools (a Writer and a Reviewer) students copy and customize (`project/README.md`)
- `resources/` — standing course resources not tied to a specific week (Ollama server etiquette, setup notes)
- `util/` — shared `ollama_client.py` helper imported across labs

## Week-by-week map

| Week | Topic | IGAI chapter | Project milestone |
|---|---|---|---|
| 1 | Introduction to Generative AI | Introduction | Pick Your Path |
| 2 | Prompting | Prompting | Teach It Your Job |
| 3 | Tokens & Attention | Tokens | Gather Your Sources |
| 4 | Metacoding (GenAI for code) | Metacoding | Promises and Specialty Models |
| 5 | Augmentation (semantics & RAG) | Semantics, Augmentation | Ground It in Your Sources |
| 6 | Agentic (tool calling & multi-agent) | Agentic | Give It Hands |
| 7 | Thinking (reasoning models) | Thinking | The Audit |
| 8 | Multimodal | Multimodal | Make It Usable, and Let It See |
| 9 | Efficiency | Efficiency | Ship It |
| 10 | Responsible AI | Responsible | Break It, Fix It, Show It |

## Project

Alongside the labs, each team of one to three builds one generative-AI tool for a field of their choosing, one milestone a week, without writing code. Teams pick a path, a Writer (turns something into a piece of writing) or a Reviewer (gives feedback on writing), start from a working demo, and make it their own by editing instructions, examples, sources, settings, and tests. Milestones apply that week's technique to the team's own problem and material; weeks 3, 7, 8, and 10 add what the lectures don't cover (gathering sources, building a test set, watching a real user, red-teaming). The tool runs on local models through Ollama. See [`project/README.md`](project/README.md) for the arc, the grading, and the starter tools.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) and a local [Ollama](https://ollama.com) install.

```bash
uv sync
ollama serve
```

Labs default to `http://localhost:11434`. If the course instead points at a shared class server, only the `host` argument in `util/ollama_client.py` needs to change; everything else in the labs stays the same. See `resources/ollama-server-guidelines.md` for etiquette on a shared server.
