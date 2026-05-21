import subprocess


PIPELINE_STEPS = [
    ("Build dataset", "scripts.build_dataset"),
    ("Create annotated windows", "scripts.create_annotated_windows"),
    ("Generate prompts", "scripts.generate_prompts"),
    ("Run mock LLM", "src.llm.runner"),
    ("Evaluate results", "scripts.evaluate_results"),
]


def run_script(module_name: str, label: str) -> None:
    print(f"\nRunning: {label}")

    result = subprocess.run(
        ["python3", "-m", module_name],
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(f"{module_name} failed.")

    print(f"Completed: {label}")


def main() -> None:
    print("\n=== Sensor2LLM Experiment Pipeline ===")

    for label, module_name in PIPELINE_STEPS:
        run_script(module_name, label)

    print("\nAll experiments completed successfully.")


if __name__ == "__main__":
    main()