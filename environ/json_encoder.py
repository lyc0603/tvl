"""
JSON encoder for datetime objects.
"""

from json import JSONEncoder

from web3.datastructures import AttributeDict
from web3.types import HexBytes


class EthJSONEncoder(JSONEncoder):
    """
    JSON encoder for datetime objects.
    """

    def default(self, o):
        if isinstance(o, HexBytes):
            return o.hex()
        if isinstance(o, AttributeDict):
            return dict(o)
        if isinstance(o, bytes):
            return o.hex()
        return super().default(o)
