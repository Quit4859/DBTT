# DBTT — Digital Brain That Thinks

DBTT is a modular **Cognitive Operating System** (“Brain OS”).

- **Thought Graph** is the single system state.
- Specialized **Brain modules** read/write structured Thoughts.
- The **LLM** is only a language-generation component (swappable backend).

## Getting started

### Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Run API

```bash
uvicorn dbtt.api.server:app --reload
```

### Call

```bash
curl -X POST http://127.0.0.1:8000/v1/think \
  -H 'content-type: application/json' \
  -d '{"text":"Hello DBTT"}'
```

## Roadmap
See `docs/` for architecture notes.

