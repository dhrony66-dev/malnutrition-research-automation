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
# DATA PATHS FROM CONFIG
# ==========================================

INPUT_PATH = Path(
    config["data"]["input_file"]
)

CLEANED_PATH = Path(
    config["data"]["cleaned_file"]
)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    INPUT_PATH
)


# ==========================================
# CLEANING START
# ==========================================

print("\n======================================")
print("        DATA CLEANING STARTED")
print("======================================")


print(
    f"\nRows before cleaning: {len(df)}"
)


# ==========================================
# REMOVE DUPLICATES
# ==========================================

duplicates = df.duplicated().sum()

df = df.drop_duplicates()


print(
    f"Rows after cleaning: {len(df)}"
)

print(
    f"Duplicates removed: {duplicates}"
)


# ==========================================
# MISSING VALUE CHECK
# ==========================================

missing_total = df.isna().sum().sum()


print(
    f"Total missing values: {missing_total}"
)


# ==========================================
# VARIABLE GROUPS FROM CONFIG
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
# DISPLAY NUMERIC VARIABLES
# ==========================================

print("\nNumeric variables:")

print(
    numeric_variables
)


# ==========================================
# MISSING VALUE SUMMARY
# ==========================================

print("\n--------------------------------------")
print("MISSING VALUE SUMMARY")
print("--------------------------------------")


missing_summary = df.isna().sum()


print(
    missing_summary
)


# ==========================================
# CREATE OUTPUT DIRECTORY
# ==========================================

CLEANED_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# SAVE CLEANED DATA
# ==========================================

df.to_csv(
    CLEANED_PATH,
    index=False
)


print("\nCleaned dataset saved to:")

print(
    CLEANED_PATH
)


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("        DATA CLEANING COMPLETED")
print("======================================")