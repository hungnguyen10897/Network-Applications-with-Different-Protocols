import json

metadata = json.load(open("./trace/metadata.json"))
route = metadata['route']
regions = json.load(open("./trace/regions.json"))


def get_region_json_map(gps_str):

    # Format GPS into compatible format with metadata
    parts = gps_str.split(" ")
    gps_tuple = [float(parts[0]), float(parts[1])]

    # Look up GPS
    for index, loc in enumerate(route):
        if gps_tuple != loc: continue

        for region, range in regions.items():
            if index >=  range["start"] and index <= range["end"]:
                return json.load(open(f"./trace/{region.lower()}.json"))

