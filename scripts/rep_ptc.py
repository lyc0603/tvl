"""
Scripts for the representative protocols
"""

from environ.fetch.aave import AaveV2
from environ.fetch.convex import Convex
from environ.fetch.curve import Curve
from environ.fetch.lido import Lido
from environ.fetch.makerdao import MakerDAO
from environ.fetch.uniswap import UniswapV2
from environ.fetch.w3 import w3

ptc_list = [
    # AaveV2(w3),
    Curve(w3),
    # Lido(w3),
    # MakerDAO(w3),
    # UniswapV2(w3),
    # Convex(w3),
]

event_dict = {
    "max_tvl": {
        "date": "2021-12-26",
        "ptc": [
            AaveV2(w3),
            Lido(w3),
            MakerDAO(w3),
            UniswapV2(w3),
            Convex(w3),
        ],
    },
    "luna_collapse": {"date": "2022-05-09", "ptc": ptc_list},
    "ftx_collapse": {"date": "2022-11-08", "ptc": ptc_list},
    "current_date": {"date": "2023-07-01", "ptc": ptc_list},
}
