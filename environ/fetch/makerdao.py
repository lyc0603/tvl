"""
Script to fetch MakerDAO data
"""

from typing import ByteString

from environ.fetch.function_caller import FunctionCaller
from environ.fetch.w3 import token_balance_normalized

ILK_REGISTRY_ADDRESS = "0x5a464C28D19848f44199D003BeF5ecc87d090F87"
CDP_MANAGER_ADDRESS = "0x5ef30b9986345249bc32d8928B7ee64DE9435E39"
VAT_ADDRESS = "0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B"
DAI_ADDRESS = "0x6B175474E89094C44Da98b954EedeAC495271d0F"


class MakerDAO:
    """
    Class to fetch MakerDAO data
    """

    def __init__(self):
        self.vaults = {}

    def cdpi(self, block_identifier: int | str = "latest") -> int:
        """
        Method to count the number of vaults
        """

        caller = FunctionCaller(CDP_MANAGER_ADDRESS)
        return caller.call_function("cdpi", block_identifier)

    def ilks(self, ilk_id: int, block_identifier: int | str = "latest") -> ByteString:
        """
        Method to get the ilk info
        """

        caller = FunctionCaller(CDP_MANAGER_ADDRESS)
        return caller.call_function("ilks", block_identifier, [ilk_id])

    def urns(self, urn_id: int, block_identifier: int | str = "latest") -> float:
        """
        Method to get the urn address
        """

        caller = FunctionCaller(CDP_MANAGER_ADDRESS)
        return caller.call_function("urns", block_identifier, [urn_id])

    def urns_data(
        self,
        ilk_id: ByteString,
        urn_address: float,
        block_identifier: int | str = "latest",
    ) -> tuple[int, int]:
        """
        Method to get the urn data
        """

        caller = FunctionCaller(VAT_ADDRESS)
        return caller.call_function("urns", block_identifier, [ilk_id, urn_address])

    def list(self, block_identifier: int | str = "latest") -> list:
        """
        Method to get all lists
        """

        caller = FunctionCaller(ILK_REGISTRY_ADDRESS)
        return caller.call_function("list", block_identifier)

    def info(self, ilk: ByteString, block_identifier: int | str = "latest") -> tuple:
        """
        Method to get the info
        """

        caller = FunctionCaller(ILK_REGISTRY_ADDRESS)
        return caller.call_function("info", block_identifier, [ilk])

    def ilks_info(
        self, ilk: ByteString, block_identifier: int | str = "latest"
    ) -> tuple:
        """
        Method to get the ilk info
        """

        caller = FunctionCaller(VAT_ADDRESS)
        return caller.call_function("ilks", block_identifier, [ilk])

    def ilk_data(
        self, ilk: ByteString, block_identifier: int | str = "latest"
    ) -> tuple:
        """
        Method to get the ilk info
        """

        caller = FunctionCaller(ILK_REGISTRY_ADDRESS)
        return caller.call_function("ilkData", block_identifier, [ilk])

    def token_breakdown(self, block_identifier: int | str = "latest"):
        """
        Get token breakdown
        """

        token_breakdown_dict = {"receipt_token": {}, "staked_token": {}}
        token_breakdown_dict["receipt_token"][DAI_ADDRESS] = 0
        token_breakdown_dict["staked_token"][DAI_ADDRESS] = {}

        for ilk in self.list(block_identifier):
            token_breakdown_dict["staked_token"][DAI_ADDRESS][
                self.info(ilk, block_identifier)[4]
            ] = 0

        for ilk in self.list(block_identifier):
            try:
                ilk_address_data = self.ilk_data(ilk, block_identifier)
                join = ilk_address_data[1]
                gem = ilk_address_data[2]

                token_breakdown_dict["staked_token"][DAI_ADDRESS][
                    gem
                ] += token_balance_normalized(gem, join, block_identifier)

                ilk_debt_data = self.ilks_info(ilk, block_identifier)

                token_breakdown_dict["receipt_token"][DAI_ADDRESS] += (
                    ilk_debt_data[0] / 10**18
                ) * (ilk_debt_data[1] / 10**27)
            except:  # pylint: disable=bare-except
                pass

        return token_breakdown_dict


if __name__ == "__main__":
    from pprint import pprint

    from web3 import Web3

    makerdao = MakerDAO()
    # cdp_id = 14282
    # # for cdp_id in tqdm(range(makerdao.cdpi())):
    # print(Web3.to_hex(makerdao.ilks(cdp_id)))
    # print(makerdao.urns(cdp_id))
    # print(makerdao.urns_data(makerdao.ilks(cdp_id), makerdao.urns(cdp_id)))
    # print(
    #     makerdao.urns_data(
    #         Web3.to_bytes(
    #             hexstr="0x555344432d410000000000000000000000000000000000000000000000000000"
    #         ),
    #         makerdao.urns(cdp_id),
    #     )
    # )
    # print(makerdao.list("latest"))
    # print(makerdao.info(makerdao.list("latest")[6]))
    # print(makerdao.ilks_info(makerdao.list("latest")[6]))
    pprint(makerdao.token_breakdown("latest"))
