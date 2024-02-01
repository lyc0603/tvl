"""
Curve Class
"""

from environ.fetch.function_caller import FunctionCaller
from scripts.w3 import w3

META_REGISTRY_ADDRESS = "0xF98B45FA17DE75FB1aD0e7aFD971b0ca00e379fC"


class Cruve:
    """
    Curve Class
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def pool_count(self, block_identifier: int) -> list[str]:
        """
        Function to get the pool list
        """

        caller = FunctionCaller(META_REGISTRY_ADDRESS, self.w3)
        return caller.call_function("pool_count", block_identifier)

    def pool_list(self, index: int, block_identifier: int) -> str:
        """
        Function to get the pool address
        """

        caller = FunctionCaller(META_REGISTRY_ADDRESS, self.w3)
        return caller.call_function("pool_list", block_identifier, [index])

    def get_pool(self, pool_address: str, block_identifier: int) -> str:
        """
        Function to get the lp token address for a pool
        """

        caller = FunctionCaller(pool_address, self.w3)
        return caller.call_function("get_lp_token", block_identifier)

    def get_coins(self, pool_address: str, block_identifier: int) -> str:
        """
        Function to get the coins address for a pool
        """

        caller = FunctionCaller(pool_address, self.w3)
        return caller.call_function("get_coins", block_identifier)

    def get_balances(self, pool_address: str, block_identifier: int) -> str:
        """
        Function to get the balances for a pool
        """

        caller = FunctionCaller(pool_address, self.w3)
        return caller.call_function("get_balances", block_identifier)


if __name__ == "__main__":
    curve = Cruve(w3)
    print(curve.pool_count("latest"))
    print(curve.pool_list(0, "latest"))
