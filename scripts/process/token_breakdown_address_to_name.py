"""
Script to convert address to name
"""

import json
from environ.constants import PROCESSED_DATA_PATH, ETH_ADDRESS, SAMPLE_DATA_DICT
from environ.fetch.w3 import token_symbol
from environ.fetch.block import date_close_to_block
from environ.fetch.uniswap import UniswapV2
from scripts.w3 import w3
from tqdm import tqdm

event = "max_tvl"

receipt_token = {}
staked_token = {}

with open(
    f"{PROCESSED_DATA_PATH}/network/token_breakdown_{event}.json",
    "r",
    encoding="utf-8",
) as f:
    node_edge_amount = json.load(f)

    for ptc_name, token_dict in tqdm(node_edge_amount["receipt_token"].items()):
        receipt_token[ptc_name] = {}
        staked_token[ptc_name] = {}
        for receipt_token_address, token_amount in token_dict.items():
            if receipt_token_address == ETH_ADDRESS:
                receipt_token_symbol = "ETH"
            else:
                receipt_token_symbol = token_symbol(
                    receipt_token_address,
                    date_close_to_block(SAMPLE_DATA_DICT[event]),
                )
            receipt_token[ptc_name][receipt_token_symbol] = token_amount
            staked_token[ptc_name][receipt_token_symbol] = {}

            for _, staked_token_dict in node_edge_amount["staked_token"][ptc_name][
                receipt_token_address
            ].items():
                for (
                    staked_token_address,
                    staked_token_amount,
                ) in staked_token_dict.items():
                    if staked_token_address == ETH_ADDRESS:
                        staked_token_symbol = "ETH"
                    else:
                        staked_token_symbol = token_symbol(
                            staked_token_address,
                            date_close_to_block(SAMPLE_DATA_DICT[event]),
                        )

                        if staked_token_symbol == "UNI-V2":
                            ptc = UniswapV2(w3)
                            token0 = ptc.token0(
                                staked_token_address, SAMPLE_DATA_DICT[event]
                            )
                            token1 = ptc.token1(
                                staked_token_address, SAMPLE_DATA_DICT[event]
                            )
                            staked_token_symbol = f"{token1}-{token0}-UNI-V2"

                    staked_token[ptc_name][receipt_token_symbol][
                        staked_token_symbol
                    ] = staked_token_amount

with open(
    f"{PROCESSED_DATA_PATH}/token_breakdown/token_breakdown_{event}_symbol.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        {"receipt_token": receipt_token, "staked_token": staked_token},
        f,
        ensure_ascii=False,
        indent=4,
    )
