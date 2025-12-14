"""
Domain Layer - Entities

This module contains core business entities with no external dependencies.
Entities represent the core business concepts of the addon.
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class ContentType(Enum):
    """Content types supported by kino.pub"""
    ALL = "all"
    MOVIE = "movie"
    SERIAL = "serial"
    TVSHOW = "tvshow"
    CONCERT = "concert"
    DOCUMOVIE = "documovie"
    DOCUSERIAL = "docuserial"
    THREED = "3d"  # 3D content


class VideoQuality(Enum):
    """Video quality levels"""
    Q_2160 = "2160"  # 4K
    Q_1080 = "1080"  # Full HD
    Q_720 = "720"    # HD
    Q_480 = "480"    # SD


class StreamType(Enum):
    """Streaming protocol types"""
    HLS4 = "hls4"
    HLS2 = "hls2"
    HLS = "hls"
    DASH = "dash"


@dataclass
class Video:
    """Video file representation"""
    quality: VideoQuality
    url: str
    stream_type: StreamType


@dataclass
class Item:
    """Base content item"""
    id: int
    title: str
    content_type: ContentType
    year: Optional[int] = None
    rating_imdb: Optional[float] = None
    rating_kinopoisk: Optional[float] = None
    poster: Optional[str] = None
    description: Optional[str] = None
    genres: List[str] = None
    
    def __post_init__(self):
        if self.genres is None:
            self.genres = []


@dataclass
class Movie(Item):
    """Movie entity"""
    duration: Optional[int] = None  # in minutes
    videos: List[Video] = None
    trailer_url: Optional[str] = None
    
    def __post_init__(self):
        super().__post_init__()
        if self.videos is None:
            self.videos = []
        self.content_type = ContentType.MOVIE


@dataclass
class Episode:
    """TV show episode"""
    id: int
    title: str
    episode_number: int
    season_number: int
    duration: Optional[int] = None
    videos: List[Video] = None
    thumbnail: Optional[str] = None
    air_date: Optional[str] = None
    watched: bool = False
    
    def __post_init__(self):
        if self.videos is None:
            self.videos = []


@dataclass
class Season:
    """TV show season"""
    season_number: int
    episodes: List[Episode] = None
    
    def __post_init__(self):
        if self.episodes is None:
            self.episodes = []


@dataclass
class TVShow(Item):
    """TV show entity"""
    seasons: List[Season] = None
    total_episodes: int = 0
    new_episodes_count: int = 0
    
    def __post_init__(self):
        super().__post_init__()
        if self.seasons is None:
            self.seasons = []
        self.content_type = ContentType.SERIAL


@dataclass
class WatchState:
    """Playback watch state"""
    item_id: int
    watched: bool
    time: int  # Resume time in seconds
    duration: int  # Total duration in seconds
    
    @property
    def percentage(self) -> float:
        """Calculate watch percentage"""
        if self.duration == 0:
            return 0.0
        return (self.time / self.duration) * 100.0


@dataclass
class Bookmark:
    """Bookmark/favorite item"""
    id: int
    title: str
    item_count: int = 0


@dataclass
class Collection:
    """Content collection"""
    id: str
    title: str
    description: Optional[str] = None
    items: List[Item] = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []


@dataclass
class User:
    """User profile"""
    username: str
    subscription_active: bool = False
    subscription_expires: Optional[str] = None
