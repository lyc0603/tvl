"""
Script to connect to a local or remote node and interact with it.
"""

from web3 import HTTPProvider, Web3

# local node
# w3 = Web3(HTTPProvider("http://localhost:8545"))

# remote node
w3 = Web3(
    HTTPProvider(
        "https://eth-mainnet.g.alchemy.com/v2/20Whs6Xw4uaBBdhUfgsc2gIOIexUJ6Ki"
    )
)
