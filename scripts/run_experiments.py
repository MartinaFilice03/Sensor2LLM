import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_script(script_name: str) -> None:
    script_path = PROJECT_ROOT / "scripts" / script_name

    print(f"\nRunning {script_name}...\n")

    result = subprocess.run(
        ["python3", str(script_path)],
        cwd=PROJECT_ROOT,
    )

    if result.returncode != 0:
        raise RuntimeError(f"{script_name} failed.")


def main() -> None:
    run_script("generate_prompts.py")
    run_script("evaluate_results.py")

    print("\nExperiment pipeline completed successfully.")


if __name__ == "__main__":
    main()