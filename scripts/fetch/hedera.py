"""
Script to fetch data from Hedera Hashgraph API
"""

import json

import pandas as pd
import requests
from tqdm import tqdm

from environ.constants import PROCESSED_DATA_PATH, SAMPLE_DATA_DICT
from environ.fetch.hedera import fetch_url, post_url

hedera_dict = {_: [] for _ in SAMPLE_DATA_DICT.keys()}

# SaucerSwap
SAUCERSWAP_API_ROOT = "https://api.saucerswap.finance/"
SAUCERSWAP_TOKEN_FULL = SAUCERSWAP_API_ROOT + "tokens/full"
SAUCERSWAP_PRICES = SAUCERSWAP_API_ROOT + "tokens/prices"
df_saucerswap_tokens = pd.DataFrame(fetch_url(SAUCERSWAP_TOKEN_FULL))
hbarx_id = df_saucerswap_tokens[df_saucerswap_tokens["symbol"] == "HBARX"]["id"].values[
    0
]

df_hbarx = pd.DataFrame(
    fetch_url(
        SAUCERSWAP_PRICES + f"/{hbarx_id}",
        {
            "from": "1640995200",
            "to": "1712246616",
            "interval": "DAY",
        },
    )
)
df_hbarx["timestampSeconds"] = pd.to_datetime(df_hbarx["timestampSeconds"], unit="s")

for event, date in SAMPLE_DATA_DICT.items():
    try:
        hedera_dict[event].append(
            {
                "source": "Stader",
                "target": "SaucerSwap",
                "value": float(
                    df_hbarx.loc[
                        df_hbarx["timestampSeconds"] == date, "liquidityUsd"
                    ].values[0]
                ),
            }
        )
    except:  # pylint: disable=bare-except
        pass

# # DaVinciGraph
# DAVINCIGRAPH_BASE = "https://davincigraph.network"
# DAVINCIGRAPH_LOG = DAVINCIGRAPH_BASE + "/api/v1/logs"
# DAVINCIGRAPH_TOKEN = DAVINCIGRAPH_BASE + "/api/v1/logs/tokens/"
# fetch_url(DAVINCIGRAPH_LOG, {"page": 19, "limit": 24})
# df_dvc = pd.concat(
#     [
#         pd.json_normalize(
#             fetch_url(DAVINCIGRAPH_LOG, {"page": page, "limit": 24})["logs"]
#         )
#         for page in tqdm(range(1, 20, 1))
#     ]
# )

# for event, date in SAMPLE_DATA_DICT.items():
#     try:
#         hedera_dict[event].append(
#             {
#                 "source": "Stader",
#                 "target": "SaucerSwap",
#                 "amount": df_dvc.loc[
#                     df_dvc["timestamp"] == date, "totalLiquidityUsd"
#                 ].values[0],
#             }
#         )
#     except:
#         pass

# HeliSwap
QUERY_URL = "https://heliswap-prod-362307.oa.r.appspot.com/query"
HELI_POOL_QUERY = {
    "operationName": "getWhitelistedPools",
    "variables": {
        "tokens": [
            "0x00000000000000000000000000000000002cc823",
            "0x000000000000000000000000000000000008437c",
            "0x0000000000000000000000000000000000101Ae3",
            "0x000000000000000000000000000000000006f89a",
            "0x0000000000000000000000000000000000101aF0",
            "0x0000000000000000000000000000000000101aFb",
            "0x0000000000000000000000000000000000107d76",
            "0x0000000000000000000000000000000000101Af5",
            "0x0000000000000000000000000000000000083E9E",
            "0x00000000000000000000000000000000000cbA44",
            "0x00000000000000000000000000000000000Ec585",
            "0x00000000000000000000000000000000000D1ea6",
            "0x0000000000000000000000000000000000098779",
            "0x00000000000000000000000000000000000E22B1",
            "0x000000000000000000000000000000000001f385",
            "0x00000000000000000000000000000000001139fd",
            "0x00000000000000000000000000000000001176B5",
            "0x0000000000000000000000000000000000107980",
            "0x0000000000000000000000000000000000163748",
            "0x000000000000000000000000000000000011219e",
            "0x000000000000000000000000000000000012E088",
            "0x00000000000000000000000000000000001d90C9",
            "0x00000000000000000000000000000000000ff4DA",
            "0x000000000000000000000000000000000022D6de",
            "0x00000000000000000000000000000000002D4720",
            "0x00000000000000000000000000000000002A30A8",
            "0x000000000000000000000000000000000021226e",
            "0x0000000000000000000000000000000000455D51",
            "0x0000000000000000000000000000000000422717",
        ]
    },
    "query": "query getWhitelistedPools($tokens: [String]!) {\n  poolsConsistingOf(tokens: $tokens) {\n    id\n    pairName\n    pairSymbol\n    pairAddress\n    pairSupply\n    token0\n    token0Name\n    token0Amount\n    token0Symbol\n    token0Decimals\n    token1\n    token1Name\n    token1Symbol\n    token1Amount\n    token1Decimals\n    volume24h\n    volume7d\n    hasCampaign\n    volume24hUsd\n    volume7dUsd\n    tvl\n    __typename\n  }\n}",
}

json_heli = post_url(QUERY_URL, HELI_POOL_QUERY)
df_heli_pool = pd.concat(
    [pd.json_normalize(_) for _ in json_heli["data"]["poolsConsistingOf"]]
)
heli_hbarx = df_heli_pool.loc[
    (df_heli_pool["token0Symbol"] == "HBARX")
    | ((df_heli_pool["token1Symbol"] == "HBARX")),
    "pairAddress",
].values.tolist()

