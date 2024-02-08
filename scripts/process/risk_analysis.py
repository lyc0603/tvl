"""
Script to perform risk analysis on the data
"""

from scripts.process.risk_token_relationship import plain_token_dict
from scripts.fetch.plf_eth_related_price import eth_related_price_dict
from environ.constants import (
    WETH_ADDRESS,
    PROCESSED_DATA_PATH,
    ETH_ADDRESS,
    ETH_ADDRESS_LOWER,
    PLAIN_TOKEN_LIST_PLF,
    SAMPLE_DATA_DICT,
    params_dict,
)
import json
from tqdm import tqdm

risk_dict = {}


for params, params_grid in params_dict.items():
    risk_dict[params] = {}
    for params_idx, target_params in enumerate(params_grid[params]):
        risk_dict[params][target_params] = {}
        for event, date in SAMPLE_DATA_DICT.items():
            risk_dict[params][target_params][event] = {}

            eth_price = eth_related_price_dict[event][WETH_ADDRESS]

            PLAIN_TOKEN_LIST = [ETH_ADDRESS, ETH_ADDRESS_LOWER, WETH_ADDRESS]

            with open(
                PROCESSED_DATA_PATH / "risk" / "plf_eth_acct.json",
                "r",
                encoding="utf-8",
            ) as f:
                plf_dict = json.load(f)

            risk_dict[params][target_params][event] = {
                "eth_decline_pct": [],
                "tvl_drop": [],
                "tvr_drop": [],
                "liq_num_mkr": [],
                "liq_num_aave": [],
            }

            # split 0 - 1 into 100 parts
            for eth_decline_pct in tqdm(range(0, 101)):

                plf_dict_risk = plf_dict.copy()

                # calculate the drop of total value locked in the non-plf
                non_plf_tvl_drop = (
                    sum(plain_token_dict[event]["eth"].values())
                    * eth_decline_pct
                    / 100
                    * eth_price
                )

                # calculate the drop of total value redeemable in the non-plf
                non_plf_tvr_drop = 0

                for token, amount in plain_token_dict[event]["eth"].items():
                    if token in PLAIN_TOKEN_LIST:
                        non_plf_tvr_drop += amount * eth_decline_pct / 100 * eth_price

                # calculate the drop of total value locked in the plf
                plf_tvl_drop = 0
                plf_tvr_drop = 0

                liq_num_aave = 0
                liq_num_mkr = 0

                for plf in ["aave", "makerdao"]:
                    system_total_collat = 0
                    system_total_debt = 0

                    for acct in plf_dict_risk[plf].copy():
                        collat_borrowing_power = 0
                        debt_value = 0
                        collateral_value_tvl = 0
                        collateral_value_tvr = 0

                        for idx, collateral in enumerate(acct["collateral"]):
                            linear_tvl_drop = 0
                            linear_tvr_drop = 0

                            collateral_value_tvl += acct["collateral"][idx][
                                "collateral_value"
                            ]

                            if collateral["collateral_address"] in PLAIN_TOKEN_LIST_PLF:
                                collateral_value_tvr += acct["collateral"][idx][
                                    "collateral_value"
                                ]

                            if collateral["collateral_address"] == WETH_ADDRESS:

                                # calculate the drop
                                linear_tvl_drop = (
                                    acct["collateral"][idx]["collateral_value"]
                                    * eth_decline_pct
                                    / 100
                                )
                                linear_tvr_drop = (
                                    acct["collateral"][idx]["collateral_value"]
                                    * eth_decline_pct
                                    / 100
                                )

                                collat_borrowing_power += (
                                    acct["collateral"][idx]["collateral_value"]
                                    * (1 - eth_decline_pct / 100)
                                    * acct["collateral"][idx]["lt"]
                                )
                                system_total_collat += acct["collateral"][idx][
                                    "collateral_value"
                                ] * (1 - eth_decline_pct / 100)
                            else:
                                collat_borrowing_power += (
                                    acct["collateral"][idx]["collateral_value"]
                                    * acct["collateral"][idx]["lt"]
                                )
                                system_total_collat += acct["collateral"][idx][
                                    "collateral_value"
                                ]

                        for idx, debt in enumerate(acct["debt"]):
                            if debt["debt_address"] == WETH_ADDRESS:
                                debt_value += acct["debt"][idx]["debt_value"] * (
                                    1 - eth_decline_pct / 100
                                )
                                system_total_debt += acct["debt"][idx]["debt_value"] * (
                                    1 - eth_decline_pct / 100
                                )
                            else:
                                debt_value += acct["debt"][idx]["debt_value"]
                                system_total_debt += acct["debt"][idx]["debt_value"]
                        # liquidation
                        if plf == "aave":
                            liq_num_aave += 1
                            if (
                                collat_borrowing_power < debt_value
                                and collat_borrowing_power
                                > debt_value
                                * params_grid["$\\psi_{1}^{AAVE}$"][params_idx]
                            ):
                                plf_tvl_drop += (
                                    collateral_value_tvl
                                    * params_grid["$\\delta^{AAVE}$"][params_idx]
                                )
                                plf_tvr_drop += (
                                    collateral_value_tvr
                                    * params_grid["$\\delta^{AAVE}$"][params_idx]
                                )

                            elif (
                                collat_borrowing_power
                                < debt_value
                                * params_grid["$\\psi_{1}^{AAVE}$"][params_idx]
                            ):
                                plf_tvl_drop += collateral_value_tvl
                                plf_tvr_drop += collateral_value_tvr

                            else:
                                plf_tvl_drop += linear_tvl_drop
                                plf_tvr_drop += linear_tvr_drop

                        if plf == "makerdao":
                            liq_num_mkr += 1
                            if (
                                collat_borrowing_power < debt_value
                                and collat_borrowing_power > debt_value
                            ):
                                plf_tvl_drop += (
                                    collateral_value_tvl
                                    * params_grid["$\\delta^{MKR}$"][params_idx]
                                )
                                plf_tvr_drop += (
                                    collateral_value_tvr
                                    * params_grid["$\\delta^{MKR}$"][params_idx]
                                )

                            else:
                                plf_tvl_drop += linear_tvl_drop
                                plf_tvr_drop += linear_tvr_drop

                risk_dict[params][target_params][event]["eth_decline_pct"].append(
                    eth_decline_pct
                )
                risk_dict[params][target_params][event]["tvl_drop"].append(
                    -(non_plf_tvl_drop + plf_tvl_drop)
                )
                risk_dict[params][target_params][event]["tvr_drop"].append(
                    -(non_plf_tvr_drop + plf_tvr_drop)
                )

                risk_dict[params][target_params][event]["liq_num_mkr"].append(
                    liq_num_mkr
                )
                risk_dict[params][target_params][event]["liq_num_aave"].append(
                    liq_num_aave
                )
