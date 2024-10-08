"""
Script to perform risk analysis on the data
"""

import json
from tqdm import tqdm
from environ.constants import (
    ETH_ADDRESS,
    ETH_ADDRESS_LOWER,
    PLAIN_TOKEN_LIST_PLF,
    PROCESSED_DATA_PATH,
    SAMPLE_DATA_DICT,
    WETH_ADDRESS,
    params_dict,
    GAS_FEE_DICT,
    GAS_USED,
)
from scripts.fetch.plf_eth_related_price import eth_related_price_dict
from scripts.process.risk_token_relationship import plain_token_dict

risk_dict = {}
depeg_dict = {}
with open(f"{PROCESSED_DATA_PATH}/mkr_tvl_debt.json", "r", encoding="utf-8") as f:
    mkr_tvl_debt_dict = json.load(f)
for params, params_grid in params_dict.items():
    risk_dict[params] = {}
    depeg_dict[params] = {}
    for params_idx, target_params in enumerate(params_grid[params]):
        risk_dict[params][target_params] = {}
        depeg_dict[params][target_params] = {}
        for event, date in SAMPLE_DATA_DICT.items():
            risk_dict[params][target_params][event] = {}
            depeg_dict[params][target_params][event] = {}
            eth_price = eth_related_price_dict[event][WETH_ADDRESS]
            PLAIN_TOKEN_LIST = [ETH_ADDRESS, ETH_ADDRESS_LOWER, WETH_ADDRESS]
            with open(
                PROCESSED_DATA_PATH / "risk" / f"plf_eth_acct_{event}.json",
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
            depeg_dict[params][target_params][event] = {
                "depeg_eth_decline_pct": [],
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
                # depeg
                mkr_tvl_drop = 0
                mkr_debt_drop = 0
                depeg_tvl_drop = 0
                for plf in ["aave", "makerdao"]:
                    system_total_collat = 0
                    system_total_debt = 0
                    for acct in plf_dict_risk[plf].copy():
                        collat_borrowing_power = 0
                        debt_value = 0
                        collateral_value_tvl = 0
                        collateral_value_tvr = 0
                        collateral_value_after = 0
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
                                collateral_value_after += acct["collateral"][idx][
                                    "collateral_value"
                                ] * (1 - eth_decline_pct / 100)
                                # system_total_collat += acct["collateral"][idx][
                                #     "collateral_value"
                                # ] * (1 - eth_decline_pct / 100)
                            else:
                                collat_borrowing_power += (
                                    acct["collateral"][idx]["collateral_value"]
                                    * acct["collateral"][idx]["lt"]
                                )
                                collateral_value_after += acct["collateral"][idx][
                                    "collateral_value"
                                ]
                                # system_total_collat += acct["collateral"][idx][
                                #     "collateral_value"
                                # ]
                        for idx, debt in enumerate(acct["debt"]):
                            if debt["debt_address"] == WETH_ADDRESS:
                                debt_value += acct["debt"][idx]["debt_value"] * (
                                    1 - eth_decline_pct / 100
                                )
                                # system_total_debt += acct["debt"][idx]["debt_value"] * (
                                #     1 - eth_decline_pct / 100
                                # )
                            else:
                                debt_value += acct["debt"][idx]["debt_value"]
                                # system_total_debt += acct["debt"][idx]["debt_value"]
                        # liquidation
                        if plf == "aave":
                            liq_num_aave += 1
                            if (collat_borrowing_power < debt_value) & (
                                (
                                    collateral_value_after
                                    - debt_value
                                    - params_grid["$gasFees$"][params_idx]
                                    * GAS_FEE_DICT[event]
                                    * GAS_USED
                                )
                                > 0
                            ):
                                plf_tvl_drop += (
                                    collateral_value_tvl
                                    * params_grid["$\\delta_{AAVE}$"][params_idx]
                                )
                                plf_tvr_drop += (
                                    collateral_value_tvr
                                    * params_grid["$\\delta_{AAVE}$"][params_idx]
                                )
                            else:
                                plf_tvl_drop += linear_tvl_drop
                                plf_tvr_drop += linear_tvr_drop
                        else:
                            liq_num_mkr += 1
                            if (collat_borrowing_power < debt_value) & (
                                (
                                    collateral_value_after
                                    - debt_value
                                    - params_grid["$gasFees$"][params_idx]
                                    * GAS_FEE_DICT[event]
                                    * GAS_USED
                                )
                                > 0
                            ):
                                plf_tvl_drop += (
                                    collateral_value_tvl
                                    * params_grid["$\\delta_{MKR}$"][params_idx]
                                )
                                plf_tvr_drop += (
                                    collateral_value_tvr
                                    * params_grid["$\\delta_{MKR}$"][params_idx]
                                )
                                mkr_tvl_drop += (
                                    collateral_value_tvl
                                    * params_grid["$\\delta_{MKR}$"][params_idx]
                                )
                                mkr_debt_drop += (
                                    debt_value
                                    * params_grid["$\\delta_{MKR}$"][params_idx]
                                )
                            else:
                                plf_tvl_drop += linear_tvl_drop
                                plf_tvr_drop += linear_tvr_drop
                                mkr_tvl_drop += linear_tvl_drop
                # DAI depeg
                if (
                    mkr_tvl_debt_dict[event]["tvl"] - mkr_tvl_drop
                    < mkr_tvl_debt_dict[event]["debt"] - mkr_debt_drop
                ):
                    dai_price = (
                        mkr_tvl_debt_dict[event]["debt"]
                        / mkr_tvl_debt_dict[event]["tvl"]
                    )
                    depeg_dict[params][target_params][event][
                        "depeg_eth_decline_pct"
                    ].append(eth_decline_pct)
                    depeg_tvl_drop = (
                        sum(plain_token_dict[event]["dai"].values())
                        + mkr_tvl_debt_dict[event]["dsr"]
                    ) * (1 - dai_price)
                risk_dict[params][target_params][event]["eth_decline_pct"].append(
                    eth_decline_pct
                )
                risk_dict[params][target_params][event]["tvl_drop"].append(
                    -(non_plf_tvl_drop + plf_tvl_drop + depeg_tvl_drop)
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

with open(
    PROCESSED_DATA_PATH / "risk" / "risk_dict.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(risk_dict, f, ensure_ascii=False, indent=4)

with open(
    PROCESSED_DATA_PATH / "risk" / "depeg_dict.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(depeg_dict, f, ensure_ascii=False, indent=4)
