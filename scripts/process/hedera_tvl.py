"""
Script to process the hedera TVL data
"""

import json
import pandas as pd

from environ.constants import DATA_PATH, END_OF_SAMPLE_PERIOD, PROCESSED_DATA_PATH

# Load the double counting data
df_dc = pd.read_csv(f"{PROCESSED_DATA_PATH}/hedera/double_counting.csv")
df_dc = df_dc[["date", "total"]].rename(columns={"total": "dc"})
df_dc["date"] = pd.to_datetime(df_dc["date"])

ptc_list = [
    "saucerswap",
    "stader",
    "davincigraph",
    "heliswap",
    "pangolin",
    "tangent",
    "bubbleswap-v1",
    "bubbleswap-v2",
]
df_hedera = []

for ptc in ptc_list:
    with open(
        f"{DATA_PATH}/defillama/tvl/{ptc}.json",
        "r",
        encoding="utf-8",
    ) as f:
        tvl_data = json.load(f)
        df_ptc = pd.concat(
            [pd.json_normalize(_) for _ in tvl_data["chainTvls"]["Hedera"]["tvl"]]
        )
        df_ptc["protocol"] = ptc
        df_ptc["date"] = pd.to_datetime(df_ptc["date"], unit="s")
        df_hedera.append(df_ptc)

df_hedera = pd.concat(df_hedera)
df_hedera = df_hedera.loc[df_hedera["date"] <= END_OF_SAMPLE_PERIOD]
df_tvr = (
    df_hedera.loc[df_hedera["protocol"] != "davincigraph"]
    .groupby(["date"])["totalLiquidityUSD"]
    .sum()
    .reset_index()
    .rename(columns={"totalLiquidityUSD": "tvl_llama"})
)
df_tvl = (df_hedera.groupby(["date"])["totalLiquidityUSD"].sum().reset_index()).rename(
    columns={"totalLiquidityUSD": "tvl"}
)

df_hedera = df_tvl.merge(df_tvr, on="date")
df_hedera = df_hedera.merge(df_dc, on="date")

df_hedera["tvr"] = df_hedera["tvl"] - df_hedera["dc"]
df_hedera = df_hedera.drop(columns=["dc"])
