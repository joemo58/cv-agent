import typer
from pathlib import Path
from cv_agent.pipeline import run_tailoring_pipeline

app = typer.Typer()


@app.command()
def tailor(
    base_cv: Path = typer.Option(...),
    jd: Path = typer.Option(...),
    out: Path = typer.Option(...),
):
    out.mkdir(parents=True, exist_ok=True)

    result = run_tailoring_pipeline(
        base_cv=base_cv.read_text(),
        jd=jd.read_text(),
    )

    (out / "01_jd_analysis.md").write_text(result["jd_analysis"])
    (out / "02_evidence_map.md").write_text(result["evidence_map"])
    (out / "03_tailoring_plan.md").write_text(result["tailoring_plan"])
    (out / "04_tailored_cv.md").write_text(result["tailored_cv"])
    (out / "05_change_report.md").write_text(result["change_report"])
    (out / "06_recruiter_message.md").write_text(result["recruiter_message"])


if __name__ == "__main__":
    app()