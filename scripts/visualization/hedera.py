"""
Script to plot the network
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import text
import numpy as np

# from scripts.process.network_data_visualization import GRAPH_DICT
from scripts.process.hedera_network_data_visualization import (
    GRAPH_DICT,
    multiplier_dict,
    protocol_dict_not_zero,
)

# from scripts.process.network_multiplier import multiplier_dict
from environ.constants import SAMPLE_DATA_DICT, FIGURE_PATH

NODE_SIZE_SCALER = 10000
EDGE_WIDTHS_LINEAR_SCALER = 250
EDGE_WIDTHS_NONLINEAR_SCALER = 2

for event, date in SAMPLE_DATA_DICT.items():
    # Plot the network
    pos = nx.circular_layout(GRAPH_DICT[event])
    plt.figure(figsize=(15, 8))

    node_sizes = nx.get_node_attributes(GRAPH_DICT[event], "tvl")
    edge_widths = nx.get_edge_attributes(GRAPH_DICT[event], "weight")
    node_colors = [multiplier_dict[event][ptc] for ptc in protocol_dict_not_zero[event]]
    cmap = plt.cm.Reds

    # add color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, max(node_colors)))
    sm.set_array([])
    rgba_colors = sm.to_rgba(node_colors)

    nx.draw_networkx_nodes(
        GRAPH_DICT[event],
        pos,
        node_size=[i / NODE_SIZE_SCALER for i in list(node_sizes.values())],
        node_color=node_colors,
        cmap=cmap,
    )

    # draw the edges with the weights
    nx.draw_networkx_edges(
        GRAPH_DICT[event],
        pos,
        width=[
            i ** (1 / EDGE_WIDTHS_NONLINEAR_SCALER) / EDGE_WIDTHS_LINEAR_SCALER
            for i in list(edge_widths.values())
        ],
        node_size=[
            i ** (1 / EDGE_WIDTHS_NONLINEAR_SCALER) / NODE_SIZE_SCALER
            for i in list(node_sizes.values())
        ],
        connectionstyle="arc3,rad=0.3",
        arrowstyle="-|>",
    )

    # nx.draw(
    #     GRAPH_DICT[event],
    #     pos,
    #     node_color=node_colors,
    #     node_size=[i / NODE_SIZE_SCALER for i in list(node_sizes.values())],
    #     cmap=cmap,
    # )

    nx.draw_networkx_labels(
        GRAPH_DICT[event], pos, font_size=20, verticalalignment="bottom"
    )

    # make the color bar tick size bigger
    cbar = plt.colorbar(sm, orientation="vertical")
    cbar.ax.tick_params(labelsize=20)
    cbar.set_label("TVL / TVR", rotation=270, labelpad=20, fontsize=20)

    plt.tight_layout()
    plt.show()
    plt.savefig(
        f"{FIGURE_PATH}/hedera_network_{event}.pdf",
        dpi=2000,
    )
