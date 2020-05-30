# Run this script first to start the server and then call api_client.py

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus
import json

trips_db = None


def load_trips():
    """
    E.g
    Returns:
        [{'vendor': 1, 'pickup': '2018-11-01T00:58:33', 'dropoff': '2018-11-01T01:10:49', 'passengers': 3, 'distance': 1.6, 'tip': 2.7, 'amount': 13.5}, 
        {'vendor': 1, 'pickup': '2018-11-01T00:58:38', 'dropoff': '2018-11-01T01:20:08', 'passengers': 2, 'distance': 2.4, 'tip': 3.25, 'amount': 19.55},
         {'vendor': 2, 'pickup': '2018-11-01T00:58:41', 'dropoff': '2018-11-01T01:03:55', 'passengers': 1, 'distance': 1.02, 'tip': 1.36, 'amount': 8.16}]
    """
    here = Path(__file__).absolute().parent
    reply_file = here / 'trips.json'
    with reply_file.open('rb') as fp:
        return json.load(fp)


class Handler(BaseHTTPRequestHandler):
    """
    For the request method GET, the do_GET() method will be called with no arguments.
    The BaseHTTPRequestHandler has the following instance variables:
        client_address, server, path, headers, responses, wfile, etc.
    The BaseHTTPRequestHandler has the following methods:
        send_error, handle, end_headers

    self.headers looks something like this:
        Host: localhost:8989
        User-Agent: python-requests/2.22.0
        Accept-Encoding: gzip, deflate
        Accept: */*
        Connection: keep-alive
        x-trips-token: l3tm3in
    """
    def do_GET(self):
        url = urlparse(self.path)  # self.path --> /trips?start=2018-11-01T00%3A02%3A04&end=2018-11-01T00%3A44%3A51
        print('The url: ', url)  # ParseResult(scheme='', netloc='', path='/trips', params='', query='start=2018-11-01T00%3A02%3A04&end=2018-11-01T00%3A44%3A51', fragment='')
        if url.path != '/trips':
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        auth = self.headers.get('X-TRIPS-TOKEN')
        if auth != 'l3tm3in':
            self.send_error(HTTPStatus.UNAUTHORIZED)
            return

        args = parse_qs(url.query)  # {'start': ['2018-11-01T00:02:04'], 'end': ['2018-11-01T00:44:51']}
        if 'start' not in args or 'end' not in args:
            self.send_error(HTTPStatus.BAD_REQUEST)
            return

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        start = args['start'][0]
        end = args['end'][0]
        reply = {
            'ok': True,
            'trips': [
                trip for trip in trips_db
                if trip['pickup'] >= start and trip['pickup'] < end
            ],
        }
        data = json.dumps(reply)
        self.wfile.write(data.encode('utf-8'))  # Writes response back to the client.


if __name__ == '__main__':
    host, port = 'localhost', 8989
    server = ThreadingHTTPServer((host, port), Handler)
    trips_db = load_trips()
    print(f'server ready on {host}:{port}')
    server.serve_forever()
