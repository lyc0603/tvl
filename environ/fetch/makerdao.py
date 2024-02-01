"""
Script to fetch MakerDAO data
"""

from typing import ByteString

from tqdm import tqdm

from environ.fetch.function_caller import FunctionCaller

CDP_MANAGER_ADDRESS = "0x5ef30b9986345249bc32d8928B7ee64DE9435E39"
VAT_ADDRESS = "0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B"


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


if __name__ == "__main__":
    from web3 import Web3

    makerdao = MakerDAO()
    cdp_id = 14282
    # for cdp_id in tqdm(range(makerdao.cdpi())):
    print(Web3.to_hex(makerdao.ilks(cdp_id)))
    print(makerdao.urns(cdp_id))
    print(makerdao.urns_data(makerdao.ilks(cdp_id), makerdao.urns(cdp_id)))
    print(
        makerdao.urns_data(
            Web3.to_bytes(
                hexstr="0x555344432d410000000000000000000000000000000000000000000000000000"
            ),
            makerdao.urns(cdp_id),
        )
    )
