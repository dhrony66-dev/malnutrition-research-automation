import yaml
from pathlib import Path


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Config file
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"


# Read config
with open(
    CONFIG_PATH,
    "r",
    encoding="utf-8"
) as file:

    config = yaml.safe_load(file)


print("\n======================================")
print("       CONFIGURATION TEST")
print("======================================")


print("\nProject:")
print(
    config["project"]["name"]
)


print("\nInput dataset:")
print(
    config["data"]["input_file"]
)


print("\nNumeric variables:")

for variable in config["variables"]["numeric"]:
    print(
        f" - {variable}"
    )


print("\nCategorical variables:")

for variable in config["variables"]["categorical"]:
    print(
        f" - {variable}"
    )


print("\nOutcomes:")

for outcome in config["variables"]["outcomes"]:
    print(
        f" - {outcome}"
    )


print("\nVIF threshold:")

print(
    config["analysis"]["vif_threshold"]
)


print("\n======================================")
print("       CONFIGURATION WORKING")
print("======================================")