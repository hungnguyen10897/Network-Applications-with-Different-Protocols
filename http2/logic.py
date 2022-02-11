import json

metadata = json.load(open("./trace/metadata.json"))
route = metadata['route']
regions = json.load(open("./trace/regions.json"))


def get_region(gps):
    for index, loc in enumerate(route):
        if gps != loc: continue

        for region, range in regions.items():
            if index >=  range["start"] and index <= range["end"]:
                return region
