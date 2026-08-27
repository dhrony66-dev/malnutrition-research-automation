import pandas as pd
import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc


# ==========================================
# PROJECT DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# DIRECTORIES
# ==========================================

DATA_DIR = BASE_DIR / "data"
TABLES_DIR = BASE_DIR / "results" / "tables"
FIGURES_DIR = BASE_DIR / "results" / "figures"

FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# DATA FILE
# ==========================================

DATA_PATH = (
    DATA_DIR
    / "final_malnutrition_dataset.csv"
)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    DATA_PATH
)


# ==========================================
# VARIABLES
# ==========================================

numeric_variables = [
    "age_months",
    "birth_weight",
    "dietary_diversity",
    "maternal_bmi"
]

categorical_variables = [
    "sex",
    "mother_education",
    "wealth_index",
    "urban_rural",
    "sanitation",
    "water_source",
    "immunization"
]

outcome_variables = [
    "stunting",
    "wasting",
    "underweight"
]


# ==========================================
# START
# ==========================================

print("\n======================================")
print("    PUBLICATION FIGURES")
print("======================================")


# ==========================================
# PREPARE OUTCOMES
# ==========================================

for outcome in outcome_variables:

    df[outcome] = df[outcome].map(
        {
            "No": 0,
            "Yes": 1
        }
    )


# ==========================================
# PLOT 1
# OUTCOME PREVALENCE
# ==========================================

prevalence = []

for outcome in outcome_variables:

    value = (
        df[outcome].mean()
        * 100
    )

    prevalence.append(value)


plt.figure(
    figsize=(8, 6)
)

plt.bar(
    outcome_variables,
    prevalence
)

plt.ylabel(
    "Prevalence (%)"
)

plt.xlabel(
    "Malnutrition Outcome"
)

plt.title(
    "Prevalence of Malnutrition Outcomes"
)

plt.ylim(
    0,
    max(prevalence) + 10
)

plt.tight_layout()

output_file = (
    FIGURES_DIR
    / "Figure_1_Outcome_Prevalence.png"
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
# PLOT 2
# AGE DISTRIBUTION
# ==========================================

plt.figure(
    figsize=(8, 6)
)

plt.hist(
    df["age_months"],
    bins=15
)

plt.xlabel(
    "Age (months)"
)

plt.ylabel(
    "Frequency"
)

plt.title(
    "Distribution of Child Age"
)

plt.tight_layout()

output_file = (
    FIGURES_DIR
    / "Figure_2_Age_Distribution.png"
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
# PLOT 3
# BIRTH WEIGHT
# ==========================================

plt.figure(
    figsize=(8, 6)
)

plt.hist(
    df["birth_weight"],
    bins=20
)

plt.xlabel(
    "Birth Weight"
)

plt.ylabel(
    "Frequency"
)

plt.title(
    "Distribution of Birth Weight"
)

plt.tight_layout()

output_file = (
    FIGURES_DIR
    / "Figure_3_Birth_Weight_Distribution.png"
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
# PLOT 4
# DIETARY DIVERSITY
# ==========================================

plt.figure(
    figsize=(8, 6)
)

plt.hist(
    df["dietary_diversity"],
    bins=9
)

plt.xlabel(
    "Dietary Diversity Score"
)

plt.ylabel(
    "Frequency"
)

plt.title(
    "Distribution of Dietary Diversity"
)

plt.tight_layout()

output_file = (
    FIGURES_DIR
    / "Figure_4_Dietary_Diversity.png"
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
# PLOT 5
# MATERNAL BMI
# ==========================================

plt.figure(
    figsize=(8, 6)
)

plt.hist(
    df["maternal_bmi"],
    bins=20
)

plt.xlabel(
    "Maternal BMI"
)

plt.ylabel(
    "Frequency"
)

plt.title(
    "Distribution of Maternal BMI"
)

plt.tight_layout()

output_file = (
    FIGURES_DIR
    / "Figure_5_Maternal_BMI_Distribution.png"
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
# PREPROCESSING FOR ROC
# ==========================================

X = df[
    numeric_variables
    + categorical_variables
].copy()


preprocessor = ColumnTransformer(

    transformers=[

        (
            "numeric",
            "passthrough",
            numeric_variables
        ),

        (
            "categorical",
            OneHotEncoder(
                drop="first",
                handle_unknown="ignore"
            ),
            categorical_variables
        )
    ]
)


# ==========================================
# ROC CURVES
# ==========================================

roc_results = {}


for outcome in outcome_variables:

    print(
        f"\nCreating ROC curve: "
        f"{outcome}"
    )


    y = df[outcome]


    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )


    model = Pipeline(
        steps=[

            (
                "preprocessor",
                preprocessor
            ),

            (
                "classifier",
                LogisticRegression(
                    max_iter=1000
                )
            )
        ]
    )


    model.fit(
        X_train,
        y_train
    )


    y_probability = model.predict_proba(
        X_test
    )[:, 1]


    fpr, tpr, thresholds = roc_curve(
        y_test,
        y_probability
    )


    roc_auc = auc(
        fpr,
        tpr
    )


    roc_results[outcome] = roc_auc


    # ======================================
    # CREATE ROC FIGURE
    # ======================================

    plt.figure(
        figsize=(8, 6)
    )

    plt.plot(
        fpr,
        tpr,
        label=f"AUC = {roc_auc:.3f}"
    )

    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--"
    )

    plt.xlabel(
        "False Positive Rate"
    )

    plt.ylabel(
        "True Positive Rate"
    )

    plt.title(
        f"ROC Curve for {outcome.capitalize()}"
    )

    plt.legend(
        loc="lower right"
    )

    plt.tight_layout()


    output_file = (
        FIGURES_DIR
        / f"Figure_ROC_{outcome}.png"
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
# ROC-AUC COMPARISON
# ==========================================

outcomes = list(
    roc_results.keys()
)

auc_values = list(
    roc_results.values()
)


plt.figure(
    figsize=(8, 6)
)

plt.bar(
    outcomes,
    auc_values
)

plt.ylabel(
    "ROC-AUC"
)

plt.xlabel(
    "Malnutrition Outcome"
)

plt.title(
    "Comparison of Model Discrimination"
)

plt.ylim(
    0,
    1
)

plt.tight_layout()


output_file = (
    FIGURES_DIR
    / "Figure_9_ROC_AUC_Comparison.png"
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
# SAVE ROC SUMMARY
# ==========================================

roc_summary = pd.DataFrame(
    {
        "Outcome": outcomes,
        "ROC_AUC": auc_values
    }
)


roc_summary["ROC_AUC"] = (
    roc_summary["ROC_AUC"]
    .round(4)
)


roc_output = (
    TABLES_DIR
    / "roc_auc_summary.csv"
)


roc_summary.to_csv(
    roc_output,
    index=False
)


print(
    f"\nROC summary saved to:"
)

print(
    roc_output
)


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("   PUBLICATION FIGURES COMPLETED")
print("======================================")