pool_tvl = []
for pool_address in tqdm(heli_hbarx):
    HELI_TVL_QUERY = {
        "operationName": "getPoolByAddress",
        "variables": {
            "poolAddress": pool_address,
            "tokens": [
                "0x00000000000000000000000000000000002cc823",
                "0x000000000000000000000000000000000008437c",
                "0x0000000000000000000000000000000000101Ae3",
                "0x000000000000000000000000000000000006f89a",
                "0x0000000000000000000000000000000000101aF0",
                "0x0000000000000000000000000000000000101aFb",
                "0x0000000000000000000000000000000000107d76",
                "0x0000000000000000000000000000000000101Af5",
                "0x0000000000000000000000000000000000083E9E",
                "0x00000000000000000000000000000000000cbA44",
                "0x00000000000000000000000000000000000Ec585",
                "0x00000000000000000000000000000000000D1ea6",
                "0x0000000000000000000000000000000000098779",
                "0x00000000000000000000000000000000000E22B1",
                "0x000000000000000000000000000000000001f385",
                "0x00000000000000000000000000000000001139fd",
                "0x00000000000000000000000000000000001176B5",
                "0x0000000000000000000000000000000000107980",
                "0x0000000000000000000000000000000000163748",
                "0x000000000000000000000000000000000011219e",
                "0x000000000000000000000000000000000012E088",
                "0x00000000000000000000000000000000001d90C9",
                "0x00000000000000000000000000000000000ff4DA",
                "0x000000000000000000000000000000000022D6de",
                "0x00000000000000000000000000000000002D4720",
                "0x00000000000000000000000000000000002A30A8",
                "0x000000000000000000000000000000000021226e",
                "0x0000000000000000000000000000000000455D51",
                "0x0000000000000000000000000000000000422717",
            ],
        },
        "query": "query getPoolByAddress($poolAddress: String!, $tokens: [String]!) {\n  getPoolByAddress(poolAddress: $poolAddress, tokens: $tokens) {\n    id\n    pairName\n    pairSymbol\n    pairAddress\n    pairSupply\n    token0\n    token0Name\n    token0Amount\n    token0Symbol\n    token0Decimals\n    token1\n    token1Name\n    token1Symbol\n    token1Amount\n    token1Decimals\n    volume24h\n    volume7d\n    hasCampaign\n    volume24hUsd\n    volume7dUsd\n    tvl\n    historicalData {\n      time\n      tvl\n      volume\n      __typename\n    }\n    fees {\n      amount\n      __typename\n    }\n    diff {\n      tvl\n      volume\n      __typename\n    }\n    __typename\n  }\n}",
    }

    json_heli_tvl = post_url(QUERY_URL, HELI_TVL_QUERY)["data"]["getPoolByAddress"][
        "historicalData"
    ]
    df_heli_tvl = pd.json_normalize(json_heli_tvl)
    df_heli_tvl["poolAddress"] = pool_address
    pool_tvl.append(df_heli_tvl)

df_heli_tvl = pd.concat(pool_tvl)
df_heli_tvl["time"] = pd.to_datetime(df_heli_tvl["time"], unit="s")
df_heli_tvl["tvl"] = df_heli_tvl["tvl"].astype(float)
df_heli_hbarx = df_heli_tvl.groupby("time")["tvl"].sum().reset_index()
df_heli_hbarx["tvl"] = df_heli_hbarx["tvl"] / 2

for event, date in SAMPLE_DATA_DICT.items():
    try:
        hedera_dict[event].append(
            {
                "source": "Stader",
                "target": "HeliSwap",
                "value": float(
                    df_heli_hbarx.loc[df_heli_hbarx["time"] == date, "tvl"].values[0]
                ),
            }
        )
    except:  # pylint: disable=bare-except
        pass

# Pangolin
PANGOLIN_QUERY = "https://graph-hedera-pangolin.canary.exchange/subgraphs/name/pangolin"
PANGOLIN_TOKEN_QUERY = {
    "query": 'query MyQuery {\n  tokenDayDatas(\n    first: 1000\n    orderBy: date\n    orderDirection: asc\n    where: {token_: {id: "0x00000000000000000000000000000000000cba44"}}\n  ) {\n    totalLiquidityUSD\n    id\n    token {\n      id\n      name\n      symbol\n    }\n    date\n  }\n}',
    "operationName": "MyQuery",
    "extensions": {},
}
json_pangolin_hbarx = post_url(PANGOLIN_QUERY, PANGOLIN_TOKEN_QUERY)
df_pangolin_hbarx = pd.concat(
    [pd.json_normalize(_) for _ in json_pangolin_hbarx["data"]["tokenDayDatas"]]
)
df_pangolin_hbarx["date"] = pd.to_datetime(df_pangolin_hbarx["date"], unit="s")

for event, date in SAMPLE_DATA_DICT.items():
    try:
        hedera_dict[event].append(
            {
                "source": "Stader",
                "target": "Pangolin",
                "value": float(
                    df_pangolin_hbarx.loc[
                        df_pangolin_hbarx["date"] == date, "totalLiquidityUSD"
                    ].values[0]
                ),
            }
        )
    except:  # pylint: disable=bare-except
        pass

for event, date in SAMPLE_DATA_DICT.items():
    with open(
        f"{PROCESSED_DATA_PATH}/network/hedera_node_edge_amount_{event}.json",
        "w",
        encoding="utf-8",
    ) as f:
        for line in hedera_dict[event]:
            f.write(json.dumps(line) + "\n")
