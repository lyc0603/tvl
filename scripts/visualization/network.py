"""
Script to plot the network
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import numpy as np

from scripts.process.network_data_visualization import GRAPH_DICT
from environ.constants import SAMPLE_DATA_DICT, FIGURE_PATH

NODE_SIZE_SCALER = 1000000
EDGE_WIDTHS_LINEAR_SCALER = 500000000
EDGE_WIDTHS_NONLINEAR_SCALER = 1

for event, date in SAMPLE_DATA_DICT.items():
    # Plot the network
    pos = nx.circular_layout(GRAPH_DICT[event])
    plt.figure(figsize=(16, 12))

    node_sizes = nx.get_node_attributes(GRAPH_DICT[event], "tvl")
    edge_widths = nx.get_edge_attributes(GRAPH_DICT[event], "weight")

    nx.draw_networkx_nodes(
        GRAPH_DICT[event],
        pos,
        node_size=[i / NODE_SIZE_SCALER for i in list(node_sizes.values())],
    )

    # draw the edges with the weights
    nx.draw_networkx_edges(
        GRAPH_DICT[event],
        pos,
        width=[i / EDGE_WIDTHS_LINEAR_SCALER for i in list(edge_widths.values())],
        node_size=[i / NODE_SIZE_SCALER for i in list(node_sizes.values())],
        connectionstyle="arc3,rad=0.3",
        arrowstyle="-|>",
    )

    nx.draw_networkx_labels(
        GRAPH_DICT[event], pos, font_size=12, verticalalignment="bottom"
    )
    plt.tight_layout()
    plt.show()
    plt.savefig(
        f"{FIGURE_PATH}/network_{event}.pdf",
        dpi=2000,
    )
