import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

PIPELINE_STEPS = [
    ("Build dataset", "build_dataset.py"),
    ("Create annotated windows", "create_annotated_windows.py"),
    ("Generate prompts", "generate_prompts.py"),
    ("Run mock LLM", "run_llm.py"),
    ("Evaluate results", "evaluate_results.py"),
]


def run_script(script_name: str) -> None:
    script_path = PROJECT_ROOT / "scripts" / script_name

    result = subprocess.run(
        ["python3", str(script_path)],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        raise RuntimeError(f"{script_name} failed.")


def main() -> None:
    print("\n=== Sensor2LLM Experiment Pipeline ===\n")

    for description, script_name in PIPELINE_STEPS:
        print(f"Running: {description}")
        run_script(script_name)
        print(f"Completed: {description}\n")

    print("All experiments completed successfully.")


if __name__ == "__main__":
    main()