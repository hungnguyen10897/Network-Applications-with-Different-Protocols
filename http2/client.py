import sys
import time
from hyper import HTTP20Connection
from logic import get_gps_str, route, get_region


speed = 1 # (gps/s)
trace = route[1:90]
# trace.reverse()

trace_header = ";".join(list(map(lambda gps: get_gps_str(gps), trace)))

if __name__ == "__main__":

    c = HTTP20Connection('localhost:8080', enable_push=True)

    req = c.request('GET', '/', headers={ 'gps' : trace_header})
    res = c.get_response()
    pushes = c.get_pushes()

    if not res:
        print("No response from server.")
        sys.exit(0)

    start_gps = trace[0]
    start_region = get_region(start_gps)

    print(f"Start GPS: {get_gps_str(start_gps)}")
    print(f"\tStart Region: {start_region.upper()}")
    print(f"\t{start_region.upper()} map:")
    print(res.read())

    region = get_region(start_gps)

    for gps in trace[1:]:
        
        current_region = get_region(gps)
        print(f"\nAt GPS: {get_gps_str(gps)}")

        if current_region != region:
            push = pushes.__next__()
            print(f"\tEnter New Region: {current_region.upper()}")
            print(f"\t{current_region.upper()} map:")
            print(push.get_response().read())
            region = current_region
            
        time.sleep(speed)
