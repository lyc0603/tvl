"""
Script to process MakerDAO vaults
"""

import pandas as pd
from environ.fetch.makerdao import MakerDAO
from scripts.w3 import w3
from environ.constants import SAMPLE_DATA_DICT, DATA_PATH, PROCESSED_DATA_PATH
from environ.fetch.block import date_close_to_block
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
