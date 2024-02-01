"""
Aave class
"""

from typing import Any

from environ.fetch.function_caller import FunctionCaller
from scripts.w3 import w3

POOL_V2_ADDRESS = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"
POOL_DATA_PROVIDER_V2_ADDRESS = "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d"

POOL_V3_ADDRESS = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"


class AaveV2:
    """
    Class for Aave V2
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def get_reserve_list(self, block_identifier: int) -> Any:
        """
        Function to get the reserves list
        """

        caller = FunctionCaller(POOL_V2_ADDRESS, self.w3)
        return caller.call_function("getReservesList", block_identifier)

    def get_all_reservs_tokens(self, block_identifier: int) -> list[tuple[str, str]]:
        """
        Function to get all the reserve tokens
        """

        caller = FunctionCaller(POOL_DATA_PROVIDER_V2_ADDRESS, self.w3)
        return caller.call_function("getAllReservesTokens", block_identifier)

    def get_reserve_tokens_addresses(self, block_identifier, asset) -> list[str]:
        """
        Function to get all the reserve tokens
        """

        caller = FunctionCaller(POOL_DATA_PROVIDER_V2_ADDRESS, self.w3)
        return caller.call_function(
            "getReserveTokensAddresses", block_identifier, [asset]
        )

    def get_token_data(self, block_identifier: int) -> list[dict[str, str]]:
        """
        Function to get all reserve data
        """
        token_data = []

        for symbol, address in self.get_all_reservs_tokens(block_identifier):
            (
                atoken_address,
                stable_debt_token_address,
                variable_debt_token_address,
            ) = self.get_reserve_tokens_addresses(block_identifier, address)

            token_data.append(
                {
                    "reserve_symbol": symbol,
                    "reserve_address": address,
                    "atoken_address": atoken_address,
                    "stable_debt_token_address": stable_debt_token_address,
                    "variable_debt_token_address": variable_debt_token_address,
                }
            )

        return token_data

    def get_user_debt_data(
        self, user_address: str, debt_token_address, block_identifier: int
    ) -> list[tuple[str, str, str, str, str, str]]:
        """
        Function to get the user debt data
        """

        caller = FunctionCaller(debt_token_address, self.w3)
        return caller.call_function(
            "balanceOf", block_identifier, [user_address], erc20=True
        )

    def get_user_reserve_data(
        self, user_addres: str, reserve_address: str, block_identifier: int
    ) -> list[tuple[str, str, str, str, str, str]]:
        """
        Function to get the user reserve data
        """

        caller = FunctionCaller(POOL_DATA_PROVIDER_V2_ADDRESS, self.w3)
        return caller.call_function(
            "getUserReserveData", block_identifier, [reserve_address, user_addres]
        )

    def get_user_account_data(self, user_address: str, block_identifier: int) -> Any:
        """
        Function to get the user account data
        """

        caller = FunctionCaller(POOL_V2_ADDRESS, self.w3)
        return caller.call_function(
            "getUserAccountData", block_identifier, [user_address]
        )

    def get_user_configuration(self, user_address: str, block_identifier: int) -> Any:
        """
        Function to get the user configuration
        """

        caller = FunctionCaller(POOL_V2_ADDRESS, self.w3)
        return caller.call_function(
            "getUserConfiguration", block_identifier, [user_address]
        )


# class AaveV3:
#     """
#     Class for Aave V3
#     """

#     def __init__(self, w3) -> None:
#         self.w3 = w3

#     def get_reserve_list(self, block_identifier) -> Any:
#         """
#         Function to get the reserves list
#         """

#         caller = FunctionCaller(POOL_V3_ADDRESS, self.w3)
#         return caller.call_function("getReservesList", block_identifier)


if __name__ == "__main__":
    AaveV2 = AaveV2(w3)
    # print(
    #     AaveV2.get_user_debt_data(
    #         "0xBD723fc4f1d737dCFc48a07FE7336766d34CAD5f",
    #         "0x6C3c78838c761c6Ac7bE9F59fe808ea2A6E4379d",
    #         11367824,
    #     )
    # )

    print(
        AaveV2.get_user_reserve_data(
            "0x4Fabb145d64652a948d72533023f6E7A623C7C53",
            "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            11367824,
        )
    )
    pass
