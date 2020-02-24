from typing import List
from dataclasses import dataclass

from tekore.model.base import Item
from tekore.model.paging import CursorPaging, OffsetPaging
from tekore.model.member import Followers, Image


@dataclass(repr=False)
class Artist(Item):
    external_urls: dict
    name: str


@dataclass(repr=False)
class SimpleArtist(Artist):
    pass


@dataclass(repr=False)
class FullArtist(Artist):
    followers: Followers
    genres: List[str]
    images: List[Image]
    popularity: int

    def __post_init__(self):
        self.followers = Followers(**self.followers)
        self.images = [Image(**i) for i in self.images]


@dataclass(repr=False)
class FullArtistCursorPaging(CursorPaging):
    items: List[FullArtist]
    total: int

    def __post_init__(self):
        super().__post_init__()
        self.items = [FullArtist(**a) for a in self.items]


@dataclass(repr=False)
class FullArtistOffsetPaging(OffsetPaging):
    items: List[FullArtist]

    def __post_init__(self):
        self.items = [FullArtist(**a) for a in self.items]
