"""
Script to fetch all events in aave v3
"""

from eth_tools.event_fetcher import EventFetcher, FetchTask

from environ.constants import DATA_PATH, SAMPLE_DATA_DICT
from environ.fetch.block import date_close_to_block
from scripts.w3 import w3

V2_POOL = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"
V3_POOL = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"


fetcher = EventFetcher(w3)

# Fetch events from Aave V2
task = FetchTask.from_dict(
    {
        "address": V2_POOL,
        "abi": f"{DATA_PATH}/abi/{V2_POOL}.json",
        "start_block": 11362579,
        "end_block": date_close_to_block(SAMPLE_DATA_DICT["current_date"]),
    }
)
fetcher.fetch_and_persist_events(task, f"{DATA_PATH}/aave/v2_events.jsonl.gz")

# # Fetch events from Aave V3
# task = FetchTask.from_dict(
#     {
#         "address": V3_POOL,
#         "abi": f"{DATA_PATH}/abi/{V3_POOL}.json",
#         "start_block": 16291127,
#         "end_block": date_close_to_block(SAMPLE_DATA_DICT["current_date"]),
#     }
# )
# fetcher.fetch_and_persist_events(task, f"{DATA_PATH}/aave/v3_events.jsonl.gz")
