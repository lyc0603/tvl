"""
Liquidity Pools List
"""

import json

from environ.constants import DATA_PATH

with open(DATA_PATH / "lp" / "lp.json", "r", encoding="utf-8") as f:
    lp = json.load(f)
