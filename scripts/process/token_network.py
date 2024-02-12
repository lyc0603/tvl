"""
Script to process token network data
"""

import networkx as nx
import json
from environ.constants import PROCESSED_DATA_PATH, SAMPLE_DATA_DICT
import matplotlib.pyplot as plt
import scipy
from tqdm import tqdm


G = nx.DiGraph()

event = "max_tvl"
date = SAMPLE_DATA_DICT[event]

with open(
    PROCESSED_DATA_PATH / "token_breakdown" / f"token_breakdown_{event}.json",
    "r",
    encoding="utf-8",
) as f:
    token_breakdown = json.load(f)

for ptc_name, ptc_dict in token_breakdown["staked_token"].items():
    for receipt_token, _ in tqdm(ptc_dict.items()):
        for staked_token, staked_token_quantity in ptc_dict[receipt_token].items():
            G.add_edge(staked_token, receipt_token)

# draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=30, font_size=8)
plt.show()
