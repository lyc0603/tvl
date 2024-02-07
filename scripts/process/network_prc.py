"""
Script to update edge amounts
"""

import json

from tqdm import tqdm

from environ.constants import PROCESSED_DATA_PATH, SAMPLE_DATA_DICT
from environ.fetch.block import date_close_to_timestamp, date_close_to_block
from environ.fetch.token_price import DeFiLlama

defillama = DeFiLlama()

for event, date in SAMPLE_DATA_DICT.items():
    with open(
        f"{PROCESSED_DATA_PATH}/network/node_edge_quantity_{event}.json",
        "r",
        encoding="utf-8",
    ) as f:
        with open(
            f"{PROCESSED_DATA_PATH}/network/node_edge_amount_{event}.json",
            "w",
            encoding="utf-8",
        ) as f2:
            for line in tqdm(f):
                line = json.loads(line)
                try:
                    if line["value"] != 0:
                        try:
                            token_price = defillama.get_price(
                                line["token_address"],
                                date_close_to_timestamp(date),
                            )
                        except:  # pylint: disable=bare-except
                            try:
                                token_price = defillama.get_price_with_derivative(
                                    line["token_address"],
                                    event,
                                    date_close_to_timestamp(date),
                                    date_close_to_block(date),
                                )
                            except:  # pylint: disable=bare-except
                                token_price = defillama.get_lp_price(
                                    line["token_address"],
                                    date_close_to_timestamp(date),
                                    event,
                                )

                        line["value"] = token_price * line["value"]

                    json.dump(line, f2)
                    f2.write("\n")
                except Exception as e:
                    print(line["token_address"], e)
