"""
Script to fetch MakerDAO vaults data
"""

import json

from tqdm import tqdm
from web3 import Web3

from environ.constants import DATA_PATH, SAMPLE_DATA_DICT
from environ.fetch.block import date_close_to_block
from environ.fetch.makerdao import MakerDAO
from environ.json_encoder import JSONEncoder

makerdao = MakerDAO()

results = {}

for event, date in SAMPLE_DATA_DICT.items():
    block = date_close_to_block(date)
    cdp_num = makerdao.cdpi(block)
    with open(DATA_PATH / "makerdao" / f"{event}.json", "w", encoding="utf-8") as f:
        for cdp_id in tqdm(range(1, cdp_num + 1, 1)):
            ilk_info = makerdao.ilks(cdp_id, block)
            collateral_amount, debt_amount = makerdao.urns_data(
                ilk_info, makerdao.urns(cdp_id, block), block
            )

            line = {
                "cdp_id": cdp_id,
                "collateral_type": Web3.to_hex(ilk_info),
                "collateral_amount": collateral_amount,
                "debt_amount": debt_amount,
            }

            json.dump(line, f, cls=JSONEncoder)
            f.write("\n")
