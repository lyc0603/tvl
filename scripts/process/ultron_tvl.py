"""
Script to process the ultron TVL data
"""

import json
import pandas as pd

from environ.constants import DATA_PATH, END_OF_SAMPLE_PERIOD

ptc_list = ["ultron-staking-hub-nft", "ultronswap", "iziswap"]
df_ultron = []

for ptc in ptc_list:
    with open(
        f"{DATA_PATH}/defillama/tvl/{ptc}.json",
        "r",
        encoding="utf-8",
    ) as f:
        tvl_data = json.load(f)
        df_ptc = (
            pd.concat(
                [pd.json_normalize(_) for _ in tvl_data["chainTvls"]["Ultron"]["tvl"]]
            )
            if ptc != "ultron-staking-hub-nft"
            else pd.concat(
                [
                    pd.json_normalize(_)
                    for _ in tvl_data["chainTvls"]["Ultron-staking"]["tvl"]
                ]
            )
        )
        df_ptc["protocol"] = ptc
        df_ptc["date"] = pd.to_datetime(df_ptc["date"], unit="s")
        if ptc == "ultron-staking-hub-nft":
            df_ptc.loc[df_ptc["date"] == "2023-09-15", "totalLiquidityUSD"] = (
                df_ptc.loc[df_ptc["date"] == "2023-09-14", "totalLiquidityUSD"].values[
                    0
                ]
            )
        df_ultron.append(df_ptc)

df_ultron = pd.concat(df_ultron)
df_ultron = df_ultron.loc[df_ultron["date"] <= END_OF_SAMPLE_PERIOD]
df_tvr = (
    df_ultron.groupby(["date"])["totalLiquidityUSD"]
    .sum()
    .reset_index()
    .rename(columns={"totalLiquidityUSD": "tvr"})
)
df_tvl = (
    df_ultron.loc[df_ultron["protocol"] != "ultron-staking-hub-nft"]
    .groupby(["date"])["totalLiquidityUSD"]
    .sum()
    .reset_index()
).rename(columns={"totalLiquidityUSD": "tvl"})
df_ultron = df_tvl.merge(df_tvr, on="date")
