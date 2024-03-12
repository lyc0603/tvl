"""
Script to fetch the date to block data
"""

import pandas as pd
from tqdm import tqdm

from environ.constants import SAMPLE_DATA_DICT, DATA_PATH
from environ.fetch.block import date_close_to_block

START_DATE = "2020-11-30"
END_DATE = SAMPLE_DATA_DICT["current_date"]

date_range = (
    pd.date_range(START_DATE, END_DATE, freq="D")
    .to_frame(index=False)
    .rename(columns={0: "date"})
)

for date in tqdm(date_range["date"]):
    block = date_close_to_block(date)
    date_range.loc[date_range["date"] == date, "block"] = block

date_range["block"] = date_range["block"].astype(int)
date_range.to_csv(DATA_PATH / "date_to_block.csv", index=False)
