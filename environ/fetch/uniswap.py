"""
Uniswap Class
"""

from environ.fetch.function_caller import FunctionCaller

UNISWAP_V2_FACTORY_ADDRESS = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
UNISWAP_V3_NFT_POSITION_MANAGER_ADDRESS = "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"


class UniswapV2:
    """
    Uniswap V2 class
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def all_pairs_lenghth(self, block_identifier: int) -> int:
        """
        Function to get the length of all pairs
        """

        caller = FunctionCaller(UNISWAP_V2_FACTORY_ADDRESS, self.w3)
        return caller.call_function("allPairsLength", block_identifier)

    def all_pairs(
        self, block_identifier: int
    ) -> list[tuple[str, str, str, str, str, str, str]]:
        """
        Function to get all pairs
        """

        caller = FunctionCaller(UNISWAP_V2_FACTORY_ADDRESS, self.w3)
        return caller.call_function("allPairs", block_identifier)


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
