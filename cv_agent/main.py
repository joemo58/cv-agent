import typer
from pathlib import Path
from rich.console import Console

from cv_agent.io import read_text_file, write_text_file, write_json_file, ensure_output_dir
from cv_agent.render import build_run_metadata
from cv_agent.pipeline import run_tailoring_pipeline

app = typer.Typer()
console = Console()


@app.command()
def tailor(
    base_cv: Path = typer.Option(..., help="Path to base CV in Markdown"),
    jd: Path = typer.Option(..., help="Path to job description in Markdown"),
    out: Path = typer.Option(..., help="Output directory"),
    model: str = typer.Option("gpt-4.1-mini", help="OpenAI model to use"),
    max_pages: int = typer.Option(2, help="Maximum CV pages (1–4)"),
    tone: str = typer.Option("direct, senior, concise", help="Writing tone"),
    target_role: str = typer.Option("", help="Target role description"),
):
    console.print("Reading inputs...")
    base_cv_text = read_text_file(base_cv)
    jd_text = read_text_file(jd)

    console.print("Running pipeline...")
    result = run_tailoring_pipeline(base_cv_text, jd_text, model, max_pages, tone, target_role)

    ensure_output_dir(out)
    write_text_file(out / "01_jd_analysis.md", result.jd_analysis_markdown)
    write_text_file(out / "02_evidence_map.md", result.evidence_map_markdown)
    write_text_file(out / "03_tailoring_plan.md", result.tailoring_plan_markdown)
    write_text_file(out / "04_tailored_cv.md", result.tailored_cv_markdown)
    write_text_file(out / "05_validation_report.md", result.validation_report_markdown)
    write_text_file(out / "06_recruiter_message.md", result.recruiter_message_markdown)

    metadata = build_run_metadata(str(base_cv), str(jd), model, max_pages, tone, target_role)
    write_json_file(out / "run_metadata.json", metadata)

    console.print(f"Done. Outputs written to {out}")


if __name__ == "__main__":
    app()
