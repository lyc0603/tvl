"""
Convex Class
"""

from tqdm import tqdm

from environ.fetch.function_caller import FunctionCaller
from environ.fetch.w3 import total_supply_normalized, token_balance_normalized

CONVEX_BOOSTER_ADDRESS = "0xF403C135812408BFbE8713b5A23a04b3D48AAE31"


# PROXY - TOKEN mapping
GOV_TOKEN_DICT = {
    "0x989AEb4d175e16225E39E87d0D97A3360524AD80": "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",
    "0x59CFCD384746ec3035299D90782Be065e466800B": "0xc8418aF6358FFddA74e09Ca9CC3Fe03Ca6aDC5b0",
    "0xf3BD66ca9b2b43F6Aa11afa6F4Dfdc836150d973": "0x574C154C83432B0A45BA3ad2429C3fA242eD7359",
}


class Convex:
    """
    Convex Class
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def pool_length(self, block_identifier: int | str) -> int:
        """
        Function to get the pool list
        """

        caller = FunctionCaller(CONVEX_BOOSTER_ADDRESS, self.w3)
        return caller.call_function("poolLength", block_identifier)

    def pool_info(self, index: int, block_identifier: int | str) -> str:
        """
        Function to get the pool address
        """

        caller = FunctionCaller(CONVEX_BOOSTER_ADDRESS, self.w3)
        return caller.call_function("poolInfo", block_identifier, [index])

    def token_breakdown(self, block_identifier: int | str) -> dict:
        """
        Function to get the token breakdown
        """

        token_breakdown_dict = {"receipt_token": {}, "staked_token": {}}

        # governance token
        for voter_proxy_vecrv_address, vecrv_address in GOV_TOKEN_DICT.items():
            token_breakdown_dict["staked_token"][voter_proxy_vecrv_address] = {
                vecrv_address: token_balance_normalized(
                    vecrv_address, voter_proxy_vecrv_address, block_identifier
                )
            }
        print(token_breakdown_dict)
        # liquidity pool
        for pool_idx in tqdm(range(self.pool_length(block_identifier))):
            stake_token_address, receipt_token_address, gauge_address, _, _, _ = (
                self.pool_info(pool_idx, block_identifier)
            )

            token_breakdown_dict["receipt_token"][receipt_token_address] = (
                total_supply_normalized(receipt_token_address, block_identifier)
            )
            token_breakdown_dict["staked_token"][receipt_token_address] = {
                stake_token_address: token_balance_normalized(
                    stake_token_address, gauge_address, block_identifier
                )
            }

        return token_breakdown_dict


if __name__ == "__main__":
    from pprint import pprint

    from environ.fetch.w3 import w3

    ptc = Convex(w3)
    pprint(ptc.token_breakdown("latest"))
    pass
