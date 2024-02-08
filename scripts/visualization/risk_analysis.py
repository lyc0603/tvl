"""
Script to perform risk analysis on the data
"""

import matplotlib.pyplot as plt
from environ.constants import SAMPLE_DATA_DICT, params_dict, FIGURE_PATH
from scripts.process.risk_analysis import risk_dict

COLOR_LIST = ["red", "darkblue", "green"]
PARAMS_NAMEING_MAPPING = {
    "$\\delta^{MKR}$": "mkr_c",
    "$\\delta^{AAVE}$": "aave_c",
    "$\\psi_{1}^{AAVE}$": "aave_t",
}


for event, date in SAMPLE_DATA_DICT.items():
    for params, params_grid in params_dict.items():
        fig, axes = plt.subplots(
            figsize=(4, 6),
        )

        ls_list = []

        for params_idx, target_params in enumerate(params_grid[params]):

            # figure size

            axes.plot(
                risk_dict[params][target_params][event]["eth_decline_pct"],
                risk_dict[params][target_params][event]["tvl_drop"],
                ls="-",
                color=COLOR_LIST[params_idx],
                label=f"{params}={target_params}",
            )

            axes.plot(
                risk_dict[params][target_params][event]["eth_decline_pct"],
                risk_dict[params][target_params][event]["tvr_drop"],
                ls="dashed",
                color=COLOR_LIST[params_idx],
                label=f"{params}={target_params}",
            )

            ls_list.append(f"{params}={target_params}")

        lines = axes.get_lines()
        legend1 = plt.legend(
            [
                lines[i]
                for i in [
                    0,
                    1,
                ]
            ],
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
        axes.xaxis.label.set_size(16)
        axes.yaxis.label.set_size(18)

        # set the x axis range
        axes.xaxis.set_label_coords(-0.5, -0.08)

        # increase the font size
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=18)

        # set the color of legend 1 line to black
        legend1.get_lines()[0].set_color("black")
        legend1.get_lines()[1].set_color("black")

        # tight layout
        plt.tight_layout()

        plt.gca().yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, loc: "{:.1f}B".format(x / 1e9))
        )

        plt.savefig(
            f"{FIGURE_PATH}/sensitivity_{event}_{PARAMS_NAMEING_MAPPING[params]}.pdf",
            dpi=2000,
        )
        plt.show()
