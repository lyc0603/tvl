"""
Script to calculate the multiplier for the network
"""

import json
from environ.constants import PROCESSED_DATA_PATH, SAMPLE_DATA_DICT
from environ.fetch.w3 import token_symbol
from tqdm import tqdm

token_set = set()
token_symbol_dict = {}

for event, date in SAMPLE_DATA_DICT.items():
    with open(
        f"{PROCESSED_DATA_PATH}/network/token_breakdown_{event}.json",
        "r",
        encoding="utf-8",
    ) as f:
        token_breakdown_dict = json.load(f)

    for ptc, ptc_dict in token_breakdown_dict["staked_token"].items():
        for token, token_quantity in ptc_dict.items():
            token_set.add(token)

for token in tqdm(token_set):
    token_symbol_dict[token] = token_symbol(token, "latest")

with open(
    f"{PROCESSED_DATA_PATH}/token_symbol_dict.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(token_symbol_dict, f, ensure_ascii=False, indent=4)
