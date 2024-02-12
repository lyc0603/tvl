"""
Script to calculate the MakerDAO collateral and debt
"""

import json

import pandas as pd
from tqdm import tqdm

from environ.constants import PROCESSED_DATA_PATH, SAMPLE_DATA_DICT
from environ.fetch.block import date_close_to_timestamp, date_close_to_block
from environ.fetch.token_price import DeFiLlama

defillama = DeFiLlama()
token_set = set()

for event, date in tqdm(SAMPLE_DATA_DICT.items(), total=len(SAMPLE_DATA_DICT)):
    mkr = pd.read_csv(PROCESSED_DATA_PATH / "makerdao" / f"{event}.csv")
    for _, row in mkr.iterrows():
        token_set.add(row["symbol"])

token_price_mkr = {}

for event, date in tqdm(SAMPLE_DATA_DICT.items(), total=len(SAMPLE_DATA_DICT)):
    token_price_mkr[event] = {}
    for token in token_set:
        try:
            token_price_mkr[event][token] = defillama.get_price(
                token, date_close_to_timestamp(date)
            )
        except Exception as e:  # pylint: disable=broad-except
            print(e)

with open(
    PROCESSED_DATA_PATH / "makerdao" / "token_price_mkr.json", "w", encoding="utf-8"
) as f:
    f.write(json.dumps(token_price_mkr))
