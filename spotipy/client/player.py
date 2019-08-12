from spotipy.client._base import SpotifyBase


class SpotifyPlayer(SpotifyBase):
    def playback(self, market: str = 'from_token'):
        """
        Get information about user's current playback.

        Parameters:
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get('me/player', market=market)

    def playback_currently_playing(self, market: str = 'from_token'):
        """
        Get user's currently playing track.

        Parameters:
            - market - An ISO 3166-1 alpha-2 country code or 'from_token'
        """
        return self._get('me/player/currently-playing', market=market)

    def playback_recently_played(self, limit: int = 20, after: str = None, before: str = None):
        """
        Get tracks from the current user's recently played tracks.
        Only after or before should be specified at one time.

        Parameters:
            - limit - the number of items to return (1..50)
            - after - a unix timestamp in milliseconds
            - before - a unix timestamp in milliseconds
        """
        return self._get('me/player/recently-played', limit=limit, after=after, before=before)

    def playback_devices(self):
        return self._get('me/player/devices')

    def playback_transfer(self, device_id: str, force_play: bool = False):
        """
        Transfer playback to another device.
        Note that the API accepts a list of device ids, but only actually supports one.

        Parameters:
            - device_id - transfer playback to this device
            - force_play - true: after transfer, play. false: keep current state.
        """
        data = {
            'device_ids': [device_id],
            'play': force_play
        }
        return self._put('me/player', payload=data)

    def playback_start(self, context_uri: str = None, uris: list = None, offset: dict = None,
                       position_ms: int = None, device_id: str = None):
        """
        Start or resume user's playback.

        Provide a `context_uri` to start playback or a album, artist, or playlist
        Provide a `uris` list to start playback of one or more tracks
        Provide `offset` as {"position": <int>} or {"uri": "<track uri>"}
        to start playback at a particular offset.

        Parameters:
            - context_uri - spotify context uri to play
            - uris - spotify track uris
            - offset - offset into context by index or track uri
            - position_ms - position of track
            - device_id - device target for playback
        """
        payload = {
            'context_uri': context_uri,
            'uris': uris,
            'offset': offset,
            'position_ms': position_ms,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        return self._put('me/player/play', payload=payload, device_id=device_id)

    def playback_pause(self, device_id: str = None):
        return self._put('me/player/pause', device_id=device_id)

    def playback_next(self, device_id: str = None):
        return self._post('me/player/next', device_id=device_id)

    def playback_previous(self, device_id: str = None):
        return self._post('me/player/previous', device_id=device_id)

    def playback_seek(self, position_ms: int, device_id: str = None):
        return self._put('me/player/seek', position_ms=position_ms, device_id=device_id)

    def playback_repeat(self, state: str, device_id: str = None):
        """
        Set repeat mode for playback.

        Parameters:
            - state - `track`, `context`, or `off`
            - device_id - device target for playback
        """
        self._put('me/player/repeat', state=state, device_id=device_id)

    def playback_shuffle(self, state: bool, device_id: str = None):
        state = 'true' if state else 'false'
        self._put('me/player/shuffle', state=state, device_id=device_id)

    def playback_volume(self, volume_percent: int, device_id: str = None):
        if volume_percent < 0:
            volume_percent = 0
        elif volume_percent > 100:
            volume_percent = 100

        self._put('me/player/volume', volume_percent=volume_percent, device_id=device_id)