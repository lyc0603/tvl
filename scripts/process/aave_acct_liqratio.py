"""
Script to calculate the liquidation ratio of Aave accounts
"""

import json
from environ.constants import (
    PROCESSED_DATA_PATH,
    DATA_PATH,
    SAMPLE_DATA_DICT,
    WETH_ADDRESS,
    ETH_PRICE_DICT,
)
from environ.fetch.block import date_close_to_block
from environ.fetch.aave import AaveV2
from environ.fetch.w3 import token_decimal
from tqdm import tqdm
from web3 import HTTPProvider, Web3


w3 = Web3(
    HTTPProvider(
        "https://eth-mainnet.g.alchemy.com/v2/20Whs6Xw4uaBBdhUfgsc2gIOIexUJ6Ki"
    )
)
aave = AaveV2(w3)

reserve_data_dict = {}
for event, date in tqdm(SAMPLE_DATA_DICT.items()):
    reserve_data_dict[event] = {}
    block = date_close_to_block(date)
    ETH_PRICE_BENCHMARK = aave.get_asset_price(WETH_ADDRESS, date_close_to_block(date))
    for reserve_address in aave.get_reserve_list(block):
        _, _, lt, _, _, _, _, _, _, _ = aave.get_reserve_configuration_data(
            reserve_address, block
        )

        reserve_price = (
            aave.get_asset_price(reserve_address, block)
            / ETH_PRICE_BENCHMARK
            * ETH_PRICE_DICT[event]
        )

        reserve_data_dict[event][reserve_address] = {
            "lt": lt / 10000,
            "price": reserve_price,
        }

w3 = Web3(HTTPProvider("http://localhost:8545"))
aave = AaveV2(w3)

# fetch reserve and decimal data
reserve_dict = {}
for event, date in SAMPLE_DATA_DICT.items():
    with open(
        DATA_PATH / "aave" / "v2" / f"{event}.json",
        "r",
        encoding="utf-8",
    ) as f:
        for line in tqdm(f):
            line = json.loads(line)
            for reserve_data in line["data"]:

                reserve_dict[reserve_data["reserve_symbol"]] = {}

                reserve_dict[reserve_data["reserve_symbol"]]["atoken_address"] = (
                    reserve_data["atoken_address"]
                )
                reserve_dict[reserve_data["reserve_symbol"]][
                    "stable_debt_token_address"
                ] = reserve_data["stable_debt_token_address"]

                reserve_dict[reserve_data["reserve_symbol"]][
                    "variable_debt_token_address"
                ] = reserve_data["variable_debt_token_address"]

reserve_decimal_data_dict = {}

for reserve_symbol, reserve_data in reserve_dict.items():
    reserve_decimal_data_dict[reserve_symbol] = {
        "reserve_address": aave.underlying_asset_address(
            reserve_data["atoken_address"], "latest"
        ),
        "atoken_decimal": token_decimal(reserve_data["atoken_address"], "latest"),
        "stable_debt_decimal": token_decimal(
            reserve_data["stable_debt_token_address"], "latest"
        ),
        "variable_debt_decimal": token_decimal(
            reserve_data["variable_debt_token_address"], "latest"
        ),
    }


for event, date in SAMPLE_DATA_DICT.items():
    block = date_close_to_block(date)
    with open(
        DATA_PATH / "aave" / "v2" / f"{event}.json",
        "r",
        encoding="utf-8",
    ) as f:
        with open(
            PROCESSED_DATA_PATH / "aave" / "v2" / f"{event}.json",
            "w",
            encoding="utf-8",
        ) as f2:
            for line in tqdm(f):
                try:
                    line = json.loads(line)
                    for reserve_data_idx, reserve_data in enumerate(line["data"]):
                        reserve_address = reserve_decimal_data_dict[
                            reserve_data["reserve_symbol"]
                        ]["reserve_address"]

                        line["data"][reserve_data_idx][
                            "reserve_address"
                        ] = reserve_address

                        for token, balance in {
                            "atoken_decimal": "currentATokenBalance",
                            "stable_debt_decimal": "currentStableDebt",
                            "variable_debt_decimal": "currentVariableDebt",
                        }.items():
                            line["data"][reserve_data_idx][balance] = (
                                line["data"][reserve_data_idx][balance]
                                / 10
                                ** reserve_decimal_data_dict[
                                    reserve_data["reserve_symbol"]
                                ][token]
                            )

                        line["data"][reserve_data_idx]["lt"] = reserve_data_dict[event][
                            reserve_address
                        ]["lt"]

                        line["data"][reserve_data_idx]["reserve_price"] = (
                            reserve_data_dict[event][reserve_address]["price"]
                        )

                    json.dump(line, f2)
                    f2.write("\n")
                except Exception as e:  # pylint: disable=broad-except
                    print(f"Error {e}")
