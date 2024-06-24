"""
Script to fetch PLF related price data from CoinGecko API
"""

from environ.fetch.token_price import DeFiLlama
from environ.constants import SAMPLE_DATA_DICT, DATA_PATH, DAI_ADDRESS
from environ.fetch.block import date_close_to_block, date_close_to_timestamp
import os
import json
from tqdm import tqdm

defillama = DeFiLlama()

ETH_UNI_TOKEN = [
    "0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852",
    "0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11",
    "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",
    "0xBb2b8038a1640196FbE3e38816F3e67Cba72D940",
    "0xDFC14d2Af169B0D36C4EFF567Ada9b2E0CAE044f",
    "0xa2107FA5B38d9bbd2C461D6EDf11B11A50F6b974",
    "0xd3d2E2692501A5c9Ca623199D38826e513033a17",
]
DAI_UNI_TOKEN = [
    "0x231B7589426Ffe1b75405526fC32aC09D44364c4",
    "0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11",
    "0xAE461cA67B15dc8dc81CE7615e0320dA1A9aB8D5",
    "0xB20bd5D04BE54f870D5C0d3cA85d82b34B836405",
]

PLF_ETH_RELATED_TOKEN = set(
    [
        "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    ]
    + [DAI_ADDRESS]
    + ETH_UNI_TOKEN
    + DAI_UNI_TOKEN
)

eth_related_price_dict = {}

if not os.path.exists(DATA_PATH / "eth_related_price.json"):
    for event, date in SAMPLE_DATA_DICT.items():
        eth_related_price_dict[event] = {}
        for token in tqdm(PLF_ETH_RELATED_TOKEN):
            if token in ETH_UNI_TOKEN + DAI_UNI_TOKEN:
                price = defillama.get_lp_derivative_price(
                    token,
                    event,
                    date_close_to_timestamp(date),
                    date_close_to_block(date),
                )
            else:
                price = defillama.get_price(
                    token,
                    date_close_to_timestamp(date),
                )

            eth_related_price_dict[event][token] = price

    with open(DATA_PATH / "eth_related_price.json", "w", encoding="utf-8") as f:
        json.dump(eth_related_price_dict, f, indent=4)
else:
    with open(DATA_PATH / "eth_related_price.json", "r", encoding="utf-8") as f:
        eth_related_price_dict = json.load(f)
