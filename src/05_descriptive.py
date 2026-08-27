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
# DATA PATH
# ==========================================

DATA_PATH = Path(
    config["data"]["final_file"]
)


# ==========================================
# OUTPUT PATH
# ==========================================

TABLES_DIR = BASE_DIR / "results" / "tables"

TABLES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    DATA_PATH
)


# ==========================================
# VARIABLES FROM CONFIG
# ==========================================

numeric_variables = config[
    "variables"
]["numeric"]

categorical_variables = config[
    "variables"
]["categorical"]

outcome_variables = config[
    "variables"
]["outcomes"]


# ==========================================
# START
# ==========================================

print("\n======================================")
print("       DESCRIPTIVE ANALYSIS")
print("======================================")


print(
    f"\nDataset shape: {df.shape}"
)


# ==========================================
# NUMERIC DESCRIPTIVE STATISTICS
# ==========================================

print("\n--------------------------------------")
print("NUMERIC DESCRIPTIVE STATISTICS")
print("--------------------------------------")


numeric_results = []


for variable in numeric_variables:

    if variable not in df.columns:
        continue

    series = df[variable]

    numeric_results.append(
        {
            "Variable": variable,
            "N": series.count(),
            "Mean": round(series.mean(), 3),
            "SD": round(series.std(), 3),
            "Min": round(series.min(), 3),
            "Median": round(series.median(), 3),
            "Max": round(series.max(), 3)
        }
    )


numeric_df = pd.DataFrame(
    numeric_results
)


print(
    numeric_df.to_string(
        index=False
    )
)


# ==========================================
# SAVE NUMERIC RESULTS
# ==========================================

numeric_output = (
    TABLES_DIR
    / "numeric_descriptive_statistics.csv"
)


numeric_df.to_csv(
    numeric_output,
    index=False
)


print("\nNumeric summary saved to:")

print(
    numeric_output
)


# ==========================================
# CATEGORICAL DESCRIPTIVE STATISTICS
# ==========================================

print("\n--------------------------------------")
print("CATEGORICAL DESCRIPTIVE STATISTICS")
print("--------------------------------------")


categorical_results = []


all_categorical = (
    categorical_variables
    + outcome_variables
)


for variable in all_categorical:

    if variable not in df.columns:
        continue

    counts = (
        df[variable]
        .value_counts(
            dropna=False
        )
    )

    percentages = (
        df[variable]
        .value_counts(
            normalize=True,
            dropna=False
        )
        * 100
    )


    for category in counts.index:

        categorical_results.append(
            {
                "Variable": variable,
                "Category": category,
                "N": counts[category],
                "Percent": round(
                    percentages[category],
                    2
                )
            }
        )


categorical_df = pd.DataFrame(
    categorical_results
)


print(
    categorical_df.to_string(
        index=False
    )
)


# ==========================================
# SAVE CATEGORICAL RESULTS
# ==========================================

categorical_output = (
    TABLES_DIR
    / "categorical_descriptive_statistics.csv"
)


categorical_df.to_csv(
    categorical_output,
    index=False
)


print("\nCategorical summary saved to:")

print(
    categorical_output
)


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("    DESCRIPTIVE ANALYSIS COMPLETED")
print("======================================")