"""
Script to process the network node and edge data
"""

import json

from tqdm import tqdm

from environ.constants import PROCESSED_DATA_PATH

for event in ["max_tvl"]:
    with open(
        f"{PROCESSED_DATA_PATH}/network/token_breakdown_{event}.json",
        "r",
        encoding="utf-8",
    ) as f:
        token_breakdown_agg = json.load(f)

    with open(
        f"{PROCESSED_DATA_PATH}/network/node_edge_quantity_{event}.json",
        "w",
        encoding="utf-8",
    ) as f:
        for receipt_protocol, receipt_token_dict in token_breakdown_agg[
            "receipt_token"
        ].items():
            for receipt_token_address, _ in tqdm(receipt_token_dict.items()):
                for staked_protocol, staked_token_dict in token_breakdown_agg[
                    "staked_token"
                ].items():
                    for (
                        staked_token_address,
                        staked_token_quantity,
                    ) in staked_token_dict.items():
                        if receipt_token_address == staked_token_address:
                            line = {
                                "source": receipt_protocol,
                                "target": staked_protocol,
                                "token_address": receipt_token_address,
                                "value": staked_token_quantity,
                            }

                            json.dump(line, f)
                            f.write("\n")
