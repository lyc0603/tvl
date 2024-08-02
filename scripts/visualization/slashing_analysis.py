"""
Script to perform slashing analysis on the data
"""

import json

import matplotlib.pyplot as plt

from environ.constants import (
    FIGURE_PATH,
    PROCESSED_DATA_PATH,
    SAMPLE_DATA_DICT,
    params_dict,
    EVENT_MAPPING,
)

DEFAULT_PARAMS_SET = ("$\\delta_{MKR}$", "1")

# from scripts.process.risk_analysis import risk_dict, depeg_dict

COLOR_LIST = ["red", "darkblue", "green"]
PARAMS_NAMEING_MAPPING = {
    "$\\delta_{MKR}$": "mkr_c",
    "$\\delta_{AAVE}$": "aave_c",
    "$\\psi_{1,AAVE}$": "aave_t",
}

for num_node_operator in range(1, 4, 1):
    with open(
        f"{PROCESSED_DATA_PATH}/risk/risk_dict_slashing_{num_node_operator}.json",
        "r",
        encoding="utf-8",
    ) as f:
        risk_dict = json.load(f)

    with open(
        f"{PROCESSED_DATA_PATH}/risk/depeg_dict_slashing_{num_node_operator}.json",
        "r",
        encoding="utf-8",
    ) as f:
        depeg_dict = json.load(f)

    # figure size
    fig, axes = plt.subplots(figsize=(9, 4))
    ls_list = []

    for event_idx, (event, date) in enumerate(SAMPLE_DATA_DICT.items()):

        params, target_params = DEFAULT_PARAMS_SET

        # figure size
        axes.plot(
            risk_dict[params][target_params][event]["eth_decline_pct"],
            risk_dict[params][target_params][event]["tvl_drop"],
            ls="-",
            color=COLOR_LIST[event_idx],
            label=f"{event}",
        )

        axes.plot(
            risk_dict[params][target_params][event]["eth_decline_pct"],
            risk_dict[params][target_params][event]["tvr_drop"],
            ls="dashed",
            color=COLOR_LIST[event_idx],
            label=f"{event}",
        )

        ls_list.append(f"{EVENT_MAPPING[event]}")

    axes.plot(
        [],
        [],
        ls="dashdot",
        color="black",
    )

    lines = axes.get_lines()
    legend1 = plt.legend(
        [lines[i] for i in [0, 1]],
        ["TVL", "TVR"],
        frameon=False,
        loc="upper right",
        prop={"size": 18},
    )
    legend2 = plt.legend(
        [lines[i] for i in [0, 2, 4]],
        ls_list,
        frameon=False,
        loc="lower left",
        prop={"size": 18},
        title="Event",
        title_fontsize="18",
    )
    axes.add_artist(legend1)
    axes.add_artist(legend2)

    # add the grid and increase the opacity and increase the intensity
    plt.grid(alpha=0.3)

    # x and y labels
    plt.xlabel(r"Slashed Validator in Percentage", loc="left")

    # set the y label
    plt.ylabel(r"Change in TVL $\Delta_{TVL}$ and TVR $\Delta_{TVR}$ (USD)")

    # increase label and tick size
    axes.xaxis.label.set_size(16)
    axes.yaxis.label.set_size(12)

    # set the x axis range
    axes.xaxis.set_label_coords(0.15, -0.08)

    # increase the font size
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    # set the color of legend 1 line to black
    legend1.get_lines()[0].set_color("black")
    legend1.get_lines()[1].set_color("black")

    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:.1f}M".format(x / 1e6))
    )
    plt.subplots_adjust(left=0.25)
    plt.tight_layout()
    plt.savefig(
        f"{FIGURE_PATH}/sensitivity_slashing_{num_node_operator}.pdf",
        dpi=2000,
    )
    plt.show()
