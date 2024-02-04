"""
Class to fetch the token price
"""

import requests
import time


class DeFiLlama:
    """
    Class to fetch the token price
    """

    def __init__(self) -> None:
        pass

    def get_price(self, token_address: str, timestamp: int) -> float:
        """
        Function to get the price of the token
        """

        response = requests.get(
            f"https://coins.llama.fi/prices/historical/{timestamp}"
            + f"/ethereum:{token_address}?searchWidth=4h",
            timeout=60,
        )
        return response.json()["coins"][f"ethereum:{token_address}"]["price"]


if __name__ == "__main__":
    defillama = DeFiLlama()
    print(defillama.get_price("0xdF574c24545E5FfEcb9a659c229253D4111d87e1", 1648680149))
