"""
Convex Class
"""

from environ.fetch.function_caller import FunctionCaller

CONVEX_BOOSTER_ADDRESS = "0xF403C135812408BFbE8713b5A23a04b3D48AAE31"


class Convex:
    """
    Convex Class
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def pool_length(self, block_identifier: int) -> list[str]:
        """
        Function to get the pool list
        """

        caller = FunctionCaller(CONVEX_BOOSTER_ADDRESS, self.w3)
        return caller.call_function("poolLength", block_identifier)

    def pool_info(self, index: int, block_identifier: int) -> str:
        """
        Function to get the pool address
        """

        caller = FunctionCaller(CONVEX_BOOSTER_ADDRESS, self.w3)
        return caller.call_function("poolInfo", block_identifier, [index])
