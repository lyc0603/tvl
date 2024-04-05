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

GRAPH_DICT = {}
multiplier_dict = {}
protocol_dict_not_zero = {}
tvl_dict = {}

ptc_list = ["SaucerSwap", "Stader", "DaVinciGraph", "HeliSwap", "Pangolin"]
CLASS_DEFILLAMA_MAPPING = {
    "SaucerSwap": ["saucerswap"],
    "Stader": ["stader"],
    "DaVinciGraph": ["davincigraph"],
    "HeliSwap": ["heliswap"],
    "Pangolin": ["pangolin"],
}
for event, date in SAMPLE_DATA_DICT.items():

    # initialize the graph
    G = nx.DiGraph()
    multiplier_dict[event] = {}
    protocol_dict_not_zero[event] = []
    tvl_dict[event] = {"flows": []}

    ptc_multiplier_not_one = []

    # node info
    for ptc in ptc_list:
        PTC_NAME = ptc
        tvl_total = 0
        for defillama_name in CLASS_DEFILLAMA_MAPPING[PTC_NAME]:
            with open(
                f"{DATA_PATH}/defillama/tvl/{defillama_name}.json",
                "r",
                encoding="utf-8",
            ) as f:
                tvl_data = json.load(f)
                for tvl_dict in tvl_data["chainTvls"]["Hedera"]["tvl"]:
                    if tvl_dict["date"] == date_close_to_timestamp(
                        SAMPLE_DATA_DICT[event]
                    ):
                        tvl_total += tvl_dict["totalLiquidityUSD"]
                        break

        if (PTC_NAME == "Pangolin") & (event == "current_date"):
            tvl_total = 180270
        if tvl_total != 0:
            G.add_node(
                PTC_NAME,
                tvl=tvl_total,
            )
            multiplier_dict[event][PTC_NAME] = tvl_total
            protocol_dict_not_zero[event].append(PTC_NAME)

    # edge info
    for ptc in ptc_list:
        PTC_NAME_SOURCE = ptc
        for ptc in ptc_list:
            PTC_NAME_TARGET = ptc
            value = 0
            with open(
                f"{PROCESSED_DATA_PATH}/network/hedera_node_edge_amount_{event}.json",
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
                multiplier_dict[event][PTC_NAME_TARGET] = multiplier_dict[event][
                    PTC_NAME_TARGET
                ] / (multiplier_dict[event][PTC_NAME_TARGET] - value)
                ptc_multiplier_not_one.append(PTC_NAME_TARGET)

    for protocol in [
        _ for _ in protocol_dict_not_zero[event] if _ not in ptc_multiplier_not_one
    ]:
        multiplier_dict[event][protocol] = 1

    GRAPH_DICT[event] = G
