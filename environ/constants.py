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

PLAIN_TOKEN_LIST_PLF = [
    # TUSD
    "0x0000000000085d4780B73119b644AE5ecd22b376",
    # RAI
    "0x03ab458634910AaD20eF5f1C8ee96F1D6ac54919",
    # GUSD
    "0x056Fd409E1d7A124BD7017459dFEa2F387b6d5Cd",
    # BAT
    "0x0D8775F648430679A709E98d2b0Cb6250d2887EF",
    # MANA
    "0x0F5D2fB29fb7d3CFeE444a200298f468908cC942",
    # YFI
    "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e",
    # DPI
    "0x1494CA1F11D487c2bBe4543E90080AeBa4BA3C2b",
    # UNI
    "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
    # WBTC
    "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
    # Republic
    "0x408e41876cCCDC0F92210600ef50372656052a38",
    # BUSD
    "0x4Fabb145d64652a948d72533023f6E7A623C7C53",
    # Chainlink
    "0x514910771AF9Ca656af840dff83E8264EcF986CA",
    # MATIC
    "0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",
    # AAVE
    "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9",
    # FRAX
    "0x853d955aCEf822Db058eb8505911ED77F175b99e",
    # USDP
    "0x8E870D67F660D95d5be530380D0eC0bd388289E1",
    # FEI
    "0x956F47F50A910163D8BF957Cf5846D573E7f87CA",
    # MAKRE
    "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2",
    # USDC
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    # LRC
    "0xBBbbCA6A901c926F240b89EacB641d8Aec7AEafD",
    # SNX
    "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F",
    # WETH
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    # AMPL
    "0xD46bA6D942050d489DBd938a2C909A5d5039A161",
    # CRV
    "0xD533a949740bb3306d119CC777fa900bA034cd52",
    # ZRX
    "0xE41d2489571d322189246DaFA5ebDe1F4699F498",
    # ENJ
    "0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c",
    # BAL
    "0xba100000625a3754423978a60c9317c58a424e3D",
    # COMP
    "0xc00e94Cb662C3520282E6f5717214004A7f26888",
    # USDT
    "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    # KNC
    "0xdd974D5C2e2928deA5F71b9825b8b646686BD200",
]

params_dict = {
    "$\\delta_{MKR}$": {
        "$\\delta_{MKR}$": [1, 0.75, 0.5],
        "$\\delta_{AAVE}$": [0.5, 0.5, 0.5],
        "$\\psi_{1,AAVE}$": [0, 0, 0],
    },
    "$\\delta_{AAVE}$": {
        "$\\delta_{MKR}$": [1, 1, 1],
        "$\\delta_{AAVE}$": [0.5, 0.75, 1],
        "$\\psi_{1,AAVE}$": [0, 0, 0],
    },
    "$\\psi_{1,AAVE}$": {
        "$\\delta_{MKR}$": [1, 1, 1],
        "$\\delta_{AAVE}$": [0.5, 0.5, 0.5],
        "$\\psi_{1,AAVE}$": [0, 0.5, 0.95],
    },
}
