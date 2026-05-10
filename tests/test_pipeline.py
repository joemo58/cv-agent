from unittest.mock import patch
from cv_agent.pipeline import run_tailoring_pipeline

BASE_CV = "x" * 300
JD = "x" * 300


def _make_responses():
    return [f"stage_{i}_output" for i in range(1, 7)]


@patch("cv_agent.pipeline.call_llm")
def test_pipeline_returns_all_sections(mock_llm):
    mock_llm.side_effect = _make_responses()
    result = run_tailoring_pipeline(BASE_CV, JD)
    assert result.jd_analysis_markdown == "stage_1_output"
    assert result.evidence_map_markdown == "stage_2_output"
    assert result.tailoring_plan_markdown == "stage_3_output"
    assert result.tailored_cv_markdown == "stage_4_output"
    assert result.validation_report_markdown == "stage_5_output"
    assert result.recruiter_message_markdown == "stage_6_output"


@patch("cv_agent.pipeline.call_llm")
def test_pipeline_calls_llm_six_times(mock_llm):
    mock_llm.side_effect = _make_responses()
    run_tailoring_pipeline(BASE_CV, JD)
    assert mock_llm.call_count == 6


@patch("cv_agent.pipeline.call_llm")
def test_evidence_map_runs_before_cv_rewrite(mock_llm):
    # Evidence map is call #2; its output must appear in the CV rewrite prompt (call #4)
    mock_llm.side_effect = _make_responses()
    run_tailoring_pipeline(BASE_CV, JD)
    cv_rewrite_prompt = mock_llm.call_args_list[3].args[0]
    assert "stage_2_output" in cv_rewrite_prompt


@patch("cv_agent.pipeline.call_llm")
def test_validation_runs_after_cv_rewrite(mock_llm):
    # CV rewrite is call #4; its output must appear in the validation prompt (call #5)
    mock_llm.side_effect = _make_responses()
    run_tailoring_pipeline(BASE_CV, JD)
    validation_prompt = mock_llm.call_args_list[4].args[0]
    assert "stage_4_output" in validation_prompt
