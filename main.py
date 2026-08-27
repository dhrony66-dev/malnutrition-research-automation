import subprocess
import sys
from pathlib import Path


# ==========================================
# PROJECT DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

SRC_DIR = BASE_DIR / "src"


# ==========================================
# ANALYSIS STEPS
# ==========================================

scripts = [
    "01_import.py",
    "02_validation.py",
    "03_cleaning.py",
    "04_missing.py",
    "05_descriptive.py",
    "06_visualization.py",
    "07_correlation.py",
    "08_vif.py",
    "09_regression.py",
    "10_diagnostics.py",
    "11_tables.py"
]


# ==========================================
# START
# ==========================================

print("\n======================================")
print("     RESEARCH AUTOMATION SYSTEM")
print("======================================")

print("\nAnalysis pipeline started...\n")


# ==========================================
# RUN EACH SCRIPT
# ==========================================

for i, script in enumerate(scripts, start=1):

    script_path = SRC_DIR / script

    print("\n--------------------------------------")
    print(f"STEP {i}: {script}")
    print("--------------------------------------")

    if not script_path.exists():

        print(
            f"ERROR: File not found: {script_path}"
        )

        sys.exit(1)

    result = subprocess.run(
        [
            sys.executable,
            str(script_path)
        ]
    )

    if result.returncode != 0:

        print(
            f"\nERROR: {script} failed."
        )

        print(
            "Pipeline stopped."
        )

        sys.exit(
            result.returncode
        )

    print(
        f"\n{script} completed successfully."
    )


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("   RESEARCH AUTOMATION COMPLETED")
print("======================================")

print("\nAll analysis steps completed successfully.")

print("\nResults are available in:")

print(
    BASE_DIR / "results"
)

print("\n======================================")