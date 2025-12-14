# New Addon Architecture Design

Clean architecture design for the rewrite of kodi.kino.pub addon.

**Version:** 2.0 (Clean Rewrite)  
**Based On:** Reverse engineering of v1.x (legacy addon)  
**Architecture:** Clean Architecture / Hexagonal Architecture  
**Language:** Python 3.8+  
**Target:** Kodi 19+ (Matrix, Nexus, Omega)

---

## Design Principles

### Core Principles

1. **Separation of Concerns** - Clear boundaries between layers
2. **Dependency Inversion** - Dependencies point inward to domain
3. **Single Responsibility** - Each module has one reason to change
4. **Testability** - All business logic unit-testable
5. **No Legacy Code** - Clean slate, modern Python patterns

### Architecture Goals

- ✅ **Maintainable** - Easy to understand and modify
- ✅ **Testable** - High test coverage possible
- ✅ **Extensible** - Easy to add new features
- ✅ **Robust** - Comprehensive error handling
- ✅ **Type-safe** - Full type hints with mypy validation

---

## Layer Architecture

```
┌────────────────────────────────────────────────┐
│         Presentation Layer (Kodi UI)          │
│  ┌──────────────────────────────────────────┐ │
│  │  Routes / Menu Handlers                  │ │
│  │  - route decorators                      │ │
│  │  - ListItem builders                     │ │
│  │  - Dialog interactions                   │ │
│  └──────────────────────────────────────────┘ │
└─────────────────┬──────────────────────────────┘
                  │
                  ↓
┌────────────────────────────────────────────────┐
│          Application Layer (Use Cases)         │
│  ┌──────────────────────────────────────────┐ │
│  │  Use Case Services                       │ │
│  │  - BrowseContent                         │ │
│  │  - SearchContent                         │ │
│  │  - PlayVideo                             │ │
│  │  - ManageBookmarks                       │ │
│  │  - TrackWatchStatus                      │ │
│  └──────────────────────────────────────────┘ │
└─────────────────┬──────────────────────────────┘
                  │
                  ↓
┌────────────────────────────────────────────────┐
│           Domain Layer (Business Logic)        │
│  ┌──────────────────────────────────────────┐ │
│  │  Entities                                │ │
│  │  - Movie, TVShow, Episode                │ │
│  │  - PlaybackSession                       │ │
│  │  - User, Subscription                    │ │
│  ├──────────────────────────────────────────┤ │
│  │  Value Objects                           │ │
│  │  - Quality, StreamType                   │ │
│  │  - WatchStatus, ResumePoint              │ │
│  ├──────────────────────────────────────────┤ │
│  │  Domain Services                         │ │
│  │  - QualitySelector                       │ │
│  │  - ResumePointCalculator                 │ │
│  └──────────────────────────────────────────┘ │
└─────────────────┬──────────────────────────────┘
                  │
                  ↓
┌────────────────────────────────────────────────┐
│       Infrastructure Layer (External I/O)      │
│  ┌──────────────────────────────────────────┐ │
│  │  API Client                              │ │
│  │  - HTTP client with retry/auth          │ │
│  │  - Request/response mappers              │ │
│  ├──────────────────────────────────────────┤ │
│  │  Storage                                 │ │
│  │  - Settings repository                   │ │
│  │  - Cache manager                         │ │
│  ├──────────────────────────────────────────┤ │
│  │  Playback                                │ │
│  │  - Player adapter                        │ │
│  │  - InputStream helper                    │ │
│  └──────────────────────────────────────────┘ │
└────────────────────────────────────────────────┘
```

---

## Module Structure

