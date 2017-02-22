from enum import Enum, unique


@unique
class VhdlVersion(Enum):
    # Not supported
    # EIGHTY_SEVEN = 87
    NINETY_THREE = 93
    TWENTY_O_TWO = 2002
    TWENTY_O_EIGHT = 2008
