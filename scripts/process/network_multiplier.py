"""
Script to calculate the multiplier
"""

import pandas as pd
from environ.constants import (
    PROCESSED_DATA_PATH,
    SAMPLE_DATA_DICT,
    CLASS_DEFILLAMA_MAPPING,
)
from scripts.rep_ptc import ptc_list

multiplier_dict = {}

for event, date in SAMPLE_DATA_DICT.items():
    multiplier_dict[event] = {}
    for ptc in ptc_list:

        ptc_name = ptc.__class__.__name__

        df_tvl = pd.read_csv(PROCESSED_DATA_PATH / "defillama_tvl_all_Ethereum.csv")
        df_tvr = pd.read_csv(PROCESSED_DATA_PATH / "defillama_tvr_all_Ethereum.csv")

        df_tvl["date"] = pd.to_datetime(df_tvl["date"])
        df_tvr["date"] = pd.to_datetime(df_tvr["date"])

        df_tvl = df_tvl.loc[df_tvl["protocol"] == CLASS_DEFILLAMA_MAPPING[ptc_name][0]]
        df_tvr = df_tvr.loc[df_tvr["protocol"] == CLASS_DEFILLAMA_MAPPING[ptc_name][0]]

        # Resample and interpolate missing values
        df_tvl = df_tvl.set_index("date").resample("D").interpolate().reset_index()
        df_tvr = df_tvr.set_index("date").resample("D").interpolate().reset_index()

        try:
            multiplier = (
                df_tvl.loc[
                    (df_tvl["date"] == date),
                    "totalLiquidityUSD",
                ].values[0]
                / df_tvr.loc[
                    (df_tvr["date"] == date),
                    "tvr",
                ].values[0]
            )
        except:  # pylint: disable=bare-except
            multiplier = (
                df_tvl.loc[
                    (df_tvl["date"] == date),
                    "totalLiquidityUSD",
                ].values[0]
                / df_tvr["tvr"].values[0]
            )

        multiplier_dict[event][ptc_name] = multiplier

multiplier_dict["ftx_collapse"]["Convex"] = 0.7826783366793301
