"""
Script to process leverage ratio data
"""

from environ.process.preprocess_defillama_tvl import preprocess_ptc_tvl

df_agg = preprocess_ptc_tvl(
    chain="Total",
)

# # get the ym as integer YYYYMM
# df_agg["ym"] = df_agg["date"].apply(lambda x: x.year * 100 + x.month)

# # sort the dataframe by date
# df_agg = df_agg.sort_values(by="date", ascending=True)

# # keep the first date of each month
# df_agg = df_agg.drop_duplicates(subset=["ym"], keep="first")

# a dictionary to store the leverage ratio data
leverage_ratio_dict = {
    "date": [],
    "value": [],
}

# calculate the leverage ratio
leverage_ratio_dict["date"] = df_agg["date"].tolist()
leverage_ratio_dict["value"] = (df_agg["totalLiquidityUSD"] / df_agg["tvr"]).tolist()
