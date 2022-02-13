import json

metadata = json.load(open("./trace/metadata.json"))
route = metadata['route']
regions = json.load(open("./trace/regions.json"))


def get_region(gps):
    # Look up GPS
    for index, loc in enumerate(route):
        if gps != loc: continue

        for region, range in regions.items():
            if index >=  range["start"] and index <= range["end"]:
                return region.lower()


# Analze route (trace of GPS locations)
# Return a list of regions starting from the beginning region to destination
def analyze_route(route):
    # Parse 'route' into sequential gps locations
    locs = route.split(";")
    
    regions = []
    for loc in locs:
        # Format GPS into compatible format with metadata
        parts = loc.split(" ")
        gps_loc = [float(parts[0]), float(parts[1])]

        region = get_region(gps_loc)
        # Append as new region if this 'region' is not the same as latest added region (regions[-1])
        if len(regions) == 0 or region != regions[-1]:
            regions.append(region)

    return regions


def get_region_json_map(region):
    return json.load(open(f"./trace/{region}.json"))


def get_gps_str(gps):
    assert type(gps) == list
    assert len(gps) == 2
    assert type(gps[0]) == float
    assert type(gps[1]) == float

    return f"{gps[0]} {gps[1]}" 
