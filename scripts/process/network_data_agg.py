"""
Script to process network data
"""

import json

from tqdm import tqdm
from environ.constants import DATA_PATH, PROCESSED_DATA_PATH
from environ.fetch.block import date_close_to_block
from scripts.rep_ptc import event_dict

for event, event_dict in event_dict.items():
    receipt_token_dict = {}
    staked_token_dict = {}

    for ptc_class in tqdm(event_dict["ptc"]):
        block = date_close_to_block(event_dict["date"])
        PROTOCOL_CLASS_NAME = ptc_class.__class__.__name__
        with open(
            f"{DATA_PATH}/token_breakdown/{PROTOCOL_CLASS_NAME}_{event}.json",
            "r",
            encoding="utf-8",
        ) as f:
            token_breakdown = json.load(f)

        receipt_token_dict[PROTOCOL_CLASS_NAME] = token_breakdown["receipt_token"]
        staked_token_dict[PROTOCOL_CLASS_NAME] = {}

        for receipt_token, staked_token_info in token_breakdown["staked_token"].items():
            for (
                staked_token_address,
                staked_token_quantity,
            ) in staked_token_info.items():
                staked_token_dict[PROTOCOL_CLASS_NAME].setdefault(
                    staked_token_address, 0
                )
                staked_token_dict[PROTOCOL_CLASS_NAME][
                    staked_token_address
                ] += staked_token_quantity

    agg_dict = {
        "receipt_token": receipt_token_dict,
        "staked_token": staked_token_dict,
    }

    with open(
        f"{PROCESSED_DATA_PATH}/network/token_breakdown_{event}.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(agg_dict, f, indent=4)
