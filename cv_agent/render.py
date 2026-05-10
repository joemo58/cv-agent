from datetime import datetime, timezone


def build_run_metadata(
    base_cv_path: str,
    jd_path: str,
    model: str,
    max_pages: int,
    tone: str,
    target_role: str,
) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "base_cv_path": base_cv_path,
        "jd_path": jd_path,
        "model": model,
        "max_pages": max_pages,
        "tone": tone,
        "target_role": target_role,
    }
