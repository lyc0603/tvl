"""
Class to fetch the token price
"""

import json

import requests

from environ.constants import PROCESSED_DATA_PATH
from environ.fetch.w3 import total_supply_normalized
from environ.fetch.block import date_close_to_block

SPECIAL_TOKEN = {
    # yDAI
    "0xC2cB1040220768554cf699b0d863A3cd4324ce32": "0x6B175474E89094C44DA98B954EEDEAC495271D0F",
    "0x16de59092dAE5CcF4A1E6439D611fd0653f0Bd01": "0x6B175474E89094C44DA98B954EEDEAC495271D0F",
    # yUSDC
    "0x26EA744E5B887E5205727f55dFBE8685e3b21951": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "0xd6aD7a6750A7593E092a9B218d66C0A814a3436e": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    # yUSDT
    "0xE6354ed5bC4b393a5Aad09f21c46E101e692d447": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "0x83f798e925BcD4017Eb265844FDDAbb448f1707D": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    # yBUSD
    "0x04bC0Ab673d88aE9dbC9DA2380cB6B79C4BCa9aE": "0x4Fabb145d64652a948d72533023f6E7A623C7C53",
    # yTUSD
    "0x73a052500105205d34Daf004eAb301916DA8190f": "0x0000000000085d4780B73119b644AE5ecd22b376",
    # cyDAI
    "0x8e595470Ed749b85C6F7669de83EAe304C2ec68F": "0x6B175474E89094C44DA98B954EEDEAC495271D0F",
    # cyUSDC
    "0x76Eb2FE28b36B3ee97F3Adae0C69606eeDB2A37c": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    # cyUSDT
    "0x48759F220ED983dB51fA7A8C0D2AAb8f3ce4166a": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    # sLINK
    "0xbBC455cb4F1B9e4bFC4B73970d360c8f032EfEE6": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
    # ycDAI
    "0x99d1Fa417f94dcD62BfE781a1213c092a47041Bc": "0x6B175474E89094C44DA98B954EEDEAC495271D0F",
    # ycUSDC
    "0x9777d7E2b60bB01759D0E2f8be2095df444cb07E": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    # ycUSDT
    "0x1bE5d71F2dA660BFdee8012dDc58D024448A0A59": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    # USDM
    "0x31d4Eb09a216e181eC8a43ce79226A487D6F0BA9": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    # alETH
    "0x0100546F2cD4C9D97f798fFC9755E47865FF7Ee6": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    # wibBTC
    "0x8751D4196027d4e6DA63716fA7786B5174F04C15": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
}

SPECIAL_TOKEN_WITH_PRICE = {
    # cDAI
    "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643": 0.02,
    # cUSDC
    "0x39AA39c021dfbaE8faC545936693aC917d5E7563": 0.02,
    # ibKRW
    "0x95dFDC8161832e4fF7816aC4B6367CE201538253": 0.00084887,
    # sKRW
    "0x269895a3dF4D73b077Fc823dD6dA1B95f72Aaf9B": 0.00084887,
    # ibJPY
    "0x5555f75e3d5278082200Fb451D1b6bA946D8e13b": 0.00874125,
    # sJPY
    "0xF6b1C627e95BFc3c1b4c9B825a032Ff0fBf3e07d": 0.00874125,
    # ibAUD
    "0xFAFdF0C4c1CB09d430Bf88c75D88BB46DAe09967": 0.722209,
    # sAUD
    "0xF48e200EAF9906362BB1442fca31e0835773b8B4": 0.722209,
    # ibGBP
    "0x69681f8fde45345C3870BCD5eaf4A05a60E7D227": 1.33908,
    # sGBP
    "0x97fe22E7341a0Cd8Db6F6C021A24Dc8f4DAD855F": 1.33908,
    # ibCHF
    "0x1CC481cE2BD2EC7Bf67d1Be64d4878b16078F309": 1.08692,
    # sCHF
    "0x0F83287FF768D1c1e17a42F44d644D7F22e8ee1d": 1.08692,
    # EURN
    "0x9fcf418B971134625CdF38448B949C8640971671": 1.13268,
    # PWRD
    "0xF0a93d4994B3d98Fb5e3A2F90dBc2d69073Cb86b": 1,
    # PARETO
    "0xea5f88E54d982Cbb0c441cde4E79bC305e5b43Bc": 0.005721,
    # Curve ironbank
    "0x5282a4eF67D9C33135340fB3289cc1711c13638C": 1,
}


