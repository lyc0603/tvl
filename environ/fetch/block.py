"""
Functions to fetch block info 
"""

import requests
import pandas as pd


def date_to_block(date: str):
    """
    Function to convert timestamp to block number
    """

    timestamp = int(pd.Timestamp(date).timestamp())

    return requests.get(
        f"https://coins.llama.fi/block/ethereum/{timestamp}", timeout=60
    ).json()["height"]


def date_close_to_block(date: str):
    """
    Function to convert date to block number
    """

    return date_to_block((pd.Timestamp(date) + pd.Timedelta("1D")).strftime("%Y-%m-%d"))


if __name__ == "__main__":
    print(date_close_to_block("2021-12-26"))
