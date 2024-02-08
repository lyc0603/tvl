"""
Script to aggregate risk analysis data
"""

import json

from environ.constants import (
    DAI_ADDRESS,
    ETH_ADDRESS,
    ETH_ADDRESS_LOWER,
    PROCESSED_DATA_PATH,
    SAMPLE_DATA_DICT,
    WETH_ADDRESS,
)
from environ.process.risk_analysis import (
    convert_to_plain_quantity,
    get_related_token,
    get_related_token_ptc,
)
from scripts.rep_ptc import non_plf_list

plain_token_dict = {}
for event, date in SAMPLE_DATA_DICT.items():
    plain_token_dict[event] = {}

    ETH_LIST = [WETH_ADDRESS, ETH_ADDRESS, ETH_ADDRESS_LOWER]

    # get related token set
    eth_related_token_set = get_related_token(event, set(ETH_LIST))
    dai_related_token_set = get_related_token(event, set([DAI_ADDRESS]))
    eth_related_only_token_set = eth_related_token_set - dai_related_token_set

    # get related token from protocol
    ptc_related_token_dict = {}
    ptc_related_token_dict = get_related_token_ptc(
        ptc_related_token_dict,
        event,
        non_plf_list,
        eth_related_only_token_set,
        "eth",
    )
    ptc_related_token_dict = get_related_token_ptc(
        ptc_related_token_dict,
        event,
        non_plf_list,
        dai_related_token_set,
        "dai",
    )

    plain_token_dict[event] = {"eth": {}, "dai": {}}

    with open(
        PROCESSED_DATA_PATH / "token_breakdown" / f"token_breakdown_{event}.json",
        "r",
        encoding="utf-8",
    ) as f:
        token_breakdown = json.load(f)

    for token, set_dict in {
        "eth": [eth_related_only_token_set, set(ETH_LIST)],
        "dai": [dai_related_token_set, set([DAI_ADDRESS])],
    }.items():
        for ptc_name, related_token_dict in ptc_related_token_dict[token].items():
            ptc_receipt = token_breakdown["receipt_token"][ptc_name]
            ptc_staked = token_breakdown["staked_token"][ptc_name]
            for related_token, related_token_quantity in related_token_dict.items():

                if related_token in ETH_LIST:
                    plain_token_dict[event][token][
                        related_token
                    ] = related_token_quantity
                else:
                    ratio_list = convert_to_plain_quantity(
                        event,
                        related_token,
                        [],
                        related_token_quantity,
                        set_dict[0],
                        set_dict[1],
                    )
                    quantity = 1
                    for ratio in ratio_list:
                        quantity *= ratio

                    if related_token in plain_token_dict[event][token]:
                        plain_token_dict[event][token][related_token] += quantity
                    else:
                        plain_token_dict[event][token][related_token] = quantity
