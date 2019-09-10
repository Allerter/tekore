import json

from contextlib import contextmanager
from requests import Request, HTTPError
from spotipy.sender import Sender, TransientSender


class SpotifyBase:
    prefix = 'https://api.spotify.com/v1/'

    def __init__(
            self,
            token: str = None,
            sender: Sender = None,
            requests_kwargs: dict = None
    ):
        """
        Create a Spotify API object.

        Parameters
        ----------
        token
            bearer token for requests
        sender
            request sender, TransientSender by default
        requests_kwargs
            keyword arguments for requests.request
        """
        self._token = token
        self.requests_kwargs = requests_kwargs or {}
        self.sender = sender or TransientSender()

    @contextmanager
    def token(self, token: str) -> 'SpotifyBase':
        self._token, old_token = token, self._token
        yield self
        self._token = old_token

    def _build_request(self, method: str, url: str, headers: dict = None) -> Request:
        if not url.startswith('http'):
            url = self.prefix + url

        default_headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json'
        }
        default_headers.update(headers or {})

        return Request(method, url, headers=default_headers)

    @staticmethod
    def _set_content(request: Request, payload=None, params: dict = None) -> None:
        params = params or {}
        request.params = {k: v for k, v in params.items() if v is not None}
        request.data = json.dumps(payload) if payload is not None else None

    def _send(self, request: Request):
        r = self.sender.send(request, **self.requests_kwargs)

        if r.status_code >= 400:
            raise HTTPError(f'Error ({r.status_code}) in {r.url}', request=r)

        if r.text and len(r.text) > 0:
            return r.json()
        else:
            return None

    def _get(self, url: str, payload=None, **params):
        r = self._build_request('GET', url)
        self._set_content(r, payload, params)
        return self._send(r)

    def _post(self, url: str, payload=None, **params):
        r = self._build_request('POST', url)
        self._set_content(r, payload, params)
        return self._send(r)

    def _delete(self, url: str, payload=None, **params):
        r = self._build_request('DELETE', url)
        self._set_content(r, payload, params)
        return self._send(r)

    def _put(self, url: str, payload=None, **params):
        r = self._build_request('PUT', url)
        self._set_content(r, payload, params)
        return self._send(r)

    def next(self, result):
        if result['next']:
            return self._get(result['next'])
        else:
            return None

    def previous(self, result):
        if result['previous']:
            return self._get(result['previous'])
        else:
            return None
