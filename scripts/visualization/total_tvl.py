"""
Script to plot the total TVL, total TVL without double counting, and TVR of the protocol
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from environ.constants import CHAIN_LIST, FIGURE_PATH, SAMPLE_DATA_DICT
from environ.process.preprocess_defillama_tvl import preprocess_ptc_tvl

fig, axes = plt.subplots(
    figsize=(5, 2),
)

PLOT_INFO_DICT = {
    "totalLiquidityUSD": {"label": "$TVL$", "color": "red"},
    "tvl": {"label": "$TVL^{\mathrm{Adj}}$", "color": "blue"},
    "tvr": {"label": "$TVR$", "color": "black"},
}

EVENT_INFO_DICT = {
    "max_tvl": {"label": "Max TVL", "ls": "dashdot"},
    "luna_collapse": {"label": "Luna Collapse", "ls": "dashed"},
    "ftx_collapse": {"label": "FTX Collapse", "ls": "dotted"},
}

for chain in CHAIN_LIST:
    # load the total tvl data
    df_agg = preprocess_ptc_tvl(
        chain=chain,
    )

    # sort the dataframe by date
    df_agg = df_agg.sort_values(by="date", ascending=True)

    # # if the chain is Mixin, ffill the totalLiquidityUSD in 2022-11-06 to 2022-11-08
    # if chain == "Mixin":
    #     df_agg.loc[
    #         (df_agg["date"] >= "2022-11-06") & (df_agg["date"] <= "2022-11-08"),
    #         "totalLiquidityUSD",
    #     ] = df_agg.loc[
    #         (df_agg["date"] == "2022-11-05"),
    #         "totalLiquidityUSD",
    #     ].values[
    #         0
    #     ]

    # plot the tvl with DC, tvl, and tvr
    for col, info in PLOT_INFO_DICT.items():
        axes.plot(
            df_agg["date"],
            df_agg[col],
            # label=info["label"],
            color=info["color"],
            linewidth=1,
        )

    for event, date in SAMPLE_DATA_DICT.items():
        axes.axvline(
            pd.to_datetime(date),
            color="black",
            linewidth=1,
            # label=EVENT_INFO_DICT[event]["label"],
            ls=EVENT_INFO_DICT[event]["ls"],
        )

    lines = axes.get_lines()
    legend1 = plt.legend(
        [
            lines[i]
            for i in [
                0,
                1,
                2,
            ]
        ],
        [info["label"] for _, info in PLOT_INFO_DICT.items()],
        frameon=False,
        loc="upper right",
        bbox_to_anchor=(0.95, 1),
        prop={"size": 7},
        title="Metrics",
        title_fontsize="8",
    )
    legend2 = plt.legend(
        [lines[i] for i in [3, 4, 5]],
        [info["label"] for _, info in EVENT_INFO_DICT.items()],
        frameon=False,
        loc="lower left",
        prop={"size": 7},
        title="Events",
        title_fontsize="8",
    )
    axes.add_artist(legend1)
    axes.add_artist(legend2)

    # # show the legend on the upper left corner
    # plt.legend(loc="upper left")

    # add the grid and increase the opacity and increase the intensity
    plt.grid(alpha=0.3)

    # set the unit of the x axis
    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter("%Y-%m"),
    )
    plt.gca().xaxis.set_major_locator(
        mdates.MonthLocator(interval=3),
    )

    # label the y axis
    plt.ylabel("Dollar Amount", fontsize=10)

    # set the unit of the y axis
    plt.gca().yaxis.get_major_formatter().set_useOffset(False)
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "${:.0f} billion".format(x / 1e9))
    )
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(base=50e9))

    # if the chain is total, make the ticks and legend smaller
    if chain == "Total":
        plt.xticks(fontsize=9)
        plt.yticks(fontsize=9)
        # plt.legend(prop={"size": 6})
    else:
        # if the chain is not total, make the ticks and legend bigger
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=6)
        # plt.legend(prop={"size": 6})

    # rotate the xticks
    plt.xticks(rotation=90)

    # tight layout
    plt.tight_layout()

    # save the plot
    plt.savefig(f"{FIGURE_PATH}/tvl_{chain}.pdf", dpi=300)
