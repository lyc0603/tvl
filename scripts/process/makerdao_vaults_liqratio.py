"""
Script to process MakerDAO vaults
"""

import pandas as pd
from environ.fetch.makerdao import MakerDAO
from scripts.w3 import w3
from environ.constants import (
    SAMPLE_DATA_DICT,
    DATA_PATH,
    PROCESSED_DATA_PATH,
    DAI_ADDRESS,
)
from environ.fetch.block import date_close_to_block
from environ.fetch.w3 import token_decimal
from web3 import Web3
import json

makerdao = MakerDAO(w3)

# get gem bytes mapping
for event, date in SAMPLE_DATA_DICT.items():

    df = []

    gem_bytes_mapping = {}
    block = date_close_to_block(date)
    for ilk in makerdao.list():
        _, _, _, _, gem, _, _, _ = makerdao.info(ilk, block)
        gem_bytes_mapping[Web3.toHex(ilk)] = {}
        gem_bytes_mapping[Web3.toHex(ilk)]["gem"] = gem
        gem_bytes_mapping[Web3.toHex(ilk)]["liq_ratio"] = makerdao.mat(ilk, block)

    with open(DATA_PATH / "makerdao" / f"{event}.json", "r", encoding="utf-8") as f:
        for line in f:
            try:
                line = json.loads(line)
                line["liq_ratio"] = gem_bytes_mapping[line["collateral_type"]][
                    "liq_ratio"
                ]
                line["symbol"] = gem_bytes_mapping[line["collateral_type"]]["gem"]
                df.append(line)
            except Exception as e:  # pylint: disable=broad-except
                pass

    df = pd.DataFrame(df)
    df.to_csv(PROCESSED_DATA_PATH / "makerdao" / f"{event}.csv", index=False)

#  process the collateral and debt amount
token_set = set([DAI_ADDRESS])
token_decimal_dict = {}

for event, date in SAMPLE_DATA_DICT.items():
    df = pd.read_csv(PROCESSED_DATA_PATH / "makerdao" / f"{event}.csv")
    for _, row in df.iterrows():
        token_set.add(row["symbol"])

for token in token_set:
    token_decimal_dict[token] = token_decimal(token, "latest")

for event, date in SAMPLE_DATA_DICT.items():
    df = pd.read_csv(PROCESSED_DATA_PATH / "makerdao" / f"{event}.csv")
    for idx, row in df.iterrows():
        df.at[idx, "collateral_amount"] = float(row["collateral_amount"]) / (
            10 ** token_decimal_dict[row["symbol"]]
        )
        df.at[idx, "debt_amount"] = float(row["debt_amount"]) / (
            10 ** token_decimal_dict[DAI_ADDRESS]
        )

    df.to_csv(PROCESSED_DATA_PATH / "makerdao" / f"{event}.csv", index=False)
