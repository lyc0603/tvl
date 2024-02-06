"""
Script to plot the network
"""

import json
import networkx as nx
from environ.constants import PROCESSED_DATA_PATH
import matplotlib.pyplot as plt
import numpy as np

with open(
    f"{PROCESSED_DATA_PATH}/network/node_edge_amount_max_tvl.json",
    "r",
    encoding="utf-8",
) as f:
    G = nx.Graph()
    for line in f:
        line = json.loads(line)
        if line["value"] != 0:
            G.add_edge(line["source"], line["target"], weight=line["value"])

node_sizes_scaler = 300000
edge_widths_scaler = 500
edge_widths = nx.get_edge_attributes(G, "weight")
# Plot the network
pos = nx.circular_layout(G)
plt.figure(figsize=(16, 12))

# plt.title(
#     label="Directional Trading Volume among Top 50 Pools in Uniswap "
#     + " at "
#     + date_str,
#     fontdict={"fontsize": 12},
#     loc="center",
# )

# nx.draw(G, node_size=node_sizes, pos=pos, with_labels = True, connectionstyle='arc3,rad=0.3')
nx.draw_networkx_nodes(
    G,
    pos,
    alpha=0.8,
)

nx.draw_networkx_edges(
    G,
    pos,
    connectionstyle="arc3,rad=0.2",
    arrowstyle="-|>",
    arrowsize=20,
    alpha=0.3,
    width=[np.sqrt(i) / edge_widths_scaler for i in list(edge_widths.values())],
)
nx.draw_networkx_labels(G, pos, font_size=18, verticalalignment="bottom")
plt.show()
