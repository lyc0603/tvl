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
    # "current_date": "2023-07-01",
}

# special address
ETH_ADDRESS = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
ETH_ADDRESS_LOWER = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

# common addresses
WETH_ADDRESS = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
DAI_ADDRESS = "0x6B175474E89094C44Da98b954EedeAC495271d0F"

# class-DeFillama mapping
CLASS_DEFILLAMA_MAPPING = {
    "Lido": ["lido"],
    "AaveV2": ["aave-v2"],
    "MakerDAO": ["makerdao", "maker-rwa"],
    "UniswapV2": ["uniswap-v2"],
    "Curve": ["curve-dex"],
    "Convex": ["convex-finance"],
}

# ETH price
ETH_PRICE_DICT = {
    "max_tvl": 4075.03,
    "luna_collapse": 2249.89,
    "ftx_collapse": 1334.29,
    "current_date": 1934.05,
}
