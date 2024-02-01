"""
Functions to fetch events data from the ethereum node
"""

import json
from typing import Any, Optional

from retry import retry
from web3 import Web3

from environ.constants import DATA_PATH
from scripts.w3 import w3


class FunctionCaller:
    """
    Class to call functions from the smart contract
    """

    def __init__(self, contract_address: str, w3: Web3 = w3):
        self.contract_address = contract_address
        self.w3 = w3

    def _load_abi(self, erc20: bool = False):
        """
        Function to load the abi of the smart contract
        """

        if erc20:
            with open(DATA_PATH / "abi" / f"erc20.json", "r", encoding="utf-8") as f:
                abi = json.load(f)
            return abi
        else:
            with open(
                DATA_PATH / "abi" / f"{self.contract_address}.json",
                "r",
                encoding="utf-8",
            ) as f:
                abi = json.load(f)
        return abi

    def _get_contract(self, erc20: bool = False):
        """
        Function to get the contract object
        """
        abi = self._load_abi(erc20=erc20)
        contract = self.w3.eth.contract(address=self.contract_address, abi=abi)
        return contract

    @retry(delay=1, backoff=2, tries=3)
    def call_function(
        self,
        function_name: str,
        block_identifier: int | str,
        params: Optional[Any] = None,
        erc20: bool = False,
    ):
        """
        Function to call a function from the smart contract
        """
        contract = self._get_contract(erc20=erc20)
        function = getattr(contract.functions, function_name)

        return (
            function().call(block_identifier=block_identifier)
            if params is None
            else function(*params).call(block_identifier=block_identifier)
        )

    def call_function_batch(
        self, function_name: str, blocks: list[int], erc20: bool = False
    ):
        """
        Function to call a function from the smart contract
        """

        return [
            self.call_function(function_name, block, erc20=erc20) for block in blocks
        ]

    # def call_function_batch_parallel(
    #     self, function_name: str, blocks: list[int], max_workers: int = 20
    # ):
    #     """
    #     Function to call a function from the smart contract
    #     """

    #     def split_into_n_ranges(lst, n):
    #         size = len(lst) // n
    #         start = 0
    #         for i in range(n):
    #             if i == n - 1:
    #                 end = len(lst)
    #             else:
    #                 end = start + size
    #             yield lst[start:end]
    #             start = end

    #     max_workers = min(max_workers, len(blocks))

    #     blocks = list(split_into_n_ranges(blocks, max_workers))
    #     workers = []
    #     for block in blocks:
    #         worker = Thread(
    #             target=self.call_function_batch, args=(function_name, block)
    #         )
    #         workers.append(worker)

    #     for worker in workers:
    #         worker.start()


# if __name__ == "__main__":
#     from datetime import datetime

#     now = datetime.now()
#     caller = FunctionCaller("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")
#     blocks = list(range(16112035, 16113035))
#     caller.call_function_batch_parallel("getTotalPooledEther", blocks)
#     print(datetime.now() - now)

#     now = datetime.now()
#     caller = FunctionCaller("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")
#     blocks = list(range(16112035, 16113035))
#     results = caller.call_function_batch("getTotalPooledEther", blocks)
#     for result in results:
#         pass
#     print(datetime.now() - now)
