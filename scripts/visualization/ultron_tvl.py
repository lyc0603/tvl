"""
Script to process the ultron TVL data
"""

from scripts.process.ultron_tvl import df_ultron
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from environ.constants import FIGURE_PATH

fig, axes = plt.subplots(
    figsize=(5, 2),
)

PLOT_INFO_DICT = {
    "tvl": {"label": "$TVL^{Adj}_{t}$", "color": "blue"},
    "tvr": {"label": "$TVL_t$ / $TVR_t$", "color": "red"},
}

EVENT_INFO_DICT = {
    "ftx_collapse": {"label": "FTX Collapse", "ls": "dotted"},
}


# plot the tvl with DC, tvl, and tvr
for col, info in PLOT_INFO_DICT.items():
    axes.plot(
        df_ultron["date"],
        df_ultron[col],
        label=info["label"],
        color=info["color"],
        linewidth=1,
    )

# show the legend on the upper left corner
plt.legend(loc="upper left", fontsize=6, frameon=False)

# add the grid and increase the opacity and increase the intensity
plt.grid(alpha=0.3)

# set the unit of the x axis
plt.gca().xaxis.set_major_formatter(
    mdates.DateFormatter("%Y-%m"),
)
plt.gca().xaxis.set_major_locator(
    mdates.MonthLocator(interval=1),
)

# label the y axis
plt.ylabel("Dollar Amount", fontsize=6)

# set the unit of the y axis
plt.gca().yaxis.get_major_formatter().set_useOffset(False)
plt.gca().yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "{:.0f}M".format(x / 1e6))
)
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(base=200e6))

plt.xticks(fontsize=6)
plt.yticks(fontsize=6)
# plt.legend(prop={"size": 6})

# rotate the xticks
plt.xticks(rotation=90)

# tight layout
plt.tight_layout()

# save the plot
plt.savefig(f"{FIGURE_PATH}/tvl_ultron.pdf", dpi=300)
