"""
Script to fetch the individual tvl data
"""

import json

import pandas as pd
from tqdm import tqdm

from environ.constants import DATA_PATH
from environ.fetch.aave import AaveV2
from environ.fetch.lido import Lido
from environ.fetch.w3 import w3, token_decimal
import matplotlib.pyplot as plt

lido = Lido(w3)
aave = AaveV2(w3)


def parse_token_prc(cg_id: str) -> pd.DataFrame:
    """
    Function to parse the token price json
    """

    with open(DATA_PATH / "token_price" / f"{cg_id}.json", "r", encoding="utf-8") as f:
        token_price = json.load(f)

    price = [_[1] for _ in token_price["prices"]]
    timestamp = [_[0] for _ in token_price["prices"]]

    df = pd.DataFrame({"price": price, "timestamp": timestamp})
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms").dt.strftime("%Y-%m-%d")

    df["price"] = df["price"].shift(-1)

    return df


# LIDO ETH
date_range = pd.read_csv(DATA_PATH / "date_to_block.csv")

lido_eth_date_range = date_range.loc[date_range["block"] >= 11473216, ["block", "date"]]

lido_eth = {"date": [], "lido": []}

for index, row in tqdm(lido_eth_date_range.iterrows(), total=len(lido_eth_date_range)):
    block = row["block"]
    date = row["date"]

    lido_eth["date"].append(date)
    lido_eth["lido"].append(lido.get_total_pooled_ether(block))

lido_eth = pd.DataFrame(lido_eth)

eth_price = parse_token_prc("ethereum")

lido_eth = lido_eth.merge(eth_price, left_on="date", right_on="timestamp")
lido_eth["tvl"] = lido_eth["lido"] * lido_eth["price"]
lido_eth["date"] = pd.to_datetime(lido_eth["date"])

# LIDO STETH
lido_matic_date_range = date_range.loc[
    date_range["block"] >= 14276886, ["block", "date"]
]

lido_matic = {"date": [], "matic": []}

for index, row in tqdm(
    lido_matic_date_range.iterrows(), total=len(lido_matic_date_range)
):
    block = row["block"]
    date = row["date"]

    lido_matic["date"].append(date)
    lido_matic["matic"].append(lido.get_total_pooled_matic(block))

lido_matic = pd.DataFrame(lido_matic)

matic_price = parse_token_prc("matic-network")

lido_matic = lido_matic.merge(matic_price, left_on="date", right_on="timestamp")
lido_matic["tvl"] = lido_matic["matic"] * lido_matic["price"]
lido_matic["date"] = pd.to_datetime(lido_matic["date"])

# add up the tvl
lido_tvl = {
    "date": [],
    "tvl": [],
}

for index, row in tqdm(lido_eth.iterrows(), total=len(lido_eth)):
    date = row["date"]
    lido_tvl["date"].append(date)
    if date in lido_matic["date"].values:
        lido_tvl["tvl"].append(
            row["tvl"] + lido_matic.loc[lido_matic["date"] == date, "tvl"].values[0]
        )
    else:
        lido_tvl["tvl"].append(row["tvl"])

lido_tvl = pd.DataFrame(lido_tvl)
lido_tvl.to_csv(DATA_PATH / "ind_tvl" / "lido.csv", index=False)

# AAVE collateral
aave_date_range = date_range.loc[date_range["block"] >= 11362589, ["block", "date"]]
aave_df = []

for index, row in tqdm(aave_date_range.iterrows(), total=len(aave_date_range)):
    block = row["block"]
    date = row["date"]
    reserve_dict = {
        "date": date,
        "block": block,
    }
    for reserve_addrress in aave.get_reserve_list(block):

        availableLiquidity, totalStableDebt, totalVariableDebt, *_ = (
            aave.get_reserve_data(reserve_addrress, block)
        )

        receivables = availableLiquidity + totalStableDebt + totalVariableDebt
        payables = totalStableDebt + totalVariableDebt

        reserve_dict[reserve_addrress + "_payable"] = payables
        reserve_dict[reserve_addrress + "_receivable"] = receivables

    aave_df.append(reserve_dict)

# save the json
with open(DATA_PATH / "ind_tvl" / "aave.json", "w", encoding="utf-8") as f:
    json.dump(aave_df, f)

# AAVE oracle

aave_price_list = []

for item in tqdm(aave_df):
    block = item["block"]
    date = item["date"]

    price_dict = {
        "date": date,
        "block": block,
    }

    reserve_list = list(
        set([_.split("_")[0] for _ in list(item.keys()) if _ not in ["date", "block"]])
    )
    aave_price = aave.get_asset_prices(reserve_list, block)

    for i, reserve in enumerate(reserve_list):
        price_dict[reserve] = aave_price[i]

    aave_price_list.append(price_dict)

aave_price_list_usd = []

# USD price
for item in tqdm(aave_price_list):
    date = item["date"]
    reserve_dict = {
        "date": date,
        "block": item["block"],
    }

    eth_price_date = eth_price.loc[eth_price["timestamp"] == date, "price"].values[0]
    reserve_list = [_ for _ in list(item.keys()) if _ not in ["date", "block"]]
    for reserve in reserve_list:
        reserve_dict[reserve] = item[reserve] * eth_price_date

    aave_price_list_usd.append(reserve_dict)

with open(DATA_PATH / "ind_tvl" / "aave.json", "r", encoding="utf-8") as f:
    aave_df = json.load(f)

# aave df
aave_df = pd.DataFrame(aave_df)
reserve_list = list(
    set([_.split("_")[0] for _ in list(item.keys()) if _ not in ["date", "block"]])
)
for reserve in reserve_list:
    aave_df[reserve + "_receivable"] = aave_df[reserve + "_receivable"] * 10 ** (
        -token_decimal(reserve, "latest")
    )
    aave_df[reserve + "_payable"] = aave_df[reserve + "_payable"] * 10 ** (
        -token_decimal(reserve, "latest")
    )


# merge price
for item in aave_price_list_usd:
    date = item["date"]
    for reserve in [_ for _ in list(item.keys()) if _ not in ["date", "block"]]:
        aave_df.loc[aave_df["date"] == date, reserve + "_receivable"] *= item[reserve]
        aave_df.loc[aave_df["date"] == date, reserve + "_payable"] *= item[reserve]

aave_df["Receivables"] = 0
aave_df["Payables"] = 0
aave_df.fillna(0, inplace=True)

# aggregate total receivables and payables
for reserve in reserve_list:
    aave_df["Receivables"] += aave_df[reserve + "_receivable"]
    aave_df["Payables"] += aave_df[reserve + "_payable"]


aave_df["TVL"] = aave_df["Receivables"] - aave_df["Payables"]

aave_df = aave_df[["date", "TVL", "Receivables", "Payables"]]
aave_df.to_csv(DATA_PATH / "ind_tvl" / "aave.csv", index=False)
