import pandas as pd
import yaml
from pathlib import Path
from statsmodels.stats.outliers_influence import variance_inflation_factor


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
# OUTPUT DIRECTORY
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


vif_threshold = config[
    "analysis"
]["vif_threshold"]


# ==========================================
# SELECT PREDICTORS
# ==========================================

X = df[
    numeric_variables
].copy()


# ==========================================
# CALCULATE VIF
# ==========================================

vif_results = []


for i, variable in enumerate(
    X.columns
):

    vif_value = variance_inflation_factor(
        X.values,
        i
    )

    if vif_value < vif_threshold:

        interpretation = "Acceptable"

    else:

        interpretation = (
            "High multicollinearity"
        )


    vif_results.append(
        {
            "Variable": variable,
            "VIF": round(
                vif_value,
                3
            ),
            "Interpretation":
                interpretation
        }
    )


vif_df = pd.DataFrame(
    vif_results
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n======================================")
print("          VIF ANALYSIS")
print("======================================")


print("\nPredictor variables:")

for variable in numeric_variables:

    print(
        f" - {variable}"
    )


print("\n--------------------------------------")
print("VIF RESULTS")
print("--------------------------------------")


print(
    vif_df.to_string(
        index=False
    )
)


# ==========================================
# MULTICOLLINEARITY CHECK
# ==========================================

print("\n--------------------------------------")
print("MULTICOLLINEARITY CHECK")
print("--------------------------------------")


high_vif = vif_df[
    vif_df["VIF"] >= vif_threshold
]


if high_vif.empty:

    print(
        "No potential multicollinearity "
        "detected."
    )

else:

    print(
        "Potential multicollinearity detected:"
    )

    for _, row in high_vif.iterrows():

        print(
            f" - {row['Variable']}: "
            f"VIF = {row['VIF']}"
        )


# ==========================================
# SAVE RESULTS
# ==========================================

OUTPUT_FILE = (
    TABLES_DIR
    / "vif_results.csv"
)


vif_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nVIF results saved to:")

print(
    OUTPUT_FILE
)


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("         VIF ANALYSIS COMPLETED")
print("======================================")