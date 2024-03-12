"""
Script to visualize the individual tvl data
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib import ticker

from environ.constants import FIGURE_PATH
from scripts.process.ind_tvl import aave, lido_eth

for df, name in [(lido_eth, "lido"), (aave, "aave")]:
    # plot the area chart
    plt.figure(figsize=(5, 4))
    plt.fill_between(
        df.index,
        df["Receivables"],
        color="g",
        alpha=0.6,
        label="Total Receivables",
    )

    plt.fill_between(
        df.index,
        -df["Payables"],
        color="r",
        alpha=0.6,
        label="Total Payables",
    )

    # plot the line chart
    df["TVL"].plot(
        color="#1f77b4",
        linestyle="-",
        linewidth=2,
        label="Protocol TVL",
    )

    # remove "token" from the legend
    plt.legend(loc="upper left", ncol=2, title="", fontsize=10)

    # x axis in the format of %Y-%m-%d
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

    # control the frequency of the x axius
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))

    # set the unit of the y axis
    plt.gca().yaxis.get_major_formatter().set_useOffset(False)
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:.0f}B".format(x / 1e9))
    )
    # plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(base=1e9))

    # add grid
    plt.grid(alpha=0.3)

    # limit setting
    plt.xlim(df.index.min(), df.index.max())
    plt.ylim(-df["Receivables"].max() * 0.5, df["Receivables"].max() * 1.1)

    # add x , y label
    plt.xlabel("")
    plt.ylabel("Dollar Amount", fontsize=12)

    # rotate the xticks
    plt.xticks(rotation=90)

    # xy tick size
    plt.tick_params(axis="both", which="major", labelsize=10)

    # tight layout
    plt.tight_layout()

    # save the plot
    plt.savefig(FIGURE_PATH / f"ind_{name}.pdf", dpi=300)

    plt.show()
