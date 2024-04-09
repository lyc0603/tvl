"""
Script to process the ultron TVL data
"""

from scripts.process.ultron_tvl import df_ultron
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from environ.constants import FIGURE_PATH

fig, ax1 = plt.subplots(
    figsize=(5, 2),
)

PLOT_INFO_DICT = {
    "tvl": {"label": "$TVL^{Adj}_{t}$", "color": "blue"},
    "tvr": {"label": "$TVL_t$ or $TVR_t$", "color": "red"},
}

EVENT_INFO_DICT = {
    "ftx_collapse": {"label": "FTX Collapse", "ls": "dotted"},
}


p1 = ax1.plot(
    df_ultron["date"],
    df_ultron["tvl"],
    label=PLOT_INFO_DICT["tvl"]["label"],
    color=PLOT_INFO_DICT["tvl"]["color"],
    linewidth=1,
)
ax1.set_ylabel(PLOT_INFO_DICT["tvl"]["label"] + ", Dollar Amount", fontsize=6)
ax1.tick_params(axis="y", labelcolor=PLOT_INFO_DICT["tvl"]["color"])


ax2 = ax1.twinx()
p2 = ax2.plot(
    df_ultron["date"],
    df_ultron["tvr"],
    label=PLOT_INFO_DICT["tvr"]["label"],
    color=PLOT_INFO_DICT["tvr"]["color"],
    linewidth=1,
)
ax2.set_ylabel(PLOT_INFO_DICT["tvr"]["label"] + ", Dollar Amount", fontsize=6)
ax2.tick_params(axis="y", labelcolor=PLOT_INFO_DICT["tvr"]["color"])

# show the legend on the upper left corner
plt.legend(handles=p1 + p2, loc="upper right", fontsize=6, frameon=False)

# add the grid and increase the opacity and increase the intensity
ax1.grid(alpha=0.3)

# # set the unit of the x axis
# plt.gca().xaxis.set_major_formatter(
#     mdates.DateFormatter("%Y-%m"),
# )
plt.gca().xaxis.set_major_locator(
    mdates.MonthLocator(interval=1),
)


# Define a function to format y-axis tick labels
def millions_formatter(x, pos):
    return "{:.0f}M".format(x / 1e6)


# Set the formatter for both y-axes
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(millions_formatter))
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(millions_formatter))

# set the fontsize of the x and y axis
ax1.tick_params(axis="x", labelsize=6)
ax1.tick_params(axis="y", labelsize=6)
ax2.tick_params(axis="y", labelsize=6)

# rotate the xticks
fig.autofmt_xdate(rotation=90)


# tight layout
plt.tight_layout()

# save the plot
plt.savefig(f"{FIGURE_PATH}/tvl_ultron.pdf", dpi=300)
