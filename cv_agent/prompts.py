def build_jd_analysis_prompt(jd: str) -> str:
    return f"""Analyse the following job description and produce a structured Markdown report.

Include these sections:
- **Role Summary**: 2-3 sentences describing the role.
- **Top Requirements**: Numbered list of the most important requirements, each with category (technical/domain/delivery/soft_skill/seniority/logistics/other), importance (high/medium/low), and what evidence a candidate should provide.
- **Must-Have Technologies**: Bullet list.
- **Nice-to-Have Technologies**: Bullet list.
- **Seniority Signals**: What signals indicate the expected experience level.
- **Hidden Priorities**: Unstated but likely important priorities inferred from the JD.
- **Risks or Unknowns**: Ambiguities or red flags in the JD.

Be concise but complete. Output only Markdown.

---
JOB DESCRIPTION:
{jd}
"""


def build_evidence_mapping_prompt(base_cv: str, jd_analysis: str) -> str:
    return f"""Map the evidence in the base CV to each requirement identified in the JD analysis.

Rules:
- Do not invent evidence. Use only what is in the base CV.
- For each requirement, quote or paraphrase the relevant CV evidence.
- Rate strength as: strong, medium, weak, or none.
- Explicitly list gaps where no evidence exists.

Produce a structured Markdown report with:
- **Evidence Map**: For each requirement: strength rating, matched CV evidence, source section.
- **Strongest Themes**: What the candidate demonstrably excels at.
- **Weakest Gaps**: Requirements with weak or no evidence.
- **Suggested Keywords**: Keywords from the JD that are missing from the CV.

Output only Markdown.

---
JD ANALYSIS:
{jd_analysis}

---
BASE CV:
{base_cv}
"""


def build_tailoring_plan_prompt(
    base_cv: str,
    jd_analysis: str,
    evidence_map: str,
    max_pages: int,
    tone: str,
    target_role: str,
) -> str:
    return f"""Create a tailoring plan for rewriting the CV to target this role.

Target role: {target_role}
Tone: {tone}
Maximum pages: {max_pages}

Produce a structured Markdown report with:
- **Positioning Summary**: How to position this candidate for the role (2-3 sentences).
- **Must Emphasise**: What to highlight prominently.
- **De-emphasise or Remove**: What to compress or cut to stay within page limit.
- **Recommended Section Order**: List sections in the recommended order.
- **Bullet Rewrite Strategy**: Guidance on rewriting bullets (action verbs, metrics, framing).
- **Risks**: What claims or gaps might raise questions at interview.

Output only Markdown.

---
JD ANALYSIS:
{jd_analysis}

---
EVIDENCE MAP:
{evidence_map}

---
BASE CV:
{base_cv}
"""


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
    return f"""Rewrite the CV below to target the job description, following the tailoring plan exactly.

Target role: {target_role}
Tone: {tone}
Maximum pages: {max_pages}

Hard rules:
- Do NOT invent employers, dates, tools, metrics, titles, or responsibilities.
- Prefer reordering, compression, and reframing over invention.
- Every claim must be defensible at interview.
- Use Australian/British spelling.
- Keep the CV within {max_pages} page(s).
- Output the CV only — no commentary, no preamble, no explanation.

---
TAILORING PLAN:
{tailoring_plan}

---
EVIDENCE MAP:
{evidence_map}

---
JD ANALYSIS:
{jd_analysis}

---
JOB DESCRIPTION:
{jd}

---
BASE CV:
{base_cv}
"""


def build_validation_prompt(
    base_cv: str,
    tailored_cv: str,
    evidence_map: str,
    jd_analysis: str,
) -> str:
    return f"""Validate the tailored CV against the base CV and evidence map.

For each significant claim in the tailored CV, classify it as:
- **supported**: directly evidenced in the base CV
- **inferred**: reasonable inference from base CV evidence
- **unsupported**: no basis in the base CV
- **overstated**: exaggerates what the base CV actually says

Produce a Markdown validation report with:
- **Findings**: Each significant claim with its classification and reason.
- **Unsupported Claims**: List of claims with no base CV evidence.
- **Overstatement Risks**: Claims that exaggerate or inflate.
- **Missing Keywords**: Important JD keywords absent from the tailored CV.
- **Overall Assessment**: 2-3 sentence summary of the tailored CV's integrity.

Output only Markdown.

---
JD ANALYSIS:
{jd_analysis}

---
EVIDENCE MAP:
{evidence_map}

---
BASE CV:
{base_cv}

---
TAILORED CV:
{tailored_cv}
"""


def build_recruiter_message_prompt(jd: str, tailored_cv: str, tone: str) -> str:
    return f"""Write a short outreach message from the candidate to the recruiter or hiring manager.

Tone: {tone}
Length: 3-6 sentences. Direct and natural. Not salesy or over-eager.
Rules:
- Base the message only on the tailored CV. Do not invent claims.
- Reference the specific role.
- Highlight 1-2 of the strongest relevant points.
- End with a clear, low-pressure call to action.

Output only the message — no subject line, no preamble.

---
JOB DESCRIPTION:
{jd}

---
TAILORED CV:
{tailored_cv}
"""
