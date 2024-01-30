"""
Script to fetch Lido data
"""

from environ.constants import SAMPLE_DATA_DICT
from environ.fetch.block import date_close_to_block
from environ.fetch.function_caller import FunctionCaller
from environ.fetch.w3 import get_account_token_balance
from scripts.lp import lp

results = {}

for event, date in SAMPLE_DATA_DICT.items():
    results[event] = {}

    for token, token_info in lp["lido"].items():
        block = date_close_to_block(date)
        if token_info["func_name"] == "balanceOf":
            results[event][token] = get_account_token_balance(
                token_info["call_address"], token_info["balance_token"], block
            )
        else:
            results[event][token] = FunctionCaller(
                token_info["call_address"]
            ).call_function(token_info["func_name"], block)
