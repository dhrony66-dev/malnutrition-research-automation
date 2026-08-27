import pandas as pd
from pathlib import Path


# ==========================================
# PROJECT DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# DIRECTORIES
# ==========================================

TABLES_DIR = BASE_DIR / "results" / "tables"

TABLES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# START
# ==========================================

print("\n======================================")
print("       PUBLICATION TABLES")
print("======================================")


# ==========================================
# TABLE 1
# NUMERIC DESCRIPTIVE STATISTICS
# ==========================================

numeric_file = (
    TABLES_DIR
    / "numeric_descriptive_statistics.csv"
)

numeric_df = pd.read_csv(
    numeric_file
)


numeric_output = (
    TABLES_DIR
    / "Table_1_Numeric_Descriptive_Statistics.csv"
)


numeric_df.to_csv(
    numeric_output,
    index=False
)


print("\nTable 1 created:")
print(numeric_output)


# ==========================================
# TABLE 1B
# CATEGORICAL DESCRIPTIVE STATISTICS
# ==========================================

categorical_file = (
    TABLES_DIR
    / "categorical_descriptive_statistics.csv"
)

categorical_df = pd.read_csv(
    categorical_file
)


categorical_output = (
    TABLES_DIR
    / "Table_1B_Categorical_Descriptive_Statistics.csv"
)


categorical_df.to_csv(
    categorical_output,
    index=False
)


print("\nTable 1B created:")
print(categorical_output)


# ==========================================
# TABLE 2
# CORRELATION MATRIX
# ==========================================

correlation_file = (
    TABLES_DIR
    / "correlation_matrix.csv"
)

correlation_df = pd.read_csv(
    correlation_file
)


correlation_output = (
    TABLES_DIR
    / "Table_2_Correlation_Matrix.csv"
)


correlation_df.to_csv(
    correlation_output,
    index=False
)


print("\nTable 2 created:")
print(correlation_output)


# ==========================================
# TABLE 3
# VIF
# ==========================================

vif_file = (
    TABLES_DIR
    / "vif_results.csv"
)

vif_df = pd.read_csv(
    vif_file
)


vif_output = (
    TABLES_DIR
    / "Table_3_VIF_Analysis.csv"
)


vif_df.to_csv(
    vif_output,
    index=False
)


print("\nTable 3 created:")
print(vif_output)


# ==========================================
# TABLE 4
# LOGISTIC REGRESSION
# ==========================================

regression_file = (
    TABLES_DIR
    / "logistic_regression_results.csv"
)

regression_df = pd.read_csv(
    regression_file
)


regression_output = (
    TABLES_DIR
    / "Table_4_Logistic_Regression.csv"
)


regression_df.to_csv(
    regression_output,
    index=False
)


print("\nTable 4 created:")
print(regression_output)


# ==========================================
# TABLE 5
# MODEL DIAGNOSTICS
# ==========================================

diagnostics_file = (
    TABLES_DIR
    / "model_diagnostics.csv"
)

diagnostics_df = pd.read_csv(
    diagnostics_file
)


diagnostics_output = (
    TABLES_DIR
    / "Table_5_Model_Diagnostics.csv"
)


diagnostics_df.to_csv(
    diagnostics_output,
    index=False
)


print("\nTable 5 created:")
print(diagnostics_output)


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("     PUBLICATION TABLES COMPLETED")
print("======================================")