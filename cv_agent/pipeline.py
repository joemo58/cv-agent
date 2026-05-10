from cv_agent.llm import call_llm
from cv_agent.models import PipelineResult
from cv_agent.validators import validate_inputs
from cv_agent.prompts import (
    build_jd_analysis_prompt,
    build_evidence_mapping_prompt,
    build_tailoring_plan_prompt,
    build_cv_rewrite_prompt,
    build_validation_prompt,
    build_recruiter_message_prompt,
)


def analyse_jd(jd: str, model: str) -> str:
    return call_llm(build_jd_analysis_prompt(jd), model=model)


def map_evidence(base_cv: str, jd_analysis: str, model: str) -> str:
    return call_llm(build_evidence_mapping_prompt(base_cv, jd_analysis), model=model)


def create_tailoring_plan(
    base_cv: str,
    jd_analysis: str,
    evidence_map: str,
    max_pages: int,
    tone: str,
    target_role: str,
    model: str,
) -> str:
    return call_llm(
        build_tailoring_plan_prompt(base_cv, jd_analysis, evidence_map, max_pages, tone, target_role),
        model=model,
    )


def rewrite_cv(
    base_cv: str,
    jd: str,
    jd_analysis: str,
    evidence_map: str,
    tailoring_plan: str,
    max_pages: int,
    tone: str,
    target_role: str,
    model: str,
) -> str:
    return call_llm(
        build_cv_rewrite_prompt(base_cv, jd, jd_analysis, evidence_map, tailoring_plan, max_pages, tone, target_role),
        model=model,
    )


def validate_tailored_cv(
    base_cv: str,
    tailored_cv: str,
    evidence_map: str,
    jd_analysis: str,
    model: str,
) -> str:
    return call_llm(
        build_validation_prompt(base_cv, tailored_cv, evidence_map, jd_analysis),
        model=model,
    )


def write_recruiter_message(jd: str, tailored_cv: str, tone: str, model: str) -> str:
    return call_llm(build_recruiter_message_prompt(jd, tailored_cv, tone), model=model)


def run_tailoring_pipeline(
    base_cv: str,
    jd: str,
    model: str = "gpt-4.1-mini",
    max_pages: int = 2,
    tone: str = "direct, senior, concise",
    target_role: str = "",
) -> PipelineResult:
    validate_inputs(base_cv, jd, max_pages, tone, target_role)

    jd_analysis = analyse_jd(jd, model)
    evidence_map = map_evidence(base_cv, jd_analysis, model)
    tailoring_plan = create_tailoring_plan(base_cv, jd_analysis, evidence_map, max_pages, tone, target_role, model)
    tailored_cv = rewrite_cv(base_cv, jd, jd_analysis, evidence_map, tailoring_plan, max_pages, tone, target_role, model)
    validation_report = validate_tailored_cv(base_cv, tailored_cv, evidence_map, jd_analysis, model)
    recruiter_message = write_recruiter_message(jd, tailored_cv, tone, model)

    return PipelineResult(
        jd_analysis_markdown=jd_analysis,
        evidence_map_markdown=evidence_map,
        tailoring_plan_markdown=tailoring_plan,
        tailored_cv_markdown=tailored_cv,
        validation_report_markdown=validation_report,
        recruiter_message_markdown=recruiter_message,
    )
