"""
Script to plot the network
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.pyplot import text
import numpy as np

from scripts.process.network_data_visualization import GRAPH_DICT
from scripts.process.network_multiplier import multiplier_dict
from environ.constants import SAMPLE_DATA_DICT, FIGURE_PATH, PROCESSED_DATA_PATH
from scripts.rep_ptc import ptc_list

NODE_SIZE_SCALER = 1000000
EDGE_WIDTHS_LINEAR_SCALER = 500000000
EDGE_WIDTHS_NONLINEAR_SCALER = 1

for event, date in SAMPLE_DATA_DICT.items():
    # Plot the network
    pos = nx.circular_layout(GRAPH_DICT[event])
    plt.figure(figsize=(15, 8))

    node_sizes = nx.get_node_attributes(GRAPH_DICT[event], "tvl")
    edge_widths = nx.get_edge_attributes(GRAPH_DICT[event], "weight")
    node_colors = [multiplier_dict[event][ptc.__class__.__name__] for ptc in ptc_list]
    cmap = plt.cm.Reds

    nx.draw_networkx_nodes(
        GRAPH_DICT[event],
        pos,
        node_size=[i / NODE_SIZE_SCALER for i in list(node_sizes.values())],
        node_color=node_colors,
        cmap=cmap,
        vmax=6,
        vmin=0,
    )

    # draw the edges with the weights
    nx.draw_networkx_edges(
        GRAPH_DICT[event],
        pos,
        width=[i / EDGE_WIDTHS_LINEAR_SCALER for i in list(edge_widths.values())],
        node_size=[i / NODE_SIZE_SCALER for i in list(node_sizes.values())],
        connectionstyle="arc3,rad=0.3",
        arrowstyle="-|>",
        arrowsize=40,
    )

    # nx.draw(
    #     GRAPH_DICT[event],
    #     pos,
    #     node_color=node_colors,
    #     node_size=[i / NODE_SIZE_SCALER for i in list(node_sizes.values())],
    #     cmap=cmap,
    # )

    nx.draw_networkx_labels(
        GRAPH_DICT[event], pos, font_size=25, verticalalignment="bottom"
    )

    # add color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 6))
    sm.set_array([])

    # make the color bar tick size bigger
    cbar = plt.colorbar(sm, orientation="vertical")
    cbar.ax.tick_params(labelsize=25)
    cbar.set_label(r"$\frac{TVL}{TVR}$", rotation=270, labelpad=40, fontsize=25)

    plt.tight_layout()
    plt.axis("off")
    # plt.show()
    plt.savefig(
        f"{FIGURE_PATH}/network_{event}.pdf",
        dpi=2000,
    )
