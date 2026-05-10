# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the CLI
uv run python -m cv_agent.main tailor \
  --base-cv data/base_cv.md \
  --jd data/jobs/example_job.md \
  --out out/example

# Optional flags
  --model gpt-4.1-mini
  --max-pages 2
  --tone "direct, senior, concise"
  --target-role "backend/fullstack engineer"

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_pipeline.py

# Run a single test
uv run pytest tests/test_pipeline.py::test_name
```

## Environment

Copy `.env` and set `OPENAI_API_KEY`. The app loads `.env` automatically via `python-dotenv`. It fails fast if the key is missing.

## Architecture

The tool tailors a base CV to a job description using a sequential, evidence-first pipeline. Each stage feeds the next; no stage is skipped.

**Pipeline** (`pipeline.py`): Orchestrates six stages in order:
1. `analyse_jd` — extracts requirements, technologies, seniority signals from the JD
2. `map_evidence` — maps each JD requirement to evidence found in the base CV (no invention)
3. `create_tailoring_plan` — decides what to emphasise, compress, or reorder
4. `rewrite_cv` — rewrites only after evidence map and plan exist
5. `validate_tailored_cv` — checks tailored CV claims against the base CV evidence
6. `write_recruiter_message` — short outreach message from the tailored CV

Each stage calls `call_llm` from `llm.py` with a prompt built by a dedicated function in `prompts.py`.

**LLM wrapper** (`llm.py`): All OpenAI calls go through `call_llm(prompt, model)`. Uses the **Responses API** (`client.responses.create(model=..., input=...)`), not Chat Completions.

**Prompts** (`prompts.py`): One function per pipeline stage. Each prompt must be self-contained and testable in isolation. Hard rules encoded in the CV rewrite prompt: no invented employers, dates, tools, metrics, or titles.

**Models** (`models.py`): Pydantic models for structured pipeline data — `JDRequirement`, `JDAnalysis`, `EvidenceMatch`, `EvidenceMap`, `TailoringPlan`, `ValidationReport`, `PipelineResult`.

**CLI** (`main.py`): Typer entry point. Reads inputs, calls the pipeline, writes six numbered Markdown files to the output directory, plus `run_metadata.json`.

**Output files**:
```
out/<name>/
  01_jd_analysis.md
  02_evidence_map.md
  03_tailoring_plan.md
  04_tailored_cv.md
  05_validation_report.md
  06_recruiter_message.md
  run_metadata.json
```

**Supporting modules** (to be implemented):
- `validators.py` — input validation (empty/short CV or JD, max_pages 1–4, tone/target_role ≤200 chars)
- `io.py` — `read_text_file`, `write_text_file`, `write_json_file`, `ensure_output_dir` (UTF-8)
- `render.py` — `build_run_metadata` helper (timestamp + run params)

## Testing

Do not call real LLMs in tests. Mock `call_llm` in `test_pipeline.py`. Tests live in `tests/` and cover validators, file I/O, and pipeline stage ordering.

## Design constraints

- Evidence-first: the CV rewrite must never run before the evidence map is complete.
- No fact invention: prompts must instruct the LLM not to invent employers, dates, tools, metrics, or titles.
- Deterministic orchestration: no autonomous agent loops — each step is explicit and sequential.
- All intermediate outputs are written to disk so the user can inspect each stage.
- The full implementation spec is in `cv_agent/spec.md`.