```
addon/
├── addon.py                      # Entry point
├── addon.xml                     # Kodi addon manifest
├── resources/
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── domain/              # Domain layer
│   │   │   ├── __init__.py
│   │   │   ├── entities/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── content.py   # Movie, TVShow, Episode
│   │   │   │   ├── playback.py  # PlaybackSession
│   │   │   │   └── user.py      # User, Subscription
│   │   │   ├── value_objects/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── quality.py
│   │   │   │   └── watch_status.py
│   │   │   └── services/
│   │   │       ├── __init__.py
│   │   │       ├── quality_selector.py
│   │   │       └── resume_calculator.py
│   │   ├── application/         # Use cases
│   │   │   ├── __init__.py
│   │   │   ├── browse_content.py
│   │   │   ├── search_content.py
│   │   │   ├── play_video.py
│   │   │   ├── manage_bookmarks.py
│   │   │   └── track_watch_status.py
│   │   ├── infrastructure/      # External I/O
│   │   │   ├── __init__.py
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py
│   │   │   │   ├── auth.py
│   │   │   │   └── mappers.py
│   │   │   ├── storage/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── settings.py
│   │   │   │   └── cache.py
│   │   │   └── playback/
│   │   │       ├── __init__.py
│   │   │       ├── player.py
│   │   │       └── inputstream.py
│   │   ├── presentation/        # Kodi UI
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── content.py
│   │   │   │   ├── search.py
│   │   │   │   ├── playback.py
│   │   │   │   └── bookmarks.py
│   │   │   └── builders/
│   │   │       ├── __init__.py
│   │   │       └── list_item.py
│   │   └── shared/              # Cross-cutting
│   │       ├── __init__.py
│   │       ├── logging.py
│   │       ├── exceptions.py
│   │       └── types.py
│   ├── language/                # Localization
│   ├── media/                   # Icons
│   └── settings.xml             # Settings schema
└── tests/                       # Test suite
    ├── unit/
    ├── integration/
    └── fixtures/
```

---

## Domain Layer

### Entities

#### Movie Entity

```python
from dataclasses import dataclass
from typing import Optional, List
from .value_objects import Quality, WatchStatus, ResumePoint

@dataclass
class Movie:
    id: int
    title: str
    year: int
    plot: str
    rating: float
    genres: List[str]
    duration: int
    watch_status: WatchStatus
    resume_point: Optional[ResumePoint]
    available_qualities: List[Quality]
    
    def is_watched(self) -> bool:
        return self.watch_status.is_watched
    
    def should_resume(self) -> bool:
        return self.resume_point is not None and not self.is_watched()
```

#### TVShow Entity

```python
@dataclass
class TVShow:
    id: int
    title: str
    year: int
    seasons: List['Season']
    total_episodes: int
    new_episodes: int
    subscribed: bool
    
    def has_new_episodes(self) -> bool:
        return self.new_episodes > 0
    
    def get_season(self, number: int) -> Optional['Season']:
        return next((s for s in self.seasons if s.number == number), None)
```

#### Episode Entity

```python
@dataclass
class Episode:
    id: int
    title: str
    number: int
    season_number: int
    duration: int
    watch_status: WatchStatus
    resume_point: Optional[ResumePoint]
    available_qualities: List[Quality]
```

---

### Value Objects

#### Quality

```python
from enum import Enum
from dataclasses import dataclass

class QualityLevel(Enum):
    SD = "480p"
    HD = "720p"
    FULL_HD = "1080p"
    UHD = "2160p"

class StreamType(Enum):
    HLS = "hls"
    HLS2 = "hls2"
    HLS4 = "hls4"

@dataclass(frozen=True)
class Quality:
    level: QualityLevel
    stream_type: StreamType
    url: str
    
    def __lt__(self, other: 'Quality') -> bool:
        order = {QualityLevel.SD: 1, QualityLevel.HD: 2, 
                 QualityLevel.FULL_HD: 3, QualityLevel.UHD: 4}
        return order[self.level] < order[other.level]
```

#### WatchStatus

```python
@dataclass(frozen=True)
class WatchStatus:
    is_watched: bool
    watched_at: Optional[int]  # Unix timestamp
    
    @classmethod
    def unwatched(cls) -> 'WatchStatus':
        return cls(is_watched=False, watched_at=None)
    
    @classmethod
    def watched(cls, timestamp: int) -> 'WatchStatus':
        return cls(is_watched=True, watched_at=timestamp)
```

#### ResumePoint

```python
@dataclass(frozen=True)
class ResumePoint:
    position: int  # seconds
    duration: int  # total duration
    
    @property
    def percentage(self) -> float:
        return (self.position / self.duration) * 100 if self.duration > 0 else 0
    
    def should_clear(self, completion_threshold: float = 90.0) -> bool:
        return self.percentage >= completion_threshold
```

---

### Domain Services

#### QualitySelector

```python
from typing import List, Optional
from ..value_objects import Quality, QualityLevel, StreamType

class QualitySelector:
    def select_quality(
        self,
        available: List[Quality],
        preferred_level: QualityLevel,
        preferred_stream: StreamType
    ) -> Quality:
        # Try exact match
        exact = self._find_exact(available, preferred_level, preferred_stream)
        if exact:
            return exact
        
        # Fallback to best available
        return max(available, key=lambda q: q.level)
    
    def _find_exact(
        self,
        available: List[Quality],
        level: QualityLevel,
        stream: StreamType
    ) -> Optional[Quality]:
        return next(
            (q for q in available if q.level == level and q.stream_type == stream),
            None
        )
```

