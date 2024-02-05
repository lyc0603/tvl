"""
Script to fetch token breakdown
"""

import json

from tqdm import tqdm

from environ.constants import DATA_PATH, SAMPLE_DATA_DICT
from environ.fetch.block import date_close_to_block
from scripts.rep_ptc import ptc_list

for ptc_class in ptc_list:
    for event, date in tqdm(SAMPLE_DATA_DICT.items()):
        block = date_close_to_block(date)
        token_breakdown = ptc_class.token_breakdown(block)
        with open(
            f"{DATA_PATH}/token_breakdown/{ptc_class.__class__.__name__}_{event}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(token_breakdown, f, indent=4)
