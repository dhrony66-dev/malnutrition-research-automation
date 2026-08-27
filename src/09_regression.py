import pandas as pd
import yaml
import numpy as np
from pathlib import Path
import statsmodels.formula.api as smf


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

        df[outcome] = (
            df[outcome]
            .map({
                "No": 0,
                "Yes": 1
            })
        )


# ==========================================
# BUILD FORMULA
# ==========================================

numeric_terms = numeric_variables


categorical_terms = [
    f"C({variable})"
    for variable in categorical_variables
]


predictor_terms = (
    numeric_terms
    + categorical_terms
)


formula_predictors = " + ".join(
    predictor_terms
)


# ==========================================
# START
# ==========================================

print("\n======================================")
print("       LOGISTIC REGRESSION")
print("======================================")


print("\nPredictors:")

for variable in predictor_terms:

    print(
        f" - {variable}"
    )


print("\nOutcomes:")

for outcome in outcome_variables:

    print(
        f" - {outcome}"
    )


# ==========================================
# RUN MODELS
# ==========================================

all_results = []


for outcome in outcome_variables:

    print("\n--------------------------------------")

    print(
        f"MODEL: {outcome.upper()}"
    )

    print("--------------------------------------")


    formula = (
        f"{outcome} ~ "
        f"{formula_predictors}"
    )


    print(
        f"\nFormula:\n{formula}"
    )


    try:

        model = smf.logit(
            formula=formula,
            data=df
        ).fit(
            disp=False
        )


        # ==================================
        # MODEL PARAMETERS
        # ==================================

        coefficients = model.params

        standard_errors = model.bse

        p_values = model.pvalues

        odds_ratios = np.exp(
            coefficients
        )

        confidence_intervals = (
            model.conf_int()
        )

        confidence_intervals[
            "OR_Lower"
        ] = np.exp(
            confidence_intervals[0]
        )

        confidence_intervals[
            "OR_Upper"
        ] = np.exp(
            confidence_intervals[1]
        )


        # ==================================
        # STORE RESULTS
        # ==================================

        for variable in coefficients.index:

            all_results.append(
                {
                    "Outcome": outcome,
                    "Variable": variable,
                    "Coefficient":
                        coefficients[variable],
                    "Std_Error":
                        standard_errors[variable],
                    "Odds_Ratio":
                        odds_ratios[variable],
                    "CI_Lower":
                        confidence_intervals.loc[
                            variable,
                            "OR_Lower"
                        ],
                    "CI_Upper":
                        confidence_intervals.loc[
                            variable,
                            "OR_Upper"
                        ],
                    "P_Value":
                        p_values[variable]
                }
            )


        # ==================================
        # MODEL SUMMARY
        # ==================================

        print(
            f"\nObservations: "
            f"{int(model.nobs)}"
        )

        print(
            f"Pseudo R-squared: "
            f"{model.prsquared:.4f}"
        )

        print(
            f"AIC: "
            f"{model.aic:.2f}"
        )

        print(
            f"BIC: "
            f"{model.bic:.2f}"
        )


    except Exception as error:

        print(
            f"\nModel failed for "
            f"{outcome}: {error}"
        )


# ==========================================
# CREATE RESULTS DATAFRAME
# ==========================================

results_df = pd.DataFrame(
    all_results
)


# ==========================================
# ROUND RESULTS
# ==========================================

if not results_df.empty:

    results_df[
        "Coefficient"
    ] = results_df[
        "Coefficient"
    ].round(4)

    results_df[
        "Std_Error"
    ] = results_df[
        "Std_Error"
    ].round(4)

    results_df[
        "Odds_Ratio"
    ] = results_df[
        "Odds_Ratio"
    ].round(4)

    results_df[
        "CI_Lower"
    ] = results_df[
        "CI_Lower"
    ].round(4)

    results_df[
        "CI_Upper"
    ] = results_df[
        "CI_Upper"
    ].round(4)

    results_df[
        "P_Value"
    ] = results_df[
        "P_Value"
    ].round(4)


# ==========================================
# SAVE RESULTS
# ==========================================

OUTPUT_FILE = (
    TABLES_DIR
    / "logistic_regression_results.csv"
)


results_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nResults saved to:")

print(
    OUTPUT_FILE
)


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("   LOGISTIC REGRESSION COMPLETED")
print("======================================")