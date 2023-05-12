from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        # print('url', url)
        url_components = parse.urlsplit(url)
        query_string_list = parse.parse_qsl(url_components.query)
        # print('query_string_list', query_string_list)
        dic = dict(query_string_list)
        # print('dictionary', dic)

        country = dic.get('query')
        # print('country', country)
        countries_api_url = f"https://restcountries.com/v3.1/name/{country}"
        print("countries_api_url", countries_api_url)
        response = requests.get(countries_api_url)
        data = response.json()
        print(f'this is the data:', data)
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
    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, handler)
    print(f'Starting httpd server on {server_address[0]}:{server_address[1]}')
    httpd.serve_forever()
