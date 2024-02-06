"""
Script to process network data for visualization
"""

import json

import networkx as nx

from environ.constants import (
    PROCESSED_DATA_PATH,
    SAMPLE_DATA_DICT,
    DATA_PATH,
    CLASS_DEFILLAMA_MAPPING,
)
from environ.fetch.block import date_close_to_timestamp
from scripts.rep_ptc import ptc_list

event = "max_tvl"

# initialize the graph
G = nx.DiGraph()

# node info
for ptc in ptc_list:
    PTC_NAME = ptc.__class__.__name__
    tvl_total = 0
    for defillama_name in CLASS_DEFILLAMA_MAPPING[PTC_NAME]:
        with open(
            f"{DATA_PATH}/defillama/tvl/{defillama_name}.json",
            "r",
            encoding="utf-8",
        ) as f:
            tvl_data = json.load(f)
            for tvl_dict in tvl_data["chainTvls"]["Ethereum"]["tvl"]:
                if tvl_dict["date"] == date_close_to_timestamp(SAMPLE_DATA_DICT[event]):
                    tvl_total += tvl_dict["totalLiquidityUSD"]
                    break
    G.add_node(
        PTC_NAME,
        tvl=tvl_total,
    )

# edge info

for ptc in ptc_list:
    PTC_NAME_SOURCE = ptc.__class__.__name__
    for ptc in ptc_list:
        PTC_NAME_TARGET = ptc.__class__.__name__
        value = 0
        with open(
            f"{PROCESSED_DATA_PATH}/network/node_edge_amount_{event}.json",
            "r",
            encoding="utf-8",
        ) as f:
            for line in f:
                line = json.loads(line)
                if (
                    line["source"] == PTC_NAME_SOURCE
                    and line["target"] == PTC_NAME_TARGET
                ):
                    value += line["value"]
        if value != 0:
            G.add_edge(
                PTC_NAME_SOURCE,
                PTC_NAME_TARGET,
                weight=value,
            )
            print(PTC_NAME_SOURCE, PTC_NAME_TARGET, value)
