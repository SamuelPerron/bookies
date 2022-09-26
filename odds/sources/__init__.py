from bs4 import BeautifulSoup
import requests


class Source:
    def _fetch_url(self, url):
        headers = {}

        response = requests.get(
            url,
            headers=headers
        )

        return response

    def _fetch_document(self, url):
        response = self._fetch_url(url)
        return BeautifulSoup(response.text, 'html.parser')

    def _params_to_url(self, params):
        url = '?'

        for param in params:
            url += f'&{param}={params[param]}'

        return url