class DeFiLlama:
    """
    Class to fetch the token price
    """

    def __init__(self) -> None:
        pass

    def get_price(self, token_address: str, timestamp: int) -> float:
        """
        Function to get the price of the token
        """
        if token_address in SPECIAL_TOKEN:
            token_address = SPECIAL_TOKEN[token_address]
        elif token_address in SPECIAL_TOKEN_WITH_PRICE:
            return SPECIAL_TOKEN_WITH_PRICE[token_address]
        response = requests.get(
            f"https://coins.llama.fi/prices/historical/{timestamp}"
            + f"/ethereum:{token_address}?searchWidth=4h",
            timeout=60,
        )
        return response.json()["coins"][f"ethereum:{token_address}"]["price"]

    def get_price_with_derivative(
        self, token_address: str, event: str, timestamp: int, block: int
    ) -> float | None:
        """
        Function to get the price of the derivative
        """
        # print(f"calculate price for {token_address}")
        try:
            return self.get_price(token_address, timestamp)
        except:  # pylint: disable=bare-except
            with open(
                f"{PROCESSED_DATA_PATH}/token_breakdown/token_breakdown_{event}.json",
                "r",
                encoding="utf-8",
            ) as f:
                derivative_dict = json.load(f)
            for _, ptc_dict in derivative_dict["staked_token"].items():
                for derivative_token, staked_token_dict in ptc_dict.items():
                    if token_address == derivative_token:
                        underlying_token_value = 0
                        for (
                            staked_token,
                            staked_token_quantity,
                        ) in staked_token_dict.items():
                            try:
                                underlying_token_price = self.get_price(
                                    staked_token, timestamp
                                )
                            except:
                                underlying_token_price = self.get_price_with_derivative(
                                    staked_token, event, timestamp, block
                                )
                            underlying_token_value += (
                                underlying_token_price * staked_token_quantity
                            )

                        return underlying_token_value / total_supply_normalized(
                            token_address, block
                        )

    def get_lp_price(self, lp_token_address: str, timestamp: int, event: str) -> float:
        """
        Function to get the price of the lp token
        """
        with open(
            f"{PROCESSED_DATA_PATH}/token_breakdown/token_breakdown_{event}.json",
            "r",
            encoding="utf-8",
        ) as f:
            derivative_dict = json.load(f)

        underlying_token_value = 0

        for staked_token_address, staked_token_quantity in derivative_dict[
            "staked_token"
        ]["UniswapV2"][lp_token_address].items():
            try:
                underlying_token_value += (
                    self.get_price(staked_token_address, timestamp)
                    * staked_token_quantity
                )
                token_with_data = staked_token_address
            except:  # pylint: disable=bare-except
                pass

        for staked_token_address, staked_token_quantity in derivative_dict[
            "staked_token"
        ]["UniswapV2"][lp_token_address].items():
            if staked_token_address == token_with_data:
                another_token_quantity = staked_token_quantity
                another_token_price = self.get_price(staked_token_address, timestamp)
            else:
                token_quantity = staked_token_quantity

        token_price = another_token_price * another_token_quantity / token_quantity
        underlying_token_value += token_price * token_quantity

        return (
            underlying_token_value
            / derivative_dict["receipt_token"]["UniswapV2"][lp_token_address]
        )


if __name__ == "__main__":
    from environ.fetch.block import date_close_to_timestamp, date_close_to_block

    defillama = DeFiLlama()
    token_address = "0xBb2b8038a1640196FbE3e38816F3e67Cba72D940"
    event = "max_tvl"
    timestamp = date_close_to_timestamp("2021-12-26")
    block = date_close_to_block("2021-12-26")

    print(defillama.get_price(token_address, timestamp))
    # print(defillama.get_price_with_derivative(token_address, event, timestamp, block))

    # print(
    #     defillama.get_lp_price(
    #         "0x17eE04ec364577937855D2e9a7adD8d2a957E4Fa",
    #         timestamp,
    #         event,
    #     )
    # )

    # print(defillama.get_price("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", timestamp))

    # with open(
    #     f"{PROCESSED_DATA_PATH}/token_breakdown/token_breakdown_{event}.json",
    #     "r",
    #     encoding="utf-8",
    # ) as f:
    #     derivative_dict = json.load(f)

    # for _, ptc_dict in derivative_dict["staked_token"].items():
    #     for derivative_token, staked_token_dict in ptc_dict.items():
    #         if token_address == derivative_token:
    #             underlying_token_quantity = 0
    #             underlying_token_value = 0
    #             for (
    #                 staked_token,
    #                 staked_token_quantity,
    #             ) in staked_token_dict.items():
    #                 underlying_token_quantity += staked_token_quantity
    #                 underlying_token_price = get_price(staked_token, timestamp)
    #                 underlying_token_value += (
    #                     underlying_token_price * staked_token_quantity
    #                 )
    #             print(underlying_token_value / underlying_token_quantity)
