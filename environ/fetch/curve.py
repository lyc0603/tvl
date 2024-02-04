"""
Curve Class
"""

from tqdm import tqdm

from environ.fetch.function_caller import FunctionCaller
from environ.fetch.w3 import total_supply_normalized
from scripts.w3 import w3

META_REGISTRY_ADDRESS = "0xF98B45FA17DE75FB1aD0e7aFD971b0ca00e379fC"
ERROR_ADDRESS = "0x28B0Cf1baFB707F2c6826d10caf6DD901a6540C5"


class Cruve:
    """
    Curve Class
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def pool_count(self, block_identifier: int | str) -> int:
        """
        Function to get the pool list
        """

        caller = FunctionCaller(META_REGISTRY_ADDRESS, self.w3)
        return caller.call_function("pool_count", block_identifier)

    def pool_list(self, index: int, block_identifier: int | str) -> str:
        """
        Function to get the pool address
        """

        caller = FunctionCaller(META_REGISTRY_ADDRESS, self.w3)
        return caller.call_function("pool_list", block_identifier, [index])

    def get_coins(self, pool_address: str, block_identifier: int | str) -> str:
        """
        Function to get the coins address for a pool
        """

        caller = FunctionCaller(META_REGISTRY_ADDRESS, self.w3)
        return caller.call_function("get_coins", block_identifier, [pool_address])

    def get_balances(self, pool_address: str, block_identifier: int | str) -> str:
        """
        Function to get the balances for a pool
        """

        caller = FunctionCaller(META_REGISTRY_ADDRESS, self.w3)
        return caller.call_function("get_balances", block_identifier, [pool_address])

    def get_decimals(self, pool_address: str, block_identifier: int | str) -> list:
        """
        Function to get the decimals for a pool
        """

        caller = FunctionCaller(META_REGISTRY_ADDRESS, self.w3)
        return caller.call_function("get_decimals", block_identifier, [pool_address])

    def get_lp_token(self, pool_address: str, block_identifier: int | str) -> str:
        """
        Function to get the lp token address for a pool
        """

        caller = FunctionCaller(META_REGISTRY_ADDRESS, self.w3)
        return caller.call_function("get_lp_token", block_identifier, [pool_address])

    def get_token_breakdown(self, block_identifier: int | str) -> dict:
        """
        Function to get the token breakdown for a pool
        """

        token_breakdown_dict = {"receipt_token": {}, "staked_token": {}}

        for pool_idx in tqdm(range(self.pool_count(block_identifier))):
            pool_address = self.pool_list(pool_idx, block_identifier)
            if pool_address == ERROR_ADDRESS:
                continue
            lp_token_address = self.get_lp_token(pool_address, block_identifier)
            lp_token_amount = total_supply_normalized(
                lp_token_address, block_identifier
            )
            token_breakdown_dict["receipt_token"][lp_token_address] = lp_token_amount
            token_breakdown_dict["staked_token"][lp_token_address] = {}

            stake_token_address_list = [
                _
                for _ in self.get_coins(pool_address, block_identifier)
                if _ != "0x0000000000000000000000000000000000000000"
            ]
            stake_token_decimal_list = self.get_decimals(
                pool_address, block_identifier
            )[0 : len(stake_token_address_list)]

            for stake_token_idx, stake_token_address in enumerate(
                stake_token_address_list
            ):
                token_breakdown_dict["staked_token"][lp_token_address][
                    stake_token_address
                ] = self.get_balances(pool_address, block_identifier)[
                    stake_token_idx
                ] / (
                    10 ** stake_token_decimal_list[stake_token_idx]
                )

        return token_breakdown_dict


if __name__ == "__main__":
    from pprint import pprint

    ptc = Cruve(w3)
    pprint(ptc.get_token_breakdown("latest"))
