"""
Uniswap Class
"""

from tqdm import tqdm

from environ.fetch.function_caller import FunctionCaller
from environ.fetch.w3 import token_decimal, total_supply_normalized

UNISWAP_V2_FACTORY_ADDRESS = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
UNISWAP_V3_NFT_POSITION_MANAGER_ADDRESS = "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"


class UniswapV2:
    """
    Uniswap V2 class
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def all_pairs_lenghth(self, block_identifier: int | str) -> int:
        """
        Function to get the length of all pairs
        """

        caller = FunctionCaller(UNISWAP_V2_FACTORY_ADDRESS, self.w3)
        return caller.call_function("allPairsLength", block_identifier)

    def all_pairs(self, pool_idx: int, block_identifier: int | str) -> str:
        """
        Function to get all pairs
        """

        caller = FunctionCaller(UNISWAP_V2_FACTORY_ADDRESS, self.w3)
        return caller.call_function("allPairs", block_identifier, [pool_idx])

    def token0(self, pair_address: str, block_identifier: int | str) -> str:
        """
        Function to get token0
        """

        caller = FunctionCaller(pair_address, self.w3)
        return caller.call_function("token0", block_identifier, uni=True)

    def token1(self, pair_address: str, block_identifier: int | str) -> str:
        """
        Function to get token1
        """

        caller = FunctionCaller(pair_address, self.w3)
        return caller.call_function("token1", block_identifier, uni=True)

    def get_reserves(
        self, pair_address: str, block_identifier: int | str
    ) -> tuple[int, int, int]:
        """
        Function to get reserves
        """

        caller = FunctionCaller(pair_address, self.w3)
        return caller.call_function("getReserves", block_identifier, uni=True)

    def token_breakdown(self, block_identifier: int | str) -> dict:
        """
        Function to get the token breakdown
        """

        token_breakdown_dict = {"receipt_token": {}, "staked_token": {}}

        # liquidity pool
        for pair_idx in tqdm(range(self.all_pairs_lenghth(block_identifier))):
            try:
                pair_address = self.all_pairs(pair_idx, block_identifier)
                token0_address = self.token0(pair_address, block_identifier)
                token1_address = self.token1(pair_address, block_identifier)
                token0_reserve, token1_reserve, _ = self.get_reserves(
                    pair_address, block_identifier
                )

                token_breakdown_dict["receipt_token"][pair_address] = (
                    total_supply_normalized(pair_address, block_identifier)
                )

                token_breakdown_dict["staked_token"][pair_address] = {
                    token0_address: token0_reserve
                    / (10 ** token_decimal(token0_address, block_identifier)),
                    token1_address: token1_reserve
                    / (10 ** token_decimal(token1_address, block_identifier)),
                }

            except Exception as e:
                print(f"Error: {e}, pair_idx: {pair_idx}")
        return token_breakdown_dict


class UniswapV3:
    """
    Uniswap V3 class
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def positions(self, block_identifier: int) -> list[tuple[str, str, str]]:
        """
        Function to get all positions
        """

        caller = FunctionCaller(UNISWAP_V3_NFT_POSITION_MANAGER_ADDRESS, self.w3)
        return caller.call_function("positions", block_identifier)


if __name__ == "__main__":
    from scripts.w3 import w3

    ptc = UniswapV2(w3)

    # print(ptc.all_pairs(0, "latest"))
    # print(ptc.all_pairs_lenghth("latest"))
    # print(ptc.token0(ptc.all_pairs(0, "latest"), "latest"))
    # print(ptc.token1(ptc.all_pairs(0, "latest"), "latest"))
    # print(ptc.get_reserves(ptc.all_pairs(0, "latest"), "latest"))
    print(ptc.token_breakdown("latest"))
