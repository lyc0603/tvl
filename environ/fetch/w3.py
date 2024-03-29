"""
Function to import the web3 object
"""

from environ.fetch.function_caller import FunctionCaller
from scripts.w3 import w3


def token_decimal(token_address: str, block_identifier: int | str) -> int:
    """
    Function to get the decimal of a token
    """
    caller = FunctionCaller(token_address, w3)
    return caller.call_function("decimals", block_identifier, erc20=True)


def token_balance(
    token_address: str, account_address: str, block_identifier: int | str
) -> int:
    """
    Function to get the balance of a token
    """
    caller = FunctionCaller(token_address, w3)
    return caller.call_function(
        "balanceOf", block_identifier, [account_address], erc20=True
    )


def total_supply(token_address: str, block_identifier: int | str) -> int:
    """
    Function to get the total supply of a token
    """
    caller = FunctionCaller(token_address, w3)
    return caller.call_function("totalSupply", block_identifier, erc20=True)


def token_balance_normalized(
    token_address: str, account_address: str, block_identifier: int | str
) -> float:
    """
    Function to get the balance of a token
    """
    balance = token_balance(token_address, account_address, block_identifier)
    decimal = token_decimal(token_address, block_identifier)
    return balance / (10**decimal)


def total_supply_normalized(token_address: str, block_identifier: int | str) -> float:
    """
    Function to get the total supply of a token
    """
    supply = total_supply(token_address, block_identifier)
    decimal = token_decimal(token_address, block_identifier)
    return supply / (10**decimal)


def token_symbol(token_address: str, block_identifier: int | str) -> str:
    """
    Function to get the symbol of a token
    """
    caller = FunctionCaller(token_address, w3)
    return caller.call_function("symbol", block_identifier, erc20=True)


if __name__ == "__main__":
    print(token_decimal("0x3Ed3B47Dd13EC9a98b44e6204A523E766B225811", "latest"))
