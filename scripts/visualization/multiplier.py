"""
Script to plot the comparison of money supply between the trafi and defi
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import json

from scripts.process.money_multiplier import money_multiplier_dict
from scripts.process.leverage_ratio import leverage_ratio_dict
from environ.constants import FIGURE_PATH, SAMPLE_DATA_DICT, DATA_PATH


def parse_token_prc(cg_id: str) -> pd.DataFrame:
    """
    Function to parse the token price json
    """

    with open(DATA_PATH / "token_price" / f"{cg_id}.json", "r", encoding="utf-8") as f:
        token_price = json.load(f)

    price = [_[1] for _ in token_price["prices"]]
    timestamp = [_[0] for _ in token_price["prices"]]

    df = pd.DataFrame({"price": price, "timestamp": timestamp})
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.drop(columns=["timestamp"], inplace=True)
    df["eth_price"] = df["price"].shift(-1)

    return df


eth_price = parse_token_prc("ethereum")

EVENT_INFO_DICT = {
    "max_tvl": {"label": "Max TVL", "ls": "dashdot"},
    "luna_collapse": {"label": "Luna Collapse", "ls": "dashed"},
    "ftx_collapse": {"label": "FTX Collapse", "ls": "dotted"},
}


df_money_supplier = pd.DataFrame(money_multiplier_dict)
df_money_supplier.rename(
    columns={"value": "money_multiplier"},
    inplace=True,
)
df_leverage_ratio = pd.DataFrame(leverage_ratio_dict)
df_leverage_ratio.rename(
    columns={"value": "leverage_ratio"},
    inplace=True,
)

df_leverage_ratio.loc[df_leverage_ratio["date"] == "2021-04-05", "leverage_ratio"] = (
    df_leverage_ratio.loc[df_leverage_ratio["date"] == "2021-04-04", "leverage_ratio"]
)

df_agg = df_leverage_ratio.merge(
    df_money_supplier,
    how="left",
    on="date",
)
df_agg = df_agg.merge(
    eth_price,
    how="left",
    on="date",
)

PLOT_DICT = {
    # "money_multiplier": {
    #     "label": "TraFi Money Multiplier",
    #     "color": "blue",
    #     "marker": "o",
    #     "markersize": 2,
    #     "linewidth": 1,
    # },
    "eth_price": {
        "label": "Ether Price",
        "color": "blue",
        "marker": "o",
        "markersize": 2,
        "linewidth": 1.5,
    },
    "leverage_ratio": {
        "label": "DeFi Money Multiplier",
        "color": "red",
        "marker": "o",
        "markersize": 2,
        "linewidth": 1.5,
    },
}

# plot the leverage ratio and eth price in two different y axis
fig, ax1 = plt.subplots(figsize=(5.5, 2))
ax1.plot(
    df_agg["date"],
    df_agg["leverage_ratio"],
    # label=PLOT_DICT["leverage_ratio"]["label"],
    color=PLOT_DICT["leverage_ratio"]["color"],
    # marker=PLOT_DICT["leverage_ratio"]["marker"],
    # markersize=PLOT_DICT["leverage_ratio"]["markersize"],
    linewidth=PLOT_DICT["leverage_ratio"]["linewidth"],
)

ax1.set_ylabel(
    "DeFi Money Multiplier", color=PLOT_DICT["leverage_ratio"]["color"], fontsize=6
)
ax1.tick_params(axis="y", labelcolor=PLOT_DICT["leverage_ratio"]["color"])

plt.xticks(rotation=90)
plt.gca().xaxis.set_major_formatter(
    mdates.DateFormatter("%Y-%m"),
)
plt.gca().xaxis.set_major_locator(
    mdates.MonthLocator(interval=3),
)

ax2 = ax1.twinx()

ax2.plot(
    df_agg["date"],
    df_agg["eth_price"],
    # label=PLOT_DICT["eth_price"]["label"],
    color=PLOT_DICT["eth_price"]["color"],
    # marker=PLOT_DICT["eth_price"]["marker"],
    # markersize=PLOT_DICT["eth_price"]["markersize"],
    linewidth=PLOT_DICT["eth_price"]["linewidth"],
)

ax2.set_ylabel("Ether Price", color=PLOT_DICT["eth_price"]["color"])
ax2.tick_params(axis="y", labelcolor=PLOT_DICT["eth_price"]["color"])

# for var, var_plot_info in PLOT_DICT.items():
#     plt.plot(
#         df_agg["date"],
#         df_agg[var],
#         label=var_plot_info["label"],
#         color=var_plot_info["color"],
#         marker=var_plot_info["marker"],
#         markersize=var_plot_info["markersize"],
#         linewidth=var_plot_info["linewidth"],
#     )

for event, date in SAMPLE_DATA_DICT.items():
    plt.axvline(
        pd.to_datetime(date),
        color="black",
        linewidth=1,
        # label=EVENT_INFO_DICT[event]["label"],
        ls=EVENT_INFO_DICT[event]["ls"],
    )
    plt.text(
        pd.to_datetime(date),
        0,
        EVENT_INFO_DICT[event]["label"],
        rotation=90,
        # backgroundcolor="white",
        fontsize=5,
        horizontalalignment="center",
        verticalalignment="bottom",
        # alpha=0.8,
        # backgroundcolor needs transparency
    )

# # show the legend on the upper right corner
# plt.legend(prop={"size": 6})

# add the grid and increase the opacity and increase the intensity
plt.grid(alpha=0.3)

# set the x limit to 2019-06-01
plt.xlim(
    [
        pd.to_datetime("2019-06-01"),
        df_leverage_ratio[df_leverage_ratio["leverage_ratio"].notnull()]["date"].max(),
    ]
)

# set the unit of the x axis
# plt.gca().xaxis.set_major_formatter(
#     mdates.DateFormatter("%Y-%m"),
# )
# plt.gca().xaxis.set_major_locator(
#     mdates.MonthLocator(interval=2),
# )

# # label the y axis
# plt.ylabel("Ratio")

# # rotate the xticks
# plt.xticks(rotation=45)

# tight layout
plt.tight_layout()

# save the figure
plt.savefig(f"{FIGURE_PATH}/money_supply_compare.pdf", dpi=300)

plt.show()
