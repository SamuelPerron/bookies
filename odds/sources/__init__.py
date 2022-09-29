import requests


class Source:
    def get_details_path(self):
        raise NotImplementedError

    def import_data(self):
        raise NotImplementedError

    def _fetch_url(self, url):
        headers = {}

        response = requests.get(
            url,
            headers=headers
        )

        return response

    def _params_to_url(self, params):
        url = '?'

        for param in params:
            url += f'&{param}={params[param]}'

        return url

