"""
Script to connect to a local or remote node and interact with it.
"""

from web3 import HTTPProvider, Web3

w3 = Web3(HTTPProvider("http://localhost:8545"))
