"""
Curve Class
"""

from tqdm import tqdm

from environ.fetch.function_caller import FunctionCaller
from environ.fetch.w3 import total_supply_normalized
from scripts.w3 import w3

META_REGISTRY_ADDRESS = "0xF98B45FA17DE75FB1aD0e7aFD971b0ca00e379fC"
META_REGISTRY_DEPLOY_BLOCK = 15732062
V1_REGISTRY_ADDRESS = "0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5"
V1_REGISTRY_DEPLOY_BLOCK = 12195750
V1_REGISTRY_LATEST_ADDRESS = "0xB9fC157394Af804a3578134A6585C0dc9cc990d4"
V1_REGISTRY_LATEST_DEPLOY_BLOCK = 12903979
V2_FACTORY_ADDRESS = "0xF18056Bbd320E96A48e3Fbf8bC061322531aac99"
V2_FACTORY_DEPLOY_BLOCK = 14005321


ERROR_ADDRESS = "0x28B0Cf1baFB707F2c6826d10caf6DD901a6540C5"


class Curve:
    """
    Curve Class
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def pool_count(self, registry_address: str, block_identifier: int | str) -> int:
        """
        Function to get the pool list
        """

        caller = FunctionCaller(registry_address, self.w3)
        return caller.call_function("pool_count", block_identifier)

    def pool_list(
        self, registry_address: str, index: int, block_identifier: int | str
    ) -> str:
        """
        Function to get the pool address
        """

        caller = FunctionCaller(registry_address, self.w3)
        return caller.call_function("pool_list", block_identifier, [index])

    def get_coins(
        self, registry_address: str, pool_address: str, block_identifier: int | str
    ) -> str:
        """
        Function to get the coins address for a pool
        """

        caller = FunctionCaller(registry_address, self.w3)
        return caller.call_function("get_coins", block_identifier, [pool_address])

    def get_balances(
        self, registry_address: str, pool_address: str, block_identifier: int | str
    ) -> str:
        """
        Function to get the balances for a pool
        """

        caller = FunctionCaller(registry_address, self.w3)
        return caller.call_function("get_balances", block_identifier, [pool_address])

    def get_decimals(
        self, registry_address: str, pool_address: str, block_identifier: int | str
    ) -> list:
        """
        Function to get the decimals for a pool
        """

        caller = FunctionCaller(registry_address, self.w3)
        return caller.call_function("get_decimals", block_identifier, [pool_address])

    def get_lp_token(
        self, registry_address: str, pool_address: str, block_identifier: int | str
    ) -> str:
        """
        Function to get the lp token address for a pool
        """

        caller = FunctionCaller(registry_address, self.w3)
        return caller.call_function("get_lp_token", block_identifier, [pool_address])

    def token(self, pool_address: str, block_identifier: int | str) -> str:
        """
        Function to get the lp token address for a v2 factory pool
        """

        caller = FunctionCaller(pool_address, self.w3)
        return caller.call_function(
            "token", block_identifier, abi_temp="curve_v2_factory.json"
        )

    def token_breakdown_address(
        self,
        registry_address: str,
        token_breakdown_dict: dict,
        block_identifier: int | str,
    ) -> dict:
        """
        Function to get the token breakdown for a registry address
        """

        # token_breakdown_dict = {"receipt_token": {}, "staked_token": {}}

        for pool_idx in tqdm(
            range(self.pool_count(registry_address, block_identifier))
        ):
            pool_address = self.pool_list(registry_address, pool_idx, block_identifier)
            if pool_address == ERROR_ADDRESS:
                continue

            if registry_address == V1_REGISTRY_LATEST_ADDRESS:
                lp_token_address = pool_address
            elif registry_address == V2_FACTORY_ADDRESS:
                lp_token_address = self.token(pool_address, block_identifier)
            else:
                lp_token_address = self.get_lp_token(
                    registry_address, pool_address, block_identifier
                )

            lp_token_amount = total_supply_normalized(
                lp_token_address, block_identifier
            )
            token_breakdown_dict["receipt_token"][lp_token_address] = lp_token_amount
            token_breakdown_dict["staked_token"][lp_token_address] = {}

            stake_token_address_list = [
                _
                for _ in self.get_coins(
                    registry_address, pool_address, block_identifier
                )
                if _ != "0x0000000000000000000000000000000000000000"
            ]
            stake_token_decimal_list = self.get_decimals(
                registry_address, pool_address, block_identifier
            )[0 : len(stake_token_address_list)]

            for stake_token_idx, stake_token_address in enumerate(
                stake_token_address_list
            ):
                token_breakdown_dict["staked_token"][lp_token_address][
                    stake_token_address
                ] = self.get_balances(registry_address, pool_address, block_identifier)[
                    stake_token_idx
                ] / (
                    10 ** stake_token_decimal_list[stake_token_idx]
                )

        return token_breakdown_dict

    def token_breakdown(
        self,
        block_identifier: int,
    ) -> dict:
        """
        Function to get the token breakdown
        """
        token_breakdown_dict = {"receipt_token": {}, "staked_token": {}}

        if (
            block_identifier >= V1_REGISTRY_DEPLOY_BLOCK
            and block_identifier < V1_REGISTRY_LATEST_DEPLOY_BLOCK
        ):
            pool_address_list = [V1_REGISTRY_ADDRESS]
        elif (
            block_identifier >= V1_REGISTRY_LATEST_DEPLOY_BLOCK
            and block_identifier < V2_FACTORY_DEPLOY_BLOCK
        ):
            pool_address_list = [V1_REGISTRY_ADDRESS, V1_REGISTRY_LATEST_ADDRESS]
        elif (
            block_identifier >= V2_FACTORY_DEPLOY_BLOCK
            and block_identifier < META_REGISTRY_DEPLOY_BLOCK
        ):
            pool_address_list = [
                V1_REGISTRY_ADDRESS,
                V1_REGISTRY_LATEST_ADDRESS,
                V2_FACTORY_ADDRESS,
            ]
        else:
            pool_address_list = [
                META_REGISTRY_ADDRESS,
            ]

        for registry_address in pool_address_list:
            token_breakdown_dict = self.token_breakdown_address(
                registry_address, token_breakdown_dict, block_identifier
            )

        return token_breakdown_dict


if __name__ == "__main__":
    from pprint import pprint

    ptc = Curve(w3)
