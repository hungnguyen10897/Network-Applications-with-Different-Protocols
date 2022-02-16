import sys
import time
import os
from hyper import HTTP20Connection
from logic import get_gps_str, route, get_region


# Invalid GPS
# trace = [[121212, 24.927370699999997]]

# Invalid GPS
# trace = route[80:98] + [[121212, 24.927370699999997]]

# Espoo -> Helsinki -> Espoo
# trace2 = route[80:98]
# trace2.reverse()
# trace = route[80:98] + trace2

start_trace_index = 80
end_trace_index = 98

# Helsinki -> Espoo
trace = route[start_trace_index:end_trace_index]
trace.reverse()

# Espoo -> Helsinki
# trace = route[80:98]

speed = 1 # (gps/s)
trace_header = ";".join(list(map(lambda gps: get_gps_str(gps), trace)))

def send_photo_with_gps(conn, gps_index):
    print(f"Sending photo for {get_gps_str(gps)}")
    image_path = f"./trace/images/gsv_{gps_index}.jpg"
    image_size = os.path.getsize(image_path)
    print(f"image_size: {image_size}")
    image_file = open(image_path, "rb")
    req = c.request('POST', '/', body=image_file, headers={ 'type': 'put_image', 'gps' : trace_header, 'Content-Length': image_size})
    res = c.get_response()
    print(res.read())
    image_file.close()


if __name__ == "__main__":

    c = HTTP20Connection('localhost:8080', enable_push=True)

    req = c.request('GET', '/', headers={ 'type': 'get_map', 'gps' : trace_header})
    res = c.get_response()

    if not res:
        print("No response from server.")
        sys.exit(1)

    if res.status != 200:
        message = res.read().decode("utf-8")
        print(f"Status code: {res.status} returned from server - Message: {message}")
        sys.exit(1)

    pushes = c.get_pushes()

    start_gps = trace[0]
    start_region = get_region(start_gps)

    print(f"Start GPS: {get_gps_str(start_gps)}")
    print(f"\tStart Region: {start_region.upper()}")
    print(f"\t{start_region.upper()} map:")
    print(res.read())

    region = get_region(start_gps)

    for (index, gps) in enumerate(trace[1:]):
        
        current_region = get_region(gps)
        print(f"\nAt GPS: {get_gps_str(gps)}")

        gps_index = start_trace_index + index
        send_photo_with_gps(c, gps_index)

        if current_region != region:
            push = pushes.__next__()
            print(f"\tEnter New Region: {current_region.upper()}")
            print(f"\t{current_region.upper()} map:")
            print(push.get_response().read())
            region = current_region
            
        time.sleep(speed)
        # Uncomment when testing with one request
        #break
