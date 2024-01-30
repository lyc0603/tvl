"""
Script to fetch MakerDAO data
"""

from dataclasses import dataclass
from typing import ByteString

from environ.fetch.function_caller import FunctionCaller

CDP_MANAGER_ADDRESS = "0x5ef30b9986345249bc32d8928B7ee64DE9435E39"
VAT_ADDRESS = "0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B"


@dataclass
class Urn:
    """
    Class for MakerDAO vaults
    """

    collateral_type: str
    collateral_amount: float
    debt_amount: float


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
        return caller.call_function("ilks", block_identifier, ilk_id)


if __name__ == "__main__":
    makerdao = MakerDAO()
    print(makerdao.cdpi())
    print(makerdao.ilks(1))
