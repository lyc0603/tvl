"""
Script to process individual tvl data
"""

import pandas as pd

from environ.constants import DATA_PATH

# LIDO ETH
lido_eth = pd.read_csv(DATA_PATH / "ind_tvl" / "lido.csv")
lido_eth["date"] = pd.to_datetime(lido_eth["date"])
lido_eth.set_index("date", inplace=True)

lido_eth["Receivables"] = lido_eth["tvl"]
lido_eth["Payables"] = 0
lido_eth.rename(columns={"tvl": "TVL"}, inplace=True)

# AAVE
aave = pd.read_csv(DATA_PATH / "ind_tvl" / "aave.csv")
aave["date"] = pd.to_datetime(aave["date"])
aave.set_index("date", inplace=True)
