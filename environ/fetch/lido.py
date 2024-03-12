"""
Lido Class
"""

from environ.fetch.function_caller import FunctionCaller

ETH_ADDRESS = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
STETH_ADDRRESS = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84"
WSTETH_ADDRESS = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"
STMATIC_ADDRESS = "0x9ee91F9f426fA633d227f7a9b000E28b9dfd8599"


class Lido:
    """
    Lido class
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def get_total_pooled_ether(self, block_identifier: int):
        """
        Get total pooled ether
        """
        caller = FunctionCaller(STETH_ADDRRESS, self.w3)
        return caller.call_function("getTotalPooledEther", block_identifier) / 10 ** (
            caller.call_function("decimals", block_identifier, erc20=True)
        )

    def get_total_pooled_matic(self, block_identifier: int):
        """
        Get total pooled ether
        """
        caller = FunctionCaller(STMATIC_ADDRESS, self.w3)
        return caller.call_function("getTotalPooledMatic", block_identifier) / 10 ** (
            caller.call_function("decimals", block_identifier, erc20=True)
        )

    def balance_of_steth(self, address: str, block_identifier: int):
        """
        Get balance of steth
        """
        caller = FunctionCaller(STETH_ADDRRESS, self.w3)
        return caller.call_function("balanceOf", block_identifier, [address]) / 10 ** (
            caller.call_function("decimals", block_identifier, erc20=True)
        )

    def total_supply_steth(self, block_identifier: int):
        """
        Get total supply of steth
        """
        caller = FunctionCaller(STETH_ADDRRESS, self.w3)
        return caller.call_function(
            "totalSupply", block_identifier, erc20=True
        ) / 10 ** (caller.call_function("decimals", block_identifier, erc20=True))

    def total_supply_wsteth(self, block_identifier: int):
        """
        Get total supply of wsteth
        """
        caller = FunctionCaller(WSTETH_ADDRESS, self.w3)
        return caller.call_function(
            "totalSupply", block_identifier, erc20=True
        ) / 10 ** (caller.call_function("decimals", block_identifier, erc20=True))

    def token_breakdown(self, block_identifier: int):
        """
        Get token breakdown
        """

        token_breakdown_dict = {"receipt_token": {}, "staked_token": {}}

        token_breakdown_dict["receipt_token"] = {
            STETH_ADDRRESS: self.total_supply_steth(block_identifier),
            WSTETH_ADDRESS: self.total_supply_wsteth(block_identifier),
        }

        token_breakdown_dict["staked_token"] = {
            STETH_ADDRRESS: {
                ETH_ADDRESS: self.get_total_pooled_ether(block_identifier)
            },
            WSTETH_ADDRESS: {
                STETH_ADDRRESS: self.balance_of_steth(WSTETH_ADDRESS, block_identifier)
            },
        }

        return token_breakdown_dict


if __name__ == "__main__":
    from pprint import pprint

    from scripts.w3 import w3

    ptc = Lido(w3)
    pprint(ptc.get_total_pooled_matic("latest"))
