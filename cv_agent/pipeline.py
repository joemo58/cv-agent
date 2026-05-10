def run_tailoring_pipeline(base_cv: str, jd: str) -> dict:
    jd_analysis = analyse_jd(jd)
    evidence_map = map_evidence(base_cv, jd_analysis)
    tailoring_plan = create_tailoring_plan(base_cv, jd_analysis, evidence_map)
    tailored_cv = rewrite_cv(base_cv, jd, evidence_map, tailoring_plan)
    change_report = validate_tailored_cv(base_cv, tailored_cv, evidence_map)
    recruiter_message = write_recruiter_message(jd, tailored_cv)

    return {
        "jd_analysis": jd_analysis,
        "evidence_map": evidence_map,
        "tailoring_plan": tailoring_plan,
        "tailored_cv": tailored_cv,
        "change_report": change_report,
        "recruiter_message": recruiter_message,
    }