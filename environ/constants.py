"""This file contains the configuration settings for the market environment."""

from environ.settings import PROJECT_ROOT

# Paths
DATA_PATH = PROJECT_ROOT / "data"
FIGURE_PATH = PROJECT_ROOT / "figures"
PROCESSED_DATA_PATH = PROJECT_ROOT / "processed_data"

# sample date
SAMPLE_DATA_DICT = {
    "max_tvl": "2021-12-26",
    "luna_collapse": "2022-05-09",
    "ftx_collapse": "2022-11-08",
    "current_date": "2023-07-01",
}

# special address
ETH_ADDRESS = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"

# class-DeFillama mapping
CLASS_DEFILLAMA_MAPPING = {
    "Lido": ["lido"],
    "AaveV2": ["aave-v2"],
    "MakerDAO": ["makerdao", "maker-rwa"],
    "UniswapV2": ["uniswap-v2"],
    "Curve": ["curve-dex"],
    "Convex": ["convex-finance"],
}
