from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        url_components = parse.urlsplit(url)
        query_string_list = parse.parse_qsl(url_components.query)
        dictionary = dict(query_string_list)

        country = dictionary.get('country')
        countries_api_url = f"https://restcountries.com/v3.1/name/{country}"
        response = requests.get(countries_api_url)
        data = response.json()
        # country = next((x for x in data if x.get('capital') == country), None)

        if country:
            capital = data[0]['capital'][0]
            country_name = data[0]['name']['common']
            message = f"The capital of {country_name} is {capital}."
        else:
            message = f"Sorry, could not find a country with capital {country}."
        print(message)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())


if __name__ == '__main__':
    server_address = ('localhost', 8000)  # use any available port
    httpd = HTTPServer(server_address, handler)  # httpd is a commonly used abbreviation for "HTTP Daemon"
    print(f'Starting httpd server on {server_address[0]}:{server_address[1]}')
    httpd.serve_forever()
