"""
Script to fetch data from CoinGecko API
"""

import time
from multiprocessing import Pool

import requests
from retry import retry
from tqdm import tqdm

from environ.constants import COINGECKO_API_KEY, DATA_PATH
import json


class CoinGecko:
    """
    Class to fetch data from CoinGecko API
    """

    def __init__(self) -> None:
        pass

    def coins_list(self) -> list[dict[str, str]]:
        """
        Method to fetch the list of coins from CoinGecko API
        """
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url, timeout=60)
        return response.json()

    @retry(delay=1, backoff=2, tries=3)
    def market_data(self, api_key: str, coin_id: str) -> dict:
        """
        Method to fetch the market data of a coin from CoinGecko API
        """
        url = (
            f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            + "/market_chart?vs_currency=usd&days=max"
            + f"&x_cg_demo_api_key={api_key}"
        )
        response = requests.get(url, timeout=60)
        time.sleep(1)
        return response.json()


if __name__ == "__main__":
    cg = CoinGecko()
    cg_id = "matic-network"

    with open(DATA_PATH / "token_price" / f"{cg_id}.json", "w", encoding="utf-8") as f:
        json.dump(cg.market_data(COINGECKO_API_KEY, cg_id), f)
