"""
Aave class
"""

from typing import Any

from environ.fetch.function_caller import FunctionCaller
from environ.fetch.w3 import total_supply_normalized
from scripts.w3 import w3

POOL_V2_ADDRESS = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"
POOL_DATA_PROVIDER_V2_ADDRESS = "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d"
PRICE_ORACLE_V2_ADDRESS = "0xA50ba011c48153De246E5192C8f9258A2ba79Ca9"

POOL_V3_ADDRESS = "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2"


class AaveV2:
    """
    Class for Aave V2
    """

    def __init__(self, w3) -> None:
        self.w3 = w3

    def get_reserve_list(self, block_identifier: int | str) -> Any:
        """
        Function to get the reserves list
        """

        caller = FunctionCaller(POOL_V2_ADDRESS, self.w3)
        return caller.call_function("getReservesList", block_identifier)

    def get_all_reservs_tokens(
        self, block_identifier: int | str
    ) -> list[tuple[str, str]]:
        """
        Function to get all the reserve tokens
        """

        caller = FunctionCaller(POOL_DATA_PROVIDER_V2_ADDRESS, self.w3)
        return caller.call_function("getAllReservesTokens", block_identifier)

    def get_reserve_tokens_addresses(
        self, block_identifier: int | str, asset: str
    ) -> list[str]:
        """
        Function to get all the reserve tokens
        """

        caller = FunctionCaller(POOL_DATA_PROVIDER_V2_ADDRESS, self.w3)
        return caller.call_function(
            "getReserveTokensAddresses", block_identifier, [asset]
        )

    def get_token_data(self, block_identifier: int | str) -> list[dict[str, str]]:
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
        self, user_address: str, debt_token_address, block_identifier: int | str
    ) -> list[tuple[str, str, str, str, str, str]]:
        """
        Function to get the user debt data
        """

        caller = FunctionCaller(debt_token_address, self.w3)
        return caller.call_function(
            "balanceOf", block_identifier, [user_address], erc20=True
        )

    def get_user_reserve_data(
        self, user_addres: str, reserve_address: str, block_identifier: int | str
    ) -> list[tuple[str, str, str, str, str, str]]:
        """
        Function to get the user reserve data
        """

        caller = FunctionCaller(POOL_DATA_PROVIDER_V2_ADDRESS, self.w3)
        return caller.call_function(
            "getUserReserveData", block_identifier, [reserve_address, user_addres]
        )

    def get_user_account_data(
        self, user_address: str, block_identifier: int | str
    ) -> Any:
        """
        Function to get the user account data
        """

        caller = FunctionCaller(POOL_V2_ADDRESS, self.w3)
        return caller.call_function(
            "getUserAccountData", block_identifier, [user_address]
        )

    def get_user_configuration(
        self, user_address: str, block_identifier: int | str
    ) -> Any:
        """
        Function to get the user configuration
        """

        caller = FunctionCaller(POOL_V2_ADDRESS, self.w3)
        return caller.call_function(
            "getUserConfiguration", block_identifier, [user_address]
        )

    def get_reserve_configuration_data(
        self, reserve_address: str, block_identifier: int | str
    ) -> Any:
        """
        Function to get the reserve configuration data
        """

        caller = FunctionCaller(POOL_DATA_PROVIDER_V2_ADDRESS, self.w3)
        return caller.call_function(
            "getReserveConfigurationData", block_identifier, [reserve_address]
        )

    def get_asset_price(self, asset: str, block_identifier: int | str) -> Any:
        """
        Function to get the asset price
        """

        caller = FunctionCaller(PRICE_ORACLE_V2_ADDRESS, self.w3)
        return caller.call_function("getAssetPrice", block_identifier, [asset])

    def underlying_asset_address(
        self, atoken_address: str, block_identifier: int | str
    ) -> Any:
        """
        Function to get the underlying asset address
        """

        caller = FunctionCaller(atoken_address, self.w3)
        return caller.call_function(
            "UNDERLYING_ASSET_ADDRESS", block_identifier, abi_temp="atoken.json"
        )

    def token_breakdown(self, block_identifier: int | str) -> dict:
        """
        Function to get the token breakdown
        """

        token_breakdown_dict = {"receipt_token": {}, "staked_token": {}}

        for reserve in self.get_reserve_list(block_identifier):
            (
                atoken_address,
                _,
                _,
            ) = self.get_reserve_tokens_addresses(block_identifier, reserve)

            atoken_amount = total_supply_normalized(atoken_address, block_identifier)
            token_breakdown_dict["receipt_token"][atoken_address] = atoken_amount
            token_breakdown_dict["staked_token"][atoken_address] = {
                reserve: atoken_amount
            }

        return token_breakdown_dict


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
    ptc = AaveV2(w3)
    # print(ptc.token_breakdown("latest"))
    print(
        ptc.underlying_asset_address(
            "0x030bA81f1c18d280636F32af80b9AAd02Cf0854e", "latest"
        )
    )
    pass
