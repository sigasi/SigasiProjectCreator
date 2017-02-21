from enum import Enum, unique


@unique
class VHDLVersion(Enum):
    # Not supported
    # EIGHTY_SEVEN = 87
    NINETY_THREE = 93
    TWO_O_O_TWO = 2002
    TWO_O_O_EIGHT = 2008
