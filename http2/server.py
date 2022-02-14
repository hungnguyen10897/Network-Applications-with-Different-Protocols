import json
import socket

import h2.connection
import h2.events
import h2.config

from logic import analyze_route, get_region_json_map


def send_push(conn, event, regions):
    for region in regions[1:]:
        print(f"Sending PUSH for region {region.upper()}")
        push_id=conn.get_next_available_stream_id()

        # push_headers = []

        # for header in event.headers:
        #     if "gps" in header:
        #         header = ('gps', get_city_first_gps('espoo'))
        #     push_headers.append(header)

        conn.push_stream(
            stream_id=event.stream_id,
            promised_stream_id=push_id,
            request_headers=event.headers
        )

        response_data = json.dumps(
            get_region_json_map(region)
        ).encode('utf-8')

        conn.send_headers(
            stream_id=push_id,
            headers=[
                (':status', '200'),
                ('server', 'basic-h2-server/1.0'),
                ('content-length', str(len(response_data))),
                ('content-type', 'application/json'),
            ],
        )

        # Single GPS location
        conn.send_data(
            stream_id=push_id,
            data=response_data,
            end_stream=True
        )

def handle_get_map_response(conn, event):
    stream_id = event.stream_id
    gps_str = dict(event.headers)[b'gps']
    print("gps_str: ", gps_str)
    regions = analyze_route(gps_str.decode("utf-8"))

    if regions is None:
        status_code = 400
        response_data = json.dumps('Invalid GPS Header').encode('utf-8')

    else:
        # Immediately respond with map of the first GPS location
        map = get_region_json_map(regions[0])
        if map is None:
            status_code = 404
            response_data = json.dumps(f'Map for region {regions[0].upper()} not Found').encode('utf-8')
        else:
            if len(regions) > 1:
                send_push(conn,event, regions)
            status_code = 200
            response_data = json.dumps(map).encode('utf-8')

    conn.send_headers(
        stream_id=stream_id,
        headers=[
            (':status', str(status_code)),
            ('server', 'basic-h2-server/1.0'),
            ('content-length', str(len(response_data))),
            ('content-type', 'application/json'),
        ],
    )

    # Single GPS location
    conn.send_data(
        stream_id=stream_id,
        data=response_data,
        end_stream=True
    )

def send_response(conn, event):
    print(dict(event.headers))

    request_type = dict(event.headers)[b'type'].decode("utf-8")

    if request_type == 'get_map':
        handle_get_map_response(conn, event)


def handle(sock):
    config = h2.config.H2Configuration(client_side=False)
    conn = h2.connection.H2Connection(config=config)
    conn.initiate_connection()
    sock.sendall(conn.data_to_send())

    while True:
        data = sock.recv(65535)
        if not data:
            break

        events = conn.receive_data(data)
        for event in events:
            print(event)
            if isinstance(event, h2.events.RequestReceived):
                send_response(conn, event)

        data_to_send = conn.data_to_send()
        if data_to_send:
            sock.sendall(data_to_send)


if __name__ == "__main__":
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 8080))
    sock.listen(5)

    while True:
        handle(sock.accept()[0])
    