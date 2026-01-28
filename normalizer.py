import re

VEHICLE_MAP = {
    "32 ft": "32FT_CONTAINER",
    "32ft": "32FT_CONTAINER",
    "32 feet": "32FT_CONTAINER",
    "container": "CONTAINER",
    "truck": "TRUCK",
    "trailer": "TRAILER"
}

CITY_ALIASES = {
    "bombay": "Mumbai",
    "bengaluru": "Bangalore",
    "banglore": "Bangalore",
    "delhi": "Delhi",
    "mumbai": "Mumbai",
    "pune": "Pune"
}

def normalize_vehicle(v):
    if not v:
        return None
    v = v.lower()
    for k, val in VEHICLE_MAP.items():
        if k in v:
            return val
    return v.upper()

def normalize_city(c):
    if not c:
        return None
    c = c.strip().lower()
    return CITY_ALIASES.get(c, c.title())
