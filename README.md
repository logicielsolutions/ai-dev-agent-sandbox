# ai-dev-agent-sandbox

A small practice project for testing AI coding agents (the always-on agent trial, AIT-1073).
Nothing here ships anywhere.

`trialkit` is a toy version of the AI Team Board's helpers: board tickets, IST time zone
handling and reminders.

## Running the tests

You need Python 3.11 or newer (`requires-python = ">=3.11"` in `pyproject.toml`).
Install pytest, then run the tests from the repo root:

```sh
python -m pip install pytest
python -m pytest
```

Rules for agents: work on a branch, open a draft PR, never push to `main` (it is protected).
