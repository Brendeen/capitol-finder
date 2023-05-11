from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        url_components = parse.urlsplit(url)
        query_string_list = parse.parse_qsl(url_components.query)
        dictionary = dict(query_string_list)

        capital = dictionary.get('capital')
        countries_api_url = "https://restcountries.com/v3.1/all"
        response = requests.get(countries_api_url)
        data = response.json()
        # print("data is:", data)
        country = next((x for x in data if x.get('capital') == capital), None)

        if country:
            capital_name = country['capital'][0]
            country_name = country['name']['common']
            message = f"The capital of {country_name} is {capital_name}."
        else:
            message = f"Sorry, could not find a country with capital {capital}."
        print("message is:", message)

        # Forming the response
        self.send_response(200)  # HTTP code
        self.send_header('Content-type', 'text/plain')  # define the content type
        self.end_headers()  # add a blank line
        self.wfile.write(message.encode())  # write the message


if __name__ == '__main__':
    server_address = ('localhost', 8000)  # use any available port
    httpd = HTTPServer(server_address, handler)  # httpd is a commonly used abbreviation for "HTTP Daemon"
    print(f'Starting httpd server on {server_address[0]}:{server_address[1]}')
    httpd.serve_forever()
