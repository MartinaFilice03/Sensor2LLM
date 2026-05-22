import sys
import subprocess


PIPELINE_STEPS = [
    ("Build dataset", "scripts.build_dataset"),
    ("Create annotated windows", "scripts.create_annotated_windows"),
    ("Generate prompts", "scripts.generate_prompts"),
    ("Run mock LLM", "scripts.run_llm"),  # fix naming consistency
    ("Evaluate results", "scripts.evaluate_results"),
]


def run_script(module_name: str, label: str) -> None:
    print(f"\n=== Running: {label} ===")

    result = subprocess.run(
        [sys.executable, "-m", module_name],
        text=True,
        capture_output=True,
    )

    print(result.stdout)

    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"{module_name} failed with return code {result.returncode}")

    print(f"=== Completed: {label} ===")


def main() -> None:
    print("\n=== Sensor2LLM Experiment Pipeline ===")

    for label, module_name in PIPELINE_STEPS:
        run_script(module_name, label)

    print("\nAll experiments completed successfully.")


if __name__ == "__main__":
    main()