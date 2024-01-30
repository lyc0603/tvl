"""
Function to import the web3 object
"""

import json

from environ.constants import DATA_PATH
from scripts.w3 import w3


def get_account_token_balance(
    token_address: str, account_address: str, block_identifier: int = "latest"
):
    """
    Function to get the balance of a token in an account
    """

    with open(DATA_PATH / "abi" / "erc20.json", "r", encoding="utf-8") as f:
        erc20_abi = json.load(f)

    return (
        w3.eth.contract(address=token_address, abi=erc20_abi)
        .functions.balanceOf(account_address)
        .call(block_identifier=block_identifier)
    )


if __name__ == "__main__":
    print(
        get_account_token_balance(
            "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
            "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
        )
    )