---

## Application Layer (Use Cases)

### BrowseContent Use Case

```python
from typing import List
from ..domain.entities import Movie, TVShow
from ..infrastructure.api import APIClient

class BrowseContentUseCase:
    def __init__(self, api_client: APIClient):
        self._api = api_client
    
    async def get_movies(
        self,
        category: str = "fresh",
        page: int = 1
    ) -> List[Movie]:
        response = await self._api.get_items(
            type="movie",
            category=category,
            page=page
        )
        return [self._map_to_movie(item) for item in response.items]
    
    async def get_tv_shows(
        self,
        category: str = "fresh",
        page: int = 1
    ) -> List[TVShow]:
        response = await self._api.get_items(
            type="serial",
            category=category,
            page=page
        )
        return [self._map_to_tvshow(item) for item in response.items]
```

### PlayVideo Use Case

```python
from ..domain.entities import Movie, Episode
from ..domain.services import QualitySelector
from ..infrastructure.playback import Player

class PlayVideoUseCase:
    def __init__(
        self,
        quality_selector: QualitySelector,
        player: Player
    ):
        self._selector = quality_selector
        self._player = player
    
    async def play_movie(self, movie: Movie, user_settings: dict):
        quality = self._selector.select_quality(
            movie.available_qualities,
            user_settings['quality_level'],
            user_settings['stream_type']
        )
        
        await self._player.play(
            url=quality.url,
            resume_point=movie.resume_point,
            metadata={
                'title': movie.title,
                'duration': movie.duration,
                'id': movie.id
            }
        )
```

---

## Infrastructure Layer

### API Client

```python
from typing import Optional
import aiohttp
from ..shared.exceptions import APIError, AuthenticationError

class APIClient:
    def __init__(self, base_url: str, auth_manager: 'AuthManager'):
        self._base_url = base_url
        self._auth = auth_manager
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def get_items(
        self,
        type: str,
        category: str,
        page: int = 1
    ) -> 'APIResponse':
        headers = await self._auth.get_headers()
        
        async with self._session.get(
            f"{self._base_url}/items/{category}",
            params={"type": type, "page": page},
            headers=headers
        ) as resp:
            if resp.status == 401:
                await self._auth.refresh_token()
                return await self.get_items(type, category, page)
            
            if resp.status != 200:
                raise APIError(f"API returned {resp.status}")
            
            data = await resp.json()
            return APIResponse.from_dict(data)
```

### Storage

```python
from typing import Optional
import json
from pathlib import Path

class SettingsRepository:
    def __init__(self, addon_id: str):
        self._addon = xbmcaddon.Addon(addon_id)
    
    def get_access_token(self) -> Optional[str]:
        token = self._addon.getSetting("access_token")
        return token if token else None
    
    def set_access_token(self, token: str):
        self._addon.setSetting("access_token", token)
    
    def get_user_preferences(self) -> dict:
        return {
            'quality_level': QualityLevel(self._addon.getSetting("video_quality")),
            'stream_type': StreamType(self._addon.getSetting("stream_type")),
            'ask_quality': self._addon.getSetting("ask_quality") == "true"
        }
```

---

## Presentation Layer

### Router

```python
from typing import Callable, Dict
import re

class Router:
    def __init__(self):
        self._routes: Dict[str, Callable] = {}
    
    def route(self, pattern: str):
        def decorator(func: Callable):
            self._routes[pattern] = func
            return func
        return decorator
    
    def dispatch(self, path: str, **kwargs):
        for pattern, handler in self._routes.items():
            match = re.match(pattern, path)
            if match:
                return handler(**match.groupdict(), **kwargs)
        
        raise RoutingError(f"No route for {path}")
```

### Route Handlers

```python
from ..application import BrowseContentUseCase
from .builders import ListItemBuilder

class ContentRoutes:
    def __init__(
        self,
        browse_use_case: BrowseContentUseCase,
        list_item_builder: ListItemBuilder
    ):
        self._browse = browse_use_case
        self._builder = list_item_builder
    
    async def show_movies(self, category: str = "fresh", page: int = 1):
        movies = await self._browse.get_movies(category, page)
        
        for movie in movies:
            list_item = self._builder.build_movie_item(movie)
            xbmcplugin.addDirectoryItem(
                handle=self._handle,
                url=self._build_url("play_movie", id=movie.id),
                listitem=list_item,
                isFolder=False
            )
        
        xbmcplugin.endOfDirectory(self._handle)
```

