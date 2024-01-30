"""This file contains the configuration settings for the market environment."""

from environ.settings import PROJECT_ROOT

# Paths
DATA_PATH = PROJECT_ROOT / "data"
FIGURE_PATH = PROJECT_ROOT / "figures"

# sample date
SAMPLE_DATA_DICT = {
    "Maximum TVL": "2021-12-26",
    "Luna Collapse": "2022-05-09",
    "FTX Collapse": "2022-11-08",
    "Current Date": "2023-07-01",
}
