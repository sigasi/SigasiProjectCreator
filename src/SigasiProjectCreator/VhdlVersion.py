# Not supported
# EIGHTY_SEVEN = 87
NINETY_THREE = 93
TWENTY_O_TWO = 2002
TWENTY_O_EIGHT = 2008
TWENTY_NINETEEN = 2019


def get_enums():
    return [NINETY_THREE, TWENTY_O_TWO, TWENTY_O_EIGHT, TWENTY_NINETEEN]


def get_str_enums():
    return [str(version) for version in get_enums()]
