# wf_core.py
from wf_dataprocessing import run_dataprocessing
from wf_visualization import run_visualization


def main() -> None:
    print("=== SER541 MS3 Workflow: Data Processing → Visualization ===")

    processed_path = run_dataprocessing()
    print(f"✅ Data processing complete: {processed_path}")

    artifacts = run_visualization()
    print("✅ Visualization complete:")
    for k, v in artifacts.items():
        print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()