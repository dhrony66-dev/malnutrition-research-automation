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
    config["data"]["input_file"]
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

id_variables = config["variables"]["id"]

numeric_variables = config["variables"]["numeric"]

categorical_variables = config["variables"]["categorical"]

outcome_variables = config["variables"]["outcomes"]


# ==========================================
# VALIDATION START
# ==========================================

print("\n======================================")
print("       VARIABLE-LEVEL VALIDATION")
print("======================================")


# ==========================================
# CHECK REQUIRED VARIABLES
# ==========================================

required_variables = (
    id_variables
    + numeric_variables
    + categorical_variables
    + outcome_variables
)


missing_variables = [
    variable
    for variable in required_variables
    if variable not in df.columns
]


if missing_variables:

    print("\nERROR: Required variables missing:")

    for variable in missing_variables:

        print(
            f" - {variable}"
        )

    raise ValueError(
        "Required variables are missing from dataset."
    )


# ==========================================
# VALIDATE VARIABLES
# ==========================================

validation_results = []


for variable in required_variables:

    series = df[variable]

    validation_results.append(
        {
            "Variable": variable,
            "Data_Type": str(
                series.dtype
            ),
            "Unique_Values": series.nunique(),
            "Missing_N": series.isna().sum(),
            "Missing_Percent":
                round(
                    series.isna().mean() * 100,
                    2
                )
        }
    )


validation_df = pd.DataFrame(
    validation_results
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print(
    validation_df.to_string(
        index=False
    )
)


# ==========================================
# SAVE VALIDATION RESULTS
# ==========================================

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "tables"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_FILE = (
    OUTPUT_DIR
    / "variable_validation.csv"
)


validation_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# COMPLETION
# ==========================================

print("\nValidation results saved to:")

print(
    OUTPUT_FILE
)


print("\n======================================")
print("       VALIDATION COMPLETED")
print("======================================")