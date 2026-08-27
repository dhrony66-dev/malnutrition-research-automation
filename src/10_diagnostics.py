import pandas as pd
import yaml
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    roc_auc_score
)


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

categorical_variables = config[
    "variables"
]["categorical"]

outcome_variables = config[
    "variables"
]["outcomes"]


# ==========================================
# CONVERT BINARY OUTCOMES
# ==========================================

for outcome in outcome_variables:

    if outcome in df.columns:

        df[outcome] = df[outcome].map(
            {
                "No": 0,
                "Yes": 1
            }
        )


# ==========================================
# PREDICTOR VARIABLES
# ==========================================

predictor_variables = (
    numeric_variables
    + categorical_variables
)


X = df[
    predictor_variables
].copy()


# ==========================================
# PREPROCESSING
# ==========================================

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
# START
# ==========================================

print("\n======================================")
print("       MODEL DIAGNOSTICS")
print("======================================")


print("\nPredictor variables:")

for variable in predictor_variables:

    print(
        f" - {variable}"
    )


print("\nOutcome variables:")

for outcome in outcome_variables:

    print(
        f" - {outcome}"
    )


# ==========================================
# RESULTS STORAGE
# ==========================================

diagnostic_results = []


# ==========================================
# RUN MODEL FOR EACH OUTCOME
# ==========================================

for outcome in outcome_variables:

    print("\n--------------------------------------")

    print(
        f"OUTCOME: {outcome.upper()}"
    )

    print("--------------------------------------")


    # ======================================
    # OUTCOME
    # ======================================

    y = df[outcome]


    # ======================================
    # TRAIN TEST SPLIT
    # ======================================

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )
    )


    print(
        f"Training observations: "
        f"{len(X_train)}"
    )

    print(
        f"Testing observations: "
        f"{len(X_test)}"
    )


    # ======================================
    # LOGISTIC REGRESSION PIPELINE
    # ======================================

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


    # ======================================
    # FIT MODEL
    # ======================================

    model.fit(
        X_train,
        y_train
    )


    # ======================================
    # PREDICTIONS
    # ======================================

    y_pred = model.predict(
        X_test
    )

    y_prob = model.predict_proba(
        X_test
    )[:, 1]


    # ======================================
    # CONFUSION MATRIX
    # ======================================

    cm = confusion_matrix(
        y_test,
        y_pred
    )


    tn, fp, fn, tp = cm.ravel()


    # ======================================
    # ACCURACY
    # ======================================

    accuracy = accuracy_score(
        y_test,
        y_pred
    )


    # ======================================
    # SENSITIVITY
    # ======================================

    if (tp + fn) > 0:

        sensitivity = (
            tp / (tp + fn)
        )

    else:

        sensitivity = np.nan


    # ======================================
    # SPECIFICITY
    # ======================================

    if (tn + fp) > 0:

        specificity = (
            tn / (tn + fp)
        )

    else:

        specificity = np.nan


    # ======================================
    # ROC-AUC
    # ======================================

    auc = roc_auc_score(
        y_test,
        y_prob
    )


    # ======================================
    # DISPLAY RESULTS
    # ======================================

    print(
        f"Accuracy: "
        f"{accuracy:.4f}"
    )

    print(
        f"Sensitivity: "
        f"{sensitivity:.4f}"
    )

    print(
        f"Specificity: "
        f"{specificity:.4f}"
    )

    print(
        f"ROC-AUC: "
        f"{auc:.4f}"
    )


    print(
        f"TN: {tn}, "
        f"FP: {fp}, "
        f"FN: {fn}, "
        f"TP: {tp}"
    )


    # ======================================
    # STORE RESULTS
    # ======================================

    diagnostic_results.append(
        {
            "Outcome": outcome,

            "Training_N": len(X_train),

            "Testing_N": len(X_test),

            "Accuracy": round(
                accuracy,
                4
            ),

            "Sensitivity": round(
                sensitivity,
                4
            ),

            "Specificity": round(
                specificity,
                4
            ),

            "ROC_AUC": round(
                auc,
                4
            ),

            "TN": int(tn),

            "FP": int(fp),

            "FN": int(fn),

            "TP": int(tp)
        }
    )


# ==========================================
# CREATE RESULTS DATAFRAME
# ==========================================

diagnostics_df = pd.DataFrame(
    diagnostic_results
)


# ==========================================
# SAVE RESULTS
# ==========================================

OUTPUT_FILE = (
    TABLES_DIR
    / "model_diagnostics.csv"
)


diagnostics_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# DISPLAY FINAL TABLE
# ==========================================

print("\n--------------------------------------")
print("DIAGNOSTIC SUMMARY")
print("--------------------------------------")

print(
    diagnostics_df.to_string(
        index=False
    )
)


# ==========================================
# OUTPUT LOCATION
# ==========================================

print("\nDiagnostic results saved to:")

print(
    OUTPUT_FILE
)


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("      MODEL DIAGNOSTICS COMPLETED")
print("======================================")