---

## Dependency Injection

### Container

```python
from dataclasses import dataclass

@dataclass
class AppContainer:
    # Infrastructure
    api_client: APIClient
    settings_repo: SettingsRepository
    player: Player
    
    # Domain Services
    quality_selector: QualitySelector
    
    # Use Cases
    browse_content: BrowseContentUseCase
    play_video: PlayVideoUseCase
    
    @classmethod
    def create(cls, addon_id: str) -> 'AppContainer':
        # Infrastructure
        settings_repo = SettingsRepository(addon_id)
        auth_manager = AuthManager(settings_repo)
        api_client = APIClient("https://api.service.kino.pub/v1", auth_manager)
        player = Player()
        
        # Domain Services
        quality_selector = QualitySelector()
        
        # Use Cases
        browse_content = BrowseContentUseCase(api_client)
        play_video = PlayVideoUseCase(quality_selector, player)
        
        return cls(
            api_client=api_client,
            settings_repo=settings_repo,
            player=player,
            quality_selector=quality_selector,
            browse_content=browse_content,
            play_video=play_video
        )
```

---

## Testing Strategy

### Unit Tests

```python
import pytest
from addon.domain.entities import Movie
from addon.domain.value_objects import WatchStatus, ResumePoint

def test_movie_should_resume_when_unwatched_with_resume_point():
    movie = Movie(
        id=1,
        title="Test Movie",
        watch_status=WatchStatus.unwatched(),
        resume_point=ResumePoint(position=100, duration=5400),
        # ... other fields
    )
    
    assert movie.should_resume() is True

def test_movie_not_resume_when_watched():
    movie = Movie(
        id=1,
        title="Test Movie",
        watch_status=WatchStatus.watched(1234567890),
        resume_point=ResumePoint(position=100, duration=5400),
        # ... other fields
    )
    
    assert movie.should_resume() is False
```

### Integration Tests

```python
import pytest
from addon.infrastructure.api import APIClient

@pytest.mark.asyncio
async def test_api_client_gets_movies(mock_api_server):
    client = APIClient(mock_api_server.url, auth_manager=MockAuth())
    
    response = await client.get_items(type="movie", category="fresh")
    
    assert len(response.items) > 0
    assert response.items[0]['type'] == "movie"
```

---

## Migration Strategy

### Phase 1: Core Framework
- Set up project structure
- Implement domain entities and value objects
- Create infrastructure adapters (API, storage, player)

### Phase 2: Basic Functionality
- Implement browse use cases
- Build simple UI with routes
- Test end-to-end movie playback

### Phase 3: Advanced Features
- TV show support with seasons
- Bookmarks and collections
- Search functionality

### Phase 4: Polish
- Error handling refinement
- Performance optimization
- Comprehensive testing

---

## Benefits Over Legacy

### Code Quality
- ✅ Type hints throughout (mypy validation)
- ✅ Comprehensive unit tests
- ✅ Clear separation of concerns
- ✅ No circular dependencies

### Maintainability
- ✅ Easy to locate and fix bugs
- ✅ Simple to add new features
- ✅ Refactoring-friendly architecture

### Robustness
- ✅ Explicit error handling
- ✅ Dependency injection for testing
- ✅ Async/await for concurrent operations

---

## Technology Stack

**Core:**
- Python 3.8+
- Type hints with mypy
- Dataclasses for immutability

**HTTP:**
- aiohttp (async HTTP client)
- urllib for OAuth (Kodi compatible)

**Testing:**
- pytest
- pytest-asyncio
- pytest-cov
- responses (HTTP mocking)

**Code Quality:**
- black (formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)

---

## Conclusion

This architecture provides:

1. **Clear Structure** - Easy to navigate and understand
2. **Testability** - Business logic isolated and testable
3. **Maintainability** - Single responsibility, loose coupling
4. **Extensibility** - Easy to add features without breaking existing code
5. **Type Safety** - Fewer runtime errors, better IDE support

**Next Steps:**
1. Create project skeleton
2. Implement domain layer (entities, value objects)
3. Build infrastructure adapters
4. Implement core use cases
5. Create presentation layer (routes)
6. Write comprehensive tests

**Estimated Effort:** 40-60 hours for MVP  
**Target:** Feature parity with v1.x but cleaner, more maintainable code
