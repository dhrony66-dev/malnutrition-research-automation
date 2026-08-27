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
# DATA PATH FROM CONFIG
# ==========================================

DATA_PATH = Path(
    config["data"]["input_file"]
)


# ==========================================
# IMPORT DATA
# ==========================================

print("\n======================================")
print("        DATA IMPORT")
print("======================================")

print("\nReading dataset from:")

print(DATA_PATH)


if not DATA_PATH.exists():

    print("\nERROR: Dataset not found.")

    print(
        f"Expected location: {DATA_PATH}"
    )

    raise FileNotFoundError(
        DATA_PATH
    )


df = pd.read_csv(
    DATA_PATH
)


# ==========================================
# BASIC INFORMATION
# ==========================================

print("\nDataset successfully loaded.")

print(
    f"\nNumber of rows: {df.shape[0]}"
)

print(
    f"Number of columns: {df.shape[1]}"
)


print("\nColumn names:")

print(
    df.columns.tolist()
)


print("\nData types:")

print(
    df.dtypes
)


print("\nFirst 5 rows:")

print(
    df.head()
)


# ==========================================
# COMPLETION
# ==========================================

print("\n======================================")
print("        IMPORT COMPLETED")
print("======================================")