import json
from pathlib import Path

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
    print(f"Error: GPS location {gps} cannot be found")
    return None


# Analze route (trace of GPS locations)
# Return a list of regions starting from the beginning region to destination
def analyze_route(route):
    try:
        # Parse 'route' into sequential gps locations
        locs = route.split(";")
        
        regions = []
        for loc in locs:
            # Format GPS into compatible format with metadata
            parts = loc.split(" ")
            gps_loc = [float(parts[0]), float(parts[1])]

            region = get_region(gps_loc)
            if region is None:
                return None
            # Append as new region if this 'region' is not the same as latest added region (regions[-1])
            if len(regions) == 0 or region != regions[-1]:
                regions.append(region)

        return regions
    except Exception as e:
        print(f"Error while parsing route: {e}")
        return None


def get_region_json_map(region):
    p = Path(f"./trace/{region}.json")
    if p.exists():
        return json.load(open(p))
    print(f"Map file for region {region.upper()} cannot be found")
    return None


def get_gps_str(gps):
    assert type(gps) == list
    assert len(gps) == 2
    assert type(gps[0]) in [float,int]
    assert type(gps[1]) in [float,int]

    return f"{gps[0]} {gps[1]}" 
