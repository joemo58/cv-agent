from pydantic import BaseModel
from typing import Literal


class JDRequirement(BaseModel):
    id: str
    requirement: str
    category: Literal["technical", "domain", "delivery", "soft_skill", "seniority", "logistics", "other"]
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
