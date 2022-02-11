import json

metadata = json.load(open("./trace/metadata.json"))
route = metadata['route']
regions = json.load(open("./trace/regions.json"))


def parse_gps(gps_str):
    # Parse gps_str into sequential gps locations
    # Format GPS into compatible format with metadata
    locs = gps_str.split(";")
    parsed = []
    for loc in locs:
        parts = loc.split(" ")
        parsed.append((float(parts[0]), float(parts[1])))
    return parsed 


def get_region_json_map(gps):

    # Look up GPS
    for index, loc in enumerate(route):
        if gps != tuple(loc): continue

        for region, range in regions.items():
            if index >=  range["start"] and index <= range["end"]:
                return json.load(open(f"./trace/{region.lower()}.json"))

