def validate_inputs(
    base_cv: str,
    jd: str,
    max_pages: int,
    tone: str,
    target_role: str,
) -> None:
    if not base_cv:
        raise ValueError("Base CV must not be empty.")
    if not jd:
        raise ValueError("Job description must not be empty.")
    if len(base_cv) < 300:
        raise ValueError("Base CV must be at least 300 characters.")
    if len(jd) < 300:
        raise ValueError("Job description must be at least 300 characters.")
    if not (1 <= max_pages <= 4):
        raise ValueError("max_pages must be between 1 and 4.")
    if len(tone) > 200:
        raise ValueError("tone must not exceed 200 characters.")
    if len(target_role) > 200:
        raise ValueError("target_role must not exceed 200 characters.")
