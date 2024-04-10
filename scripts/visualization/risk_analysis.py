"""
Script to perform risk analysis on the data
"""

import json

import matplotlib.pyplot as plt

from environ.constants import (
    FIGURE_PATH,
    PROCESSED_DATA_PATH,
    SAMPLE_DATA_DICT,
    params_dict,
)

# from scripts.process.risk_analysis import risk_dict, depeg_dict

COLOR_LIST = ["red", "darkblue", "green"]
PARAMS_NAMEING_MAPPING = {
    "$\\delta_{MKR}$": "mkr_c",
    "$\\delta_{AAVE}$": "aave_c",
    "$\\psi_{1,AAVE}$": "aave_t",
}

with open(f"{PROCESSED_DATA_PATH}/risk/risk_dict.json", "r", encoding="utf-8") as f:
    risk_dict = json.load(f)

with open(f"{PROCESSED_DATA_PATH}/risk/depeg_dict.json", "r", encoding="utf-8") as f:
    depeg_dict = json.load(f)

for event, date in SAMPLE_DATA_DICT.items():
    for params, params_grid in params_dict.items():
        # figure size
        fig, axes = plt.subplots(figsize=(6, 6))

        ls_list = []

        for params_idx, target_params in enumerate(params_grid[params]):
            target_params = str(target_params)
            # figure size
            axes.plot(
                risk_dict[params][target_params][event]["eth_decline_pct"],
                risk_dict[params][target_params][event]["tvl_drop"],
                ls="-",
                color=COLOR_LIST[params_idx],
                label=f"{target_params}",
            )

            axes.plot(
                risk_dict[params][target_params][event]["eth_decline_pct"],
                risk_dict[params][target_params][event]["tvr_drop"],
                ls="dashed",
                color=COLOR_LIST[params_idx],
                label=f"{target_params}",
            )

            ls_list.append(f"{target_params}")

        for params_idx, target_params in enumerate(params_grid[params]):
            target_params = str(target_params)
            # plot the shading after depeg
            if (
                len(depeg_dict[params][target_params][event]["depeg_eth_decline_pct"])
                > 0
            ):
                depeg_start_pcg = depeg_dict[params][target_params][event][
                    "depeg_eth_decline_pct"
                ][0]
                print(params, target_params, event, depeg_start_pcg)
                axes.axvline(
                    x=depeg_start_pcg,
                    color=COLOR_LIST[params_idx],
                    ls="dashdot",
                    alpha=0.5,
                )

        axes.plot(
            [],
            [],
            ls="dashdot",
            color="black",
        )

        lines = axes.get_lines()
        legend1 = plt.legend(
            [lines[i] for i in [0, 1, -1]],
            ["TVL", "TVR", "DAI Depeg"],
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
            title=params,
            title_fontsize="18",
        )
        axes.add_artist(legend1)
        axes.add_artist(legend2)

        # add the grid and increase the opacity and increase the intensity
        plt.grid(alpha=0.3)

        # x and y labels
        plt.xlabel(r"ETH Price Decline in Percentage, $d$", loc="left")

        # set the y label
        plt.ylabel(r"Change in TVL $\Delta_{TVL}$ and TVR $\Delta_{TVR}$ (USD)")

        # increase label and tick size
        axes.xaxis.label.set_size(18)
        axes.yaxis.label.set_size(14)

        # set the x axis range
        axes.xaxis.set_label_coords(0, -0.08)

        # increase the font size
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)

        # set the color of legend 1 line to black
        legend1.get_lines()[0].set_color("black")
        legend1.get_lines()[1].set_color("black")

        plt.gca().yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, loc: "{:.1f}B".format(x / 1e9))
        )
        plt.subplots_adjust(left=0.25)
        plt.tight_layout()
        plt.savefig(
            f"{FIGURE_PATH}/sensitivity_{event}_{PARAMS_NAMEING_MAPPING[params]}.pdf",
            dpi=2000,
        )
        plt.show()
