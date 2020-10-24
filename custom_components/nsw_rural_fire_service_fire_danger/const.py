"""NSW Rural Fire Service - Fire Danger - Consts."""

CONF_DISTRICT_NAME = "district_name"

DEFAULT_ATTRIBUTION = "NSW Rural Fire Service"

DEFAULT_FORCE_UPDATE = True
DEFAULT_METHOD = "GET"
DEFAULT_NAME = "Fire Danger"
DEFAULT_VERIFY_SSL = True

SENSOR_ATTRIBUTES = {
    # <XML Key>: [<Display Name>, <Conversion Function>]
    "RegionNumber": ["region_number", lambda x: int(x)],
    "Councils": ["councils", lambda x: x.split(";")],
    "DangerLevelToday": ["danger_level_today", lambda x: x.lower().capitalize()],
    "DangerLevelTomorrow": ["danger_level_tomorrow", lambda x: x.lower().capitalize()],
    "FireBanToday": ["fire_ban_today", lambda x: x == "Yes"],
    "FireBanTomorrow": ["fire_ban_tomorrow", lambda x: x == "Yes"],
}

URL = "http://www.rfs.nsw.gov.au/feeds/fdrToban.xml"

XML_DISTRICT = "District"
XML_FIRE_DANGER_MAP = "FireDangerMap"
XML_NAME = "Name"
