from pydantic import BaseModel
from typing import Literal

class JDRequirement(BaseModel):
    requirement: str
    category: Literal["technical", "domain", "soft_skill", "seniority", "logistics"]
    importance: Literal["high", "medium", "low"]
    evidence_needed: str


class EvidenceMatch(BaseModel):
    requirement: str
    matched_experience: str
    source_section: str
    strength: Literal["strong", "medium", "weak", "none"]
    notes: str


class TailoringPlan(BaseModel):
    summary: str
    must_emphasise: list[str]
    de_emphasise: list[str]
    risks: list[str]
    recommended_order: list[str]


class ChangeReport(BaseModel):
    changed_sections: list[str]
    removed_or_compressed: list[str]
    claims_to_verify: list[str]
    possible_overreach: list[str]