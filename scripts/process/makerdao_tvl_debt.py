"""
Script to calculate the TVL and Debt of MakerDAO
"""

import json

from environ.constants import DATA_PATH, SAMPLE_DATA_DICT, PROCESSED_DATA_PATH
from environ.fetch.block import date_close_to_timestamp, date_close_to_block
from environ.fetch.makerdao import MakerDAO, DAI_ADDRESS
from environ.fetch.w3 import total_supply_normalized
from scripts.w3 import w3

makerdao = MakerDAO(w3=w3)

mkr_tvl_debt_dict = {}
for event, date in SAMPLE_DATA_DICT.items():

    timestamp = date_close_to_timestamp(SAMPLE_DATA_DICT[event])
    block = date_close_to_block(date)

    mkr_tvl_debt_dict[event] = {
        "tvl": 0,
        "debt": 0,
        "dsr": 0,
    }
    with open(f"{DATA_PATH}/defillama/tvl/makerdao.json", "r", encoding="utf-8") as f:
        makerdao_tvl_data = json.load(f)

    with open(f"{DATA_PATH}/defillama/tvl/maker-rwa.json", "r", encoding="utf-8") as f:
        makerdao_debt_data = json.load(f)

    for tvl_dict in makerdao_tvl_data["tvl"]:
        if tvl_dict["date"] == timestamp:
            mkr_tvl_debt_dict[event]["tvl"] += tvl_dict["totalLiquidityUSD"]
            break

    for tvl_dict in makerdao_debt_data["tvl"]:
        if tvl_dict["date"] == timestamp:
            mkr_tvl_debt_dict[event]["tvl"] += tvl_dict["totalLiquidityUSD"]
            break

    dsr = makerdao.dsr(block)

    mkr_tvl_debt_dict[event]["debt"] = total_supply_normalized(DAI_ADDRESS, block) + dsr
    mkr_tvl_debt_dict[event]["dsr"] = dsr

with open(f"{PROCESSED_DATA_PATH}/mkr_tvl_debt.json", "w", encoding="utf-8") as f:
    json.dump(mkr_tvl_debt_dict, f, indent=4)
