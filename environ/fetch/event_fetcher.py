"""
Class to fetch events from the database
"""
from argparse import RawTextHelpFormatter
import json
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from os import path
from typing import Iterable, Iterator, List, Optional

from eth_typing import Address
from web3 import Web3
from web3.contract import Contract
from web3.types import FilterParams, LogReceipt
from typing import Any
from scripts.w3 import w3


class ContractFetcher:
    """
    Class to fetch events from the database
    """

    def __init__(self, contract: Any) -> None:
        self.contract = contract
        contract_events = [event() for event in self.contract.events]
        self.events_by_topic = {
            event.build_filter().topics[0]: event
            for event in contract_events
            if not event.abi["anonymous"]
        }

    def process_log(self, event: LogReceipt) -> LogReceipt:
        """
        Function to process a log
        """
        topics = event.get("topics")
        if topics and topics[0] in self.events_by_topic:
            event = self.events_by_topic[topics[0]].processLog(event)
        return event

    def process_logs(self, events: list[LogReceipt]) -> list[LogReceipt]:
        """
        Function to process a list of logs
        """
        return [self.process_log(event) for event in events]

    def _fetch_events(self, start_block: int, end_block: int) -> Any:
        """
        Function to fetch events from the database
        """
        event_filter = w3.eth.filter(
            FilterParams(
                address=self.contract.address,
                fromBlock=start_block,
                toBlock=end_block,
            )
        )
        events = event_filter.get_all_entries()
        return self.process_logs(events)


if __name__ == "__main__":
    import json
    from scripts.w3 import w3
    from environ.constants import DATA_PATH

    CONTRACT_ADDRESS = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"
    with open(f"{DATA_PATH}/abi/{CONTRACT_ADDRESS}.json", encoding="utf-8") as f:
        abi = json.load(f)

    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
    fetcher = ContractFetcher(contract=contract)

    print(fetcher._fetch_events(19126088, 19126088))
