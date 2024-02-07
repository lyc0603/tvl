"""
Functions to perform risk analysis on the data
"""

from environ.constants import PROCESSED_DATA_PATH, ETH_ADDRESS, WETH_ADDRESS
import json
from typing import Any


def get_related_token(
    event: str, related_token_set: set = set([WETH_ADDRESS, ETH_ADDRESS])
) -> set:
    """
    Function to get the related token set from a given snapshot
    """

    length_last = 0

    while len(related_token_set) > length_last:
        length_last = len(related_token_set)

        with open(
            PROCESSED_DATA_PATH / "token_breakdown" / f"token_breakdown_{event}.json",
            "r",
            encoding="utf-8",
        ) as f:
            token_breakdown_json = json.load(f)

            for _, ptc_dict in token_breakdown_json["staked_token"].items():
                for receipt_token_address, staked_token_dict in ptc_dict.items():
                    for staked_token_address, _ in staked_token_dict.items():
                        if staked_token_address in related_token_set:
                            related_token_set.add(receipt_token_address)

    return related_token_set


def get_related_token_ptc(
    ptc_related_token_dict: dict,
    event: str,
    non_plf_list: list,
    token_set: set,
    token: str,
) -> dict:
    """
    Function to get the related token set from the protocol
    """

    ptc_related_token_dict[token] = {}

    with open(
        PROCESSED_DATA_PATH / "token_breakdown" / f"token_breakdown_{event}.json",
        "r",
        encoding="utf-8",
    ) as f:
        token_breakdown = json.load(f)

    # get protocol related token
    for non_plf_ptc in non_plf_list:
        ptc_name = non_plf_ptc.__class__.__name__
        ptc_related_token_dict[token][ptc_name] = {}

        ptc_breakdown = token_breakdown["staked_token"][ptc_name]
        for _, staked_token_dict in ptc_breakdown.items():
            for staked_token, staked_token_quantity in staked_token_dict.items():
                if staked_token in token_set and staked_token_quantity != 0:
                    ptc_related_token_dict[token][ptc_name][
                        staked_token
                    ] = staked_token_quantity

    return ptc_related_token_dict


def convert_to_plain_quantity(
    event: str,
    token_address: str,
    ratio_list: list,
    staked_quantity: float,
    token_related_set: set,
    plain_token_set: set,
) -> Any:
    """
    Function to convert to plain token quantity using recursion
    """
    derivative_ptc_dict = {}

    with open(
        PROCESSED_DATA_PATH / "token_breakdown" / f"token_breakdown_{event}.json",
        "r",
        encoding="utf-8",
    ) as f:
        token_breakdown = json.load(f)
        for ptc_name, ptc_dict in token_breakdown["receipt_token"].items():
            for receipt_token, _ in ptc_dict.items():
                derivative_ptc_dict[receipt_token] = ptc_name

    if token_address in (token_related_set - plain_token_set):
        ratio_list.append(
            staked_quantity
            / token_breakdown["receipt_token"][derivative_ptc_dict[token_address]][
                token_address
            ]
        )
        for derivative_token, derivative_token_quantity in token_breakdown[
            "staked_token"
        ][derivative_ptc_dict[token_address]][token_address].items():
            if derivative_token in (token_related_set - plain_token_set):
                ratio_list = convert_to_plain_quantity(
                    event,
                    derivative_token,
                    ratio_list,
                    derivative_token_quantity,
                    token_related_set,
                    plain_token_set,
                )
            elif derivative_token in plain_token_set:
                ratio_list.append(derivative_token_quantity)
            else:
                pass

    return ratio_list
