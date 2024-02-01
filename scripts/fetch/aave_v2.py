"""
Scripts to fetch data from Aave
"""

import gzip
import json
import os

import pandas as pd
from tqdm import tqdm

from environ.constants import DATA_PATH, SAMPLE_DATA_DICT
from environ.fetch.aave import AaveV2
from environ.fetch.block import date_close_to_block
from environ.json_encoder import JSONEncoder
from scripts.w3 import w3

AaveV2 = AaveV2(w3)

for event, date in SAMPLE_DATA_DICT.items():
    block = date_close_to_block(date)
    token_data = AaveV2.get_token_data(block)

    if not os.path.exists(DATA_PATH / "aave" / "v2" / f"{event}.csv"):
        df_account = pd.DataFrame()
        account_list = set()

        with gzip.open(
            f"{DATA_PATH}/aave/v2/v2_events.jsonl.gz", "rt", encoding="utf-8"
        ) as f:
            for line in f:
                data = json.loads(line)
                if "event" in data and data["blockNumber"] <= block:
                    if data["event"] == "Borrow":
                        account_list.add(data["args"]["onBehalfOf"])

        df_account["account"] = list(account_list)
        df_account["done"] = 0
        df_account.to_csv(DATA_PATH / "aave" / "v2" / f"{event}.csv", index=False)
    else:
        df_account = pd.read_csv(DATA_PATH / "aave" / "v2" / f"{event}.csv")

    df_todo = df_account.loc[df_account["done"] == 0, "account"]

    with open(DATA_PATH / "aave" / "v2" / f"{event}.json", "a", encoding="utf-8") as f:
        for account in tqdm(
            df_todo,
            total=df_todo.shape[0],
        ):
            try:
                user_data_dict = {}

                # (
                #     totalCollateralETH,
                #     totalDebtETH,
                #     availableBorrowsETH,
                #     currentLiquidationThreshold,
                #     ltv,
                #     healthFactor,
                # ) = AaveV2.get_user_account_data(account, block)

                user_data_dict = {
                    "account": account,
                    # "totalCollateralETH": totalCollateralETH,
                    # "totalDebtETH": totalDebtETH,
                    # "availableBorrowsETH": availableBorrowsETH,
                    # "currentLiquidationThreshold": currentLiquidationThreshold,
                    # "ltv": ltv,
                    # "healthFactor": healthFactor,
                    "data": [],
                }

                for _ in token_data:
                    reserve_symbol = _["reserve_symbol"]
                    reserve_address = _["reserve_address"]
                    atoken_address = _["atoken_address"]
                    stable_debt_token_address = _["stable_debt_token_address"]
                    variable_debt_token_address = _["variable_debt_token_address"]

                    (
                        currentATokenBalance,
                        currentStableDebt,
                        currentVariableDebt,
                        principalStableDebt,
                        scaledVariableDebt,
                        stableBorrowRate,
                        liquidityRate,
                        stableRateLastUpdated,
                        usageAsCollateralEnabled,
                    ) = AaveV2.get_user_reserve_data(account, reserve_address, block)

                    if (
                        currentATokenBalance == 0
                        and currentStableDebt == 0
                        and currentVariableDebt == 0
                    ):
                        continue

                    user_data_dict["data"].append(
                        {
                            "reserve_symbol": reserve_symbol,
                            "atoken_address": atoken_address,
                            "stable_debt_token_address": stable_debt_token_address,
                            "variable_debt_token_address": variable_debt_token_address,
                            "currentATokenBalance": currentATokenBalance,
                            "currentStableDebt": currentStableDebt,
                            "currentVariableDebt": currentVariableDebt,
                            "principalStableDebt": principalStableDebt,
                            "scaledVariableDebt": scaledVariableDebt,
                            "stableBorrowRate": stableBorrowRate,
                            "liquidityRate": liquidityRate,
                            "stableRateLastUpdated": stableRateLastUpdated,
                            "usageAsCollateralEnabled": usageAsCollateralEnabled,
                        }
                    )

                json.dump(user_data_dict, f, cls=JSONEncoder)
                f.write("\n")

                df_account.loc[df_account["account"] == account, "done"] = 1
                df_account.to_csv(
                    DATA_PATH / "aave" / "v2" / f"{event}.csv", index=False
                )
            except Exception as e:
                print(f"Error: cannot fetch data for {account}")
