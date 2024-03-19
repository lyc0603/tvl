"""
Script to preprocess the total TVL from DeFiLlama
"""

from environ.constants import PROCESSED_DATA_PATH
from environ.process.preprocess_defillama_tvl import preprocess_total_tvl

# load the total tvl data
df_tvl_all = preprocess_total_tvl(
    df_path=f"{PROCESSED_DATA_PATH}/defillama/defillama_tvl_all.csv"
)


# load the total tvr data
df_tvr_all = preprocess_total_tvl(
    df_path=f"{PROCESSED_DATA_PATH}/defillama/defillama_tvr_all.csv"
)
