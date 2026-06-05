"""
run_all.py -- Reproducibility entry point
==========================================
Executes project.ipynb end-to-end using nbconvert and saves the executed
notebook to project_executed.ipynb.

Usage
-----
    python run_all.py            # full run  (FAST_MODE=False)
    python run_all.py --fast     # fast check (FAST_MODE=True, single seed)

Requirements
------------
    pip install jupyter nbconvert
    Dataset must be present at:
        data/hotel_bookings_course_release_v1.csv
    SHA-256: 7c2ae42a7353905ea136e5c2287f17c92c5435826598bfbb8491c6f0c7b1fc06

Output
------
    project_executed.ipynb   -- notebook with all outputs regenerated
    experiments.csv          -- updated experiment log
"""

import subprocess
import sys
import argparse
import time
import os
import importlib.util

if importlib.util.find_spec("nbconvert") is None:
    print("nbconvert not found — installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "nbconvert"])
else:
    print("nbconvert already installed — skipping.")


def check_dataset():
    path = os.path.join("data", "hotel_bookings_course_release_v1.csv")
    if not os.path.exists(path):
        print(f"ERROR: Dataset not found at '{path}'.")
        print("       Place the course release CSV in the data/ folder before running.")
        sys.exit(1)
    print(f"Dataset found: {path}")


def set_fast_mode(fast: bool):
    """Patch FAST_MODE value in project.ipynb before execution."""
    import json
    nb_path = "project.ipynb"
    with open(nb_path, encoding="utf-8") as f:
        nb = json.load(f)

    patched = 0
    for cell in nb["cells"]:
        src = "".join(cell["source"])
        if "FAST_MODE" in src and cell["cell_type"] == "code":
            new_src = []
            for line in cell["source"]:
                if line.strip().startswith("FAST_MODE"):
                    new_line = f'FAST_MODE = {fast}\n'
                    if line != new_line:
                        new_src.append(new_line)
                        patched += 1
                    else:
                        new_src.append(line)
                else:
                    new_src.append(line)
            cell["source"] = new_src

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"FAST_MODE set to {fast} in {patched} cell(s).")


def run_notebook():
    cmd = [
        sys.executable, "-m", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=3600",
        "--ExecutePreprocessor.kernel_name=UnsupervisedLearning",
        "project.ipynb",
    ]
    print("\nExecuting notebook...")
    print("  Command:", " ".join(cmd))
    print("  This may take several minutes for a full run.\n")

    t0 = time.time()
    result = subprocess.run(cmd)
    elapsed = time.time() - t0

    if result.returncode == 0:
        print(f"\nNotebook executed successfully in {elapsed:.1f}s.")
        print("Output saved to: project.ipynb")
        print("Experiment log:  experiments.csv")
    else:
        print(f"\nERROR: Notebook execution failed (return code {result.returncode}).")
        print("Check project_executed.ipynb or the console output above for details.")
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Run the Hotel Booking Clustering pipeline end-to-end.")
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Fast check mode: single seed, n_init=1, 1 subsample. Use for pipeline integrity checks."
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Hotel Booking Demand Clustering — run_all.py")
    print("=" * 60)
    print(f"Mode: {'FAST (single seed)' if args.fast else 'FULL (report run)'}")
    print()

    check_dataset()
    set_fast_mode(args.fast)
    run_notebook()


if __name__ == "__main__":
    main()
