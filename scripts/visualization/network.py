"""
Script to plot the network
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import numpy as np

from scripts.process.network_data_visualization import G

NODE_SIZE_SCALER = 1000000
EDGE_WIDTHS_LINEAR_SCALER = 500000000
EDGE_WIDTHS_NONLINEAR_SCALER = 1


# Plot the network
pos = nx.circular_layout(G)
plt.figure(figsize=(16, 12))

node_sizes = nx.get_node_attributes(G, "tvl")
edge_widths = nx.get_edge_attributes(G, "weight")


# plt.title(
#     label="Directional Trading Volume among Top 50 Pools in Uniswap "
#     + " at "
#     + date_str,
#     fontdict={"fontsize": 12},
#     loc="center",
# )

# nx.draw(
#     G,
#     node_size=[i / NODE_SIZE_SCALER for i in list(node_sizes.values())],
#     pos=pos,
#     with_labels=True,
#     connectionstyle="arc3,rad=0.3",
# )

nx.draw_networkx_nodes(
    G,
    pos,
    node_size=[i / NODE_SIZE_SCALER for i in list(node_sizes.values())],
)

# draw the edges with the weights
nx.draw_networkx_edges(
    G,
    pos,
    width=[i / EDGE_WIDTHS_LINEAR_SCALER for i in list(edge_widths.values())],
    node_size=[i / NODE_SIZE_SCALER for i in list(node_sizes.values())],
    connectionstyle="arc3,rad=0.3",
    arrowstyle="-|>",
)


nx.draw_networkx_labels(G, pos, font_size=12, verticalalignment="bottom")

plt.show()
