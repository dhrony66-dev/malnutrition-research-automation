import pandas as pd
import yaml
from pathlib import Path


# ==========================================
# PROJECT DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# LOAD CONFIGURATION
# ==========================================

CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

with open(
    CONFIG_PATH,
    "r",
    encoding="utf-8"
) as file:

    config = yaml.safe_load(file)


# ==========================================
# DATA PATHS
# ==========================================

INPUT_PATH = Path(
    config["data"]["cleaned_file"]
)

FINAL_PATH = Path(
    config["data"]["final_file"]
)


# ==========================================
# LOAD CLEANED DATA
# ==========================================

df = pd.read_csv(
    INPUT_PATH
)


# ==========================================
# START
# ==========================================

print("\n======================================")
print("       MISSING VALUE HANDLING")
print("======================================")


print(
    f"\nDataset shape: {df.shape}"
)


# ==========================================
# MISSING VALUE SUMMARY
# ==========================================

missing_summary = pd.DataFrame({
    "Variable": df.columns,
    "Missing_N": df.isna().sum().values,
    "Missing_Percent": (
        df.isna().mean().values * 100
    )
})


missing_summary["Missing_Percent"] = (
    missing_summary["Missing_Percent"]
    .round(2)
)


print("\n--------------------------------------")
print("MISSING VALUE SUMMARY")
print("--------------------------------------")

print(
    missing_summary.to_string(
        index=False
    )
)


# ==========================================
# TOTAL MISSING VALUES
# ==========================================

total_missing = df.isna().sum().sum()


print(
    f"\nTotal missing values: {total_missing}"
)


# ==========================================
# HANDLE MISSING VALUES
# ==========================================

if total_missing == 0:

    print(
        "\nNo missing values detected."
    )

    print(
        "No imputation was required."
    )

else:

    print(
        "\nMissing values detected."
    )

    print(
        "For this dataset, missing values "
        "will be handled using median imputation "
        "for numeric variables."
    )

    numeric_variables = config[
        "variables"
    ]["numeric"]

    for variable in numeric_variables:

        if variable in df.columns:

            median_value = df[
                variable
            ].median()

            df[variable] = df[
                variable
            ].fillna(
                median_value
            )


# ==========================================
# VERIFY AFTER HANDLING
# ==========================================

remaining_missing = (
    df.isna().sum().sum()
)


print(
    f"\nRemaining missing values: "
    f"{remaining_missing}"
)


# ==========================================
# SAVE FINAL DATASET
# ==========================================

FINAL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


df.to_csv(
    FINAL_PATH,
    index=False
)


print("\nFinal dataset saved to:")

print(
    FINAL_PATH
)


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("       MISSING VALUE HANDLING")
print("             COMPLETED")
print("======================================")