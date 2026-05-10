Below is a copy/paste-ready implementation spec.

````markdown
# CV Agent CLI MVP — Implementation Spec

## Goal

Build a Python CLI tool that tailors a base CV to a job description using an LLM-assisted, evidence-first pipeline.

The tool should:

1. Read a base CV from Markdown.
2. Read a job description from Markdown/text.
3. Analyse the JD.
4. Map JD requirements to evidence from the base CV.
5. Produce a tailoring plan.
6. Generate a tailored CV.
7. Validate the tailored CV for unsupported or exaggerated claims.
8. Generate a short recruiter message.
9. Write all outputs as Markdown files.

This is an MVP. Prioritise clean structure, debuggability, and truthful output over fancy agent behaviour.

---

## Tech stack

Use:

- Python 3.12+
- `uv`
- `typer` for CLI
- `rich` for console output
- `pydantic` for data models
- `openai` Python SDK
- `python-dotenv`
- `pytest`

Do not add a web UI.
Do not add MCP yet.
Do not add DOCX/PDF export yet.
Do not use a database.

---

## CLI interface

The command should be:

```bash
uv run python -m cv_agent.main tailor \
  --base-cv ./data/base_cv.md \
  --jd ./data/jobs/example_jd.md \
  --out ./out/example
````

Optional args:

```bash
--model gpt-4.1-mini
--max-pages 2
--tone "direct, senior, concise"
--target-role "backend/fullstack engineer"
```

Required args:

* `--base-cv`
* `--jd`
* `--out`

Expected output directory:

```text
out/example/
  01_jd_analysis.md
  02_evidence_map.md
  03_tailoring_plan.md
  04_tailored_cv.md
  05_validation_report.md
  06_recruiter_message.md
  run_metadata.json
```

---

## Project structure

Create:

```text
cv-agent/
  cv_agent/
    __init__.py
    main.py
    config.py
    io.py
    llm.py
    models.py
    pipeline.py
    prompts.py
    render.py
    validators.py
  data/
    base_cv.md
    jobs/
      example_jd.md
  out/
  tests/
    test_io.py
    test_pipeline.py
    test_validators.py
  .env.example
  pyproject.toml
  README.md
```

---

## Environment

`.env.example`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

The app should load `.env` automatically.

If `OPENAI_API_KEY` is missing, fail with a clear error.

---

## Data models

Implement in `models.py`.

Use Pydantic models.

```python
from pydantic import BaseModel, Field
from typing import Literal


class JDRequirement(BaseModel):
    id: str
    requirement: str
    category: Literal[
        "technical",
        "domain",
        "delivery",
        "soft_skill",
        "seniority",
        "logistics",
        "other",
    ]
    importance: Literal["high", "medium", "low"]
    evidence_needed: str


class JDAnalysis(BaseModel):
    role_title: str | None = None
    company: str | None = None
    role_summary: str
    top_requirements: list[JDRequirement]
    must_have_technologies: list[str]
    nice_to_have_technologies: list[str]
    seniority_signals: list[str]
    hidden_priorities: list[str]
    risks_or_unknowns: list[str]


class EvidenceMatch(BaseModel):
    requirement_id: str
    requirement: str
    matched_experience: list[str]
    source_sections: list[str]
    strength: Literal["strong", "medium", "weak", "none"]
    notes: str


class EvidenceMap(BaseModel):
    matches: list[EvidenceMatch]
    strongest_themes: list[str]
    weakest_gaps: list[str]
    suggested_keywords: list[str]


class TailoringPlan(BaseModel):
    positioning_summary: str
    must_emphasise: list[str]
    de_emphasise: list[str]
    recommended_section_order: list[str]
    bullet_rewrite_strategy: list[str]
    risks: list[str]


class ValidationFinding(BaseModel):
    claim: str
    status: Literal["supported", "inferred", "unsupported", "overstated"]
    reason: str
    suggested_fix: str | None = None


class ValidationReport(BaseModel):
    findings: list[ValidationFinding]
    unsupported_claims: list[str]
    overstatement_risks: list[str]
    missing_keywords: list[str]
    overall_assessment: str


class PipelineResult(BaseModel):
    jd_analysis_markdown: str
    evidence_map_markdown: str
    tailoring_plan_markdown: str
    tailored_cv_markdown: str
    validation_report_markdown: str
    recruiter_message_markdown: str
```

---

## Pipeline

Implement in `pipeline.py`.

The pipeline must be explicit and sequential.

```python
def run_tailoring_pipeline(
    base_cv: str,
    jd: str,
    model: str,
    max_pages: int,
    tone: str,
    target_role: str,
) -> PipelineResult:
    ...
```

Pipeline steps:

1. Validate inputs.
2. Analyse JD.
3. Map evidence from base CV to JD.
4. Create tailoring plan.
5. Rewrite CV.
6. Validate tailored CV.
7. Generate recruiter message.
8. Return markdown outputs.

Do not skip evidence mapping.

Do not rewrite the CV before the evidence map exists.

---

## LLM wrapper

Implement in `llm.py`.

Requirements:

* Centralise all OpenAI calls.
* Accept a prompt string.
* Accept a model string.
* Return text.
* Add basic retry handling.
* Raise clear exceptions.

Suggested interface:

```python
def call_llm(prompt: str, model: str) -> str:
    ...
```

Use the OpenAI Responses API.

Keep it simple.

---

## Prompt requirements

Implement prompts in `prompts.py`.

Use one function per prompt.

### 1. JD analysis prompt

Function:

```python
def build_jd_analysis_prompt(jd: str) -> str:
    ...
```

The prompt should instruct the model to produce Markdown with:

* Role summary
* Top requirements
* Must-have technologies
* Nice-to-have technologies
* Seniority signals
* Hidden priorities
* Risks or unknowns

The output should be concise but complete.

### 2. Evidence mapping prompt

Function:

```python
def build_evidence_mapping_prompt(base_cv: str, jd_analysis: str) -> str:
    ...
```

Rules:

* Do not invent evidence.
* Use only the base CV.
* Mark each requirement as `strong`, `medium`, `weak`, or `none`.
* Quote or paraphrase the relevant base CV evidence.
* Explicitly list gaps.

### 3. Tailoring plan prompt

Function:

```python
def build_tailoring_plan_prompt(
    base_cv: str,
    jd_analysis: str,
    evidence_map: str,
    max_pages: int,
    tone: str,
    target_role: str,
) -> str:
    ...
```

Output should include:

* Positioning summary
* What to emphasise
* What to compress or remove
* Recommended section order
* Bullet rewrite strategy
* Risks

### 4. CV rewrite prompt

Function:

```python
def build_cv_rewrite_prompt(
    base_cv: str,
    jd: str,
    jd_analysis: str,
    evidence_map: str,
    tailoring_plan: str,
    max_pages: int,
    tone: str,
    target_role: str,
) -> str:
    ...
```

Hard rules:

* Do not invent employers, dates, tools, metrics, titles, or responsibilities.
* Prefer reordering, compression, and reframing over invention.
* Keep claims interview-defensible.
* Keep the CV concise.
* Use Australian/British spelling.
* Optimise for the target role.
* Preserve strong evidence.
* Do not include commentary outside the CV.

### 5. Validation prompt

Function:

```python
def build_validation_prompt(
    base_cv: str,
    tailored_cv: str,
    evidence_map: str,
    jd_analysis: str,
) -> str:
    ...
```

Output should include:

* Supported claims
* Inferred claims
* Unsupported claims
* Overstated claims
* Missing important keywords
* Suggested fixes

### 6. Recruiter message prompt

Function:

```python
def build_recruiter_message_prompt(
    jd: str,
    tailored_cv: str,
    tone: str,
) -> str:
    ...
```

Output:

* Short message
* 3–6 sentences
* Direct, natural, not overly salesy
* No invented claims

---

## Input validation

Implement in `validators.py`.

Rules:

* Base CV must not be empty.
* JD must not be empty.
* Base CV should be at least 300 characters.
* JD should be at least 300 characters.
* `max_pages` must be between 1 and 4.
* `tone` must not exceed 200 characters.
* `target_role` must not exceed 200 characters.

Fail early with clear error messages.

---

## File IO

Implement in `io.py`.

Functions:

```python
def read_text_file(path: Path) -> str:
    ...

def write_text_file(path: Path, content: str) -> None:
    ...

def write_json_file(path: Path, data: dict) -> None:
    ...

def ensure_output_dir(path: Path) -> None:
    ...
```

Use UTF-8.

Create directories as needed.

---

## Rendering

Implement in `render.py`.

For now, the LLM outputs Markdown directly.

Add a small helper to create metadata:

```python
def build_run_metadata(
    base_cv_path: str,
    jd_path: str,
    model: str,
    max_pages: int,
    tone: str,
    target_role: str,
) -> dict:
    ...
```

Metadata should include:

* timestamp
* input paths
* model
* max_pages
* tone
* target_role

---

## CLI behaviour

In `main.py`:

* Use Typer.
* Show progress with Rich.
* Print each pipeline stage as it runs.
* Write all outputs.
* Print final output path.

Example console output:

```text
Reading inputs...
Analysing job description...
Mapping evidence...
Creating tailoring plan...
Rewriting CV...
Validating tailored CV...
Writing recruiter message...
Done. Outputs written to out/example
```

---

## Tests

Use pytest.

### `test_validators.py`

Test:

* empty base CV fails
* empty JD fails
* short base CV fails
* short JD fails
* invalid max pages fails
* overly long tone fails
* overly long target role fails

### `test_io.py`

Test:

* can read text file
* missing file raises useful error
* can write text file
* can create output directory
* can write JSON

### `test_pipeline.py`

Do not call real LLMs in tests.

Mock `call_llm`.

Test:

* pipeline calls stages in order
* pipeline returns all expected markdown sections
* validation runs after CV rewrite
* evidence map runs before CV rewrite

---

## README requirements

Create a README with:

* What the tool does
* Setup instructions
* `.env` setup
* Example command
* Output explanation
* Known limitations
* Future roadmap

Future roadmap:

```text
- DOCX export
- PDF export
- Structured JSON outputs
- Experience bank / RAG
- MCP server wrapper
- AWS Bedrock support
- Web UI
- Application tracking database
```

---

## Acceptance criteria

The MVP is complete when:

1. I can run the CLI against a base CV and JD.
2. It creates all expected output files.
3. The tailored CV is generated only after JD analysis, evidence mapping, and tailoring plan.
4. The validation report identifies unsupported or risky claims.
5. The recruiter message is generated.
6. Tests pass.
7. README explains how to run the project.
8. The code is clean enough to extend with MCP later.

---

## Important design constraints

* Keep the pipeline simple and explicit.
* Do not build autonomous multi-agent behaviour yet.
* Do not let the LLM invent facts.
* Prefer deterministic orchestration over vague agent loops.
* Keep each prompt isolated and testable.
* Make every intermediate output visible to the user.
* Optimise for learning tools and agents later, not for perfect CV output now.

```
```
