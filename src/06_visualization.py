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
# FIGURE OUTPUT DIRECTORY
# ==========================================

FIGURES_DIR = BASE_DIR / "results" / "figures"

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
print("       VISUALIZATION STARTED")
print("======================================")


# ==========================================
# NUMERIC VARIABLE DISTRIBUTIONS
# ==========================================

for variable in numeric_variables:

    if variable not in df.columns:
        continue

    plt.figure(figsize=(8, 5))

    plt.hist(
        df[variable].dropna(),
        bins=20
    )

    plt.title(
        f"Distribution of {variable}"
    )

    plt.xlabel(variable)

    plt.ylabel("Frequency")

    plt.tight_layout()


    output_file = (
        FIGURES_DIR
        / f"{variable}_distribution.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output_file}"
    )


# ==========================================
# OUTCOME PREVALENCE
# ==========================================

for outcome in outcome_variables:

    if outcome not in df.columns:
        continue

    counts = (
        df[outcome]
        .value_counts()
    )

    plt.figure(figsize=(7, 5))

    counts.plot(
        kind="bar"
    )

    plt.title(
        f"{outcome.capitalize()} Prevalence"
    )

    plt.xlabel(outcome)

    plt.ylabel("Number of children")

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()


    output_file = (
        FIGURES_DIR
        / f"{outcome}_prevalence.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output_file}"
    )


# ==========================================
# CATEGORICAL VARIABLE DISTRIBUTIONS
# ==========================================

for variable in categorical_variables:

    if variable not in df.columns:
        continue

    counts = (
        df[variable]
        .value_counts()
    )

    plt.figure(figsize=(8, 5))

    counts.plot(
        kind="bar"
    )

    plt.title(
        f"Distribution of {variable}"
    )

    plt.xlabel(variable)

    plt.ylabel("Frequency")

    plt.xticks(
        rotation=30,
        ha="right"
    )

    plt.tight_layout()


    output_file = (
        FIGURES_DIR
        / f"{variable}_distribution.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output_file}"
    )


# ==========================================
# AGE DISTRIBUTION BY SEX
# ==========================================

if (
    "age_months" in df.columns
    and "sex" in df.columns
):

    groups = []

    labels = []

    for sex in df["sex"].dropna().unique():

        groups.append(
            df.loc[
                df["sex"] == sex,
                "age_months"
            ]
        )

        labels.append(sex)


    plt.figure(figsize=(8, 5))

    plt.boxplot(
        groups,
        tick_labels=labels
    )

    plt.title(
        "Age Distribution by Sex"
    )

    plt.xlabel("Sex")

    plt.ylabel("Age in months")

    plt.tight_layout()


    output_file = (
        FIGURES_DIR
        / "age_distribution_by_sex.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Saved: {output_file}"
    )


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("       VISUALIZATION COMPLETED")
print("======================================")