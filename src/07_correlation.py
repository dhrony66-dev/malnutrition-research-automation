import pandas as pd
import yaml
import matplotlib.pyplot as plt
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
# OUTPUT DIRECTORIES
# ==========================================

TABLES_DIR = BASE_DIR / "results" / "tables"

FIGURES_DIR = BASE_DIR / "results" / "figures"

TABLES_DIR.mkdir(
    parents=True,
    exist_ok=True
)

FIGURES_DIR.mkdir(
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


# ==========================================
# CORRELATION THRESHOLD
# ==========================================

correlation_threshold = config[
    "analysis"
]["correlation_threshold"]


# ==========================================
# SELECT NUMERIC VARIABLES
# ==========================================

numeric_df = df[
    numeric_variables
].copy()


# ==========================================
# START
# ==========================================

print("\n======================================")
print("       CORRELATION ANALYSIS")
print("======================================")


print("\nNumeric variables:")

for variable in numeric_variables:

    print(
        f" - {variable}"
    )


# ==========================================
# CORRELATION MATRIX
# ==========================================

correlation_matrix = (
    numeric_df.corr()
)


print("\n--------------------------------------")
print("CORRELATION MATRIX")
print("--------------------------------------")

print(
    correlation_matrix.round(3)
)


# ==========================================
# SAVE CORRELATION MATRIX
# ==========================================

correlation_output = (
    TABLES_DIR
    / "correlation_matrix.csv"
)


correlation_matrix.to_csv(
    correlation_output
)


print("\nCorrelation matrix saved to:")

print(
    correlation_output
)


# ==========================================
# IDENTIFY STRONG CORRELATIONS
# ==========================================

strong_correlations = []


for i in range(
    len(correlation_matrix.columns)
):

    for j in range(
        i + 1,
        len(correlation_matrix.columns)
    ):

        variable_1 = (
            correlation_matrix.columns[i]
        )

        variable_2 = (
            correlation_matrix.columns[j]
        )

        correlation = (
            correlation_matrix.iloc[i, j]
        )


        if abs(correlation) >= correlation_threshold:

            strong_correlations.append(
                {
                    "Variable_1": variable_1,
                    "Variable_2": variable_2,
                    "Correlation": round(
                        correlation,
                        3
                    )
                }
            )


# ==========================================
# DISPLAY STRONG CORRELATIONS
# ==========================================

print("\n--------------------------------------")
print("STRONG CORRELATIONS")
print("--------------------------------------")


if len(strong_correlations) == 0:

    print(
        "No pair of variables has "
        f"absolute correlation ≥ "
        f"{correlation_threshold:.2f}."
    )

else:

    strong_df = pd.DataFrame(
        strong_correlations
    )

    print(
        strong_df.to_string(
            index=False
        )
    )


# ==========================================
# SAVE STRONG CORRELATIONS
# ==========================================

strong_output = (
    TABLES_DIR
    / "strong_correlations.csv"
)


if len(strong_correlations) > 0:

    strong_df.to_csv(
        strong_output,
        index=False
    )

else:

    pd.DataFrame(
        columns=[
            "Variable_1",
            "Variable_2",
            "Correlation"
        ]
    ).to_csv(
        strong_output,
        index=False
    )


print("\nStrong correlation results saved to:")

print(
    strong_output
)


# ==========================================
# CORRELATION HEATMAP
# ==========================================

plt.figure(
    figsize=(8, 6)
)

plt.imshow(
    correlation_matrix,
    aspect="auto"
)

plt.colorbar(
    label="Correlation"
)


plt.xticks(
    range(
        len(correlation_matrix.columns)
    ),
    correlation_matrix.columns,
    rotation=45,
    ha="right"
)


plt.yticks(
    range(
        len(correlation_matrix.columns)
    ),
    correlation_matrix.columns
)


# ==========================================
# ADD CORRELATION VALUES
# ==========================================

for i in range(
    len(correlation_matrix.index)
):

    for j in range(
        len(correlation_matrix.columns)
    ):

        value = correlation_matrix.iloc[
            i,
            j
        ]

        plt.text(
            j,
            i,
            f"{value:.2f}",
            ha="center",
            va="center"
        )


plt.title(
    "Correlation Matrix"
)

plt.tight_layout()


heatmap_output = (
    FIGURES_DIR
    / "correlation_heatmap.png"
)


plt.savefig(
    heatmap_output,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\nCorrelation heatmap saved to:")

print(
    heatmap_output
)


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("     CORRELATION ANALYSIS COMPLETED")
print("======================================")