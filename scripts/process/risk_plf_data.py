"""
Script to aggregate plf data
"""

import json
import pandas as pd
from environ.constants import (
    SAMPLE_DATA_DICT,
    DAI_ADDRESS,
    PROCESSED_DATA_PATH,
)
from scripts.process.risk_token_relationship import eth_related_token_set
from scripts.fetch.plf_eth_related_price import eth_related_price_dict

event = "max_tvl"
date = SAMPLE_DATA_DICT[event]

plf_dict = {}

store_list = []

reserve_set = set()

# prcoeess aave v2 data
with open(
    PROCESSED_DATA_PATH / "aave" / "v2" / f"{event}.json",
    "r",
    encoding="utf-8",
) as f:
    for line in f:
        line = json.loads(line)

        eth_related = False
        eth_related_acct_dict = {"collateral": [], "debt": []}

        for reserve in line["data"]:
            if reserve["reserve_address"] in eth_related_token_set:
                eth_related = True
            reserve_set.add(reserve["reserve_address"])

        if eth_related:

            reserve_lt_value = 0
            debt_value = 0

            for reserve in line["data"]:
                # fetch collateral data
                if reserve["currentATokenBalance"] != 0:

                    eth_related_acct_dict["collateral"].append(
                        {
                            "collateral_address": reserve["reserve_address"],
                            "collateral_value": reserve["currentATokenBalance"]
                            * reserve["reserve_price"],
                            "lt": reserve["lt"],
                        }
                    )
                    reserve_lt_value += (
                        reserve["currentATokenBalance"] * reserve["reserve_price"]
                    ) * reserve["lt"]

                if reserve["currentStableDebt"] + reserve["currentVariableDebt"] != 0:
                    eth_related_acct_dict["debt"].append(
                        {
                            "debt_address": reserve["reserve_address"],
                            "debt_value": (
                                reserve["currentStableDebt"]
                                + reserve["currentVariableDebt"]
                            )
                            * reserve["reserve_price"],
                        }
                    )

                    debt_value += (
                        reserve["currentStableDebt"] + reserve["currentVariableDebt"]
                    ) * reserve["reserve_price"]
            if reserve_lt_value >= debt_value:
                store_list.append(eth_related_acct_dict)
            else:
                continue

plf_dict["aave"] = store_list

# process MakerDAO data
store_list = []
df_mkr = pd.read_csv(PROCESSED_DATA_PATH / "makerdao" / f"{event}.csv")

for idx, row in df_mkr.iterrows():
    reserve_set.add(row["symbol"])

    eth_related_acct_dict = {"collateral": [], "debt": []}
    if row["symbol"] in eth_related_token_set and float(row["collateral_amount"]) != 0:
        collateral_value = 0
        debt_value = 0

        eth_related_acct_dict["collateral"].append(
            {
                "collateral_address": row["symbol"],
                "collateral_value": float(row["collateral_amount"])
                * eth_related_price_dict[event][row["symbol"]],
                "lt": 1 / float(row["liq_ratio"]),
            }
        )

        eth_related_acct_dict["debt"].append(
            {
                "debt_address": DAI_ADDRESS,
                "debt_value": float(row["debt_amount"])
                * eth_related_price_dict[event][DAI_ADDRESS],
            }
        )

        collateral_value += (
            float(row["collateral_amount"])
            * eth_related_price_dict[event][row["symbol"]]
            * (1 / float(row["liq_ratio"]))
        )

        debt_value += (
            float(row["debt_amount"]) * eth_related_price_dict[event][DAI_ADDRESS]
        )

        if collateral_value >= debt_value:
            store_list.append(eth_related_acct_dict)
        else:
            continue

plf_dict["makerdao"] = store_list

with open(
    PROCESSED_DATA_PATH / "risk" / "plf_eth_acct.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(plf_dict, f, indent=4)
