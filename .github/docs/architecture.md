# Architecture Documentation

Core modules, dependencies, and class hierarchies for the kodi.kino.pub addon.

## Module Inventory

**Location:** `src/resources/lib/`

Total: **13 modules** | **2,474 lines** | **31 classes**

### Core Modules

#### `plugin.py` (259 lines)
**Purpose:** Main plugin singleton and coordinator

**Classes:**
- `Plugin` - Central coordinator class

**Responsibilities:**
- Initialize all subsystems (auth, routing, logger, items, client, etc.)
- Parse sys.argv for URL and query parameters
- Provide singleton settings access
- Factory for ExtendedListItem creation
- Main menu item configuration
- Window property management for playback data

**Key Properties:**
- `PLUGIN_ID` (ClassVar) - Addon identifier from addon.xml
- `PLUGIN_URL` (ClassVar) - Plugin URL scheme
- `settings` (ClassVar) - Shared Settings instance
- `path` - Current URL path
- `handle` - Kodi plugin handle (int from sys.argv[1])
- `kwargs` - Query parameters from sys.argv[2]

**Dependencies:**
- `auth.Auth`
- `client.KinoPubClient`
- `routing.Routing`
- `logger.Logger`
- `modeling.ItemsCollection`
- `search_history.SearchHistory`
- `settings.Settings`
- `xbmc_settings.XbmcProxySettings`
- `xbmcaddon` (Kodi)

---

#### `main.py` (545 lines)
**Purpose:** Route handlers and view logic

**Classes:** None (pure functions)

**Functions:** 39 route handlers decorated with `@plugin.routing.route()`

**Responsibilities:**
- Define all route handlers
- Render items and pagination
- Coordinate between API, models, and UI
- Handle user interactions (search, bookmarks, watch status)

**Dependencies:**
- `plugin.Plugin` (singleton instance)
- `modeling` (ItemEntity, Multi, TVShow)
- `player.Player`
- `utils` (localize, popup_info)
- `xbmc*` modules for UI

**Key Functions:**
- `render_items()` - Display item listings
- `render_pagination()` - Add next page/home buttons
- `render_heading()` - Display category heading
- All route handlers (login, index, items, play, bookmarks, etc.)

---

#### `routing.py` (118 lines)
**Purpose:** URL routing and pattern matching

**Classes:**
- `RoutingException` ← Exception
- `Routing` - Route registration and dispatch
- `UrlRule` - Pattern matching and parameter extraction

**Responsibilities:**
- Register route patterns with handlers
- Match incoming URLs to patterns
- Extract path and query parameters
- Build plugin URLs
- Resolve icon paths
- Dispatch to appropriate handler

**Key Methods:**
- `route(pattern)` - Decorator for route registration
- `dispatch(path)` - Match and invoke handler
- `build_url()` - Construct plugin URLs
- `build_icon_path()` - Resolve media paths
- `UrlRule.match()` - Regex-based pattern matching

**Dependencies:**
- `re` for regex
- `urllib.parse` for URL encoding
- `xbmc`, `xbmcvfs` for Kodi paths

---

#### `modeling.py` (529 lines)
**Purpose:** Domain models and data entities

**Classes:** 9 classes in hierarchy

```
ItemEntity (base)
├── PlayableItem
│   ├── Movie
│   ├── Episode
│   └── SeasonEpisode
├── TVShow
├── Season
└── Multi

ItemsCollection (separate)
```

**Responsibilities:**
- Fetch items from API
- Transform API data to domain models
- Provide ListItem representations for Kodi
- Handle playback URL resolution
- Manage quality selection and stream types
- InputStream Adaptive integration

**Key Classes:**
- `ItemsCollection` - API interaction and instantiation factory
- `ItemEntity` - Base class with common properties (title, item_id, video_info, etc.)
- `PlayableItem` - Adds playback capabilities (media_url, quality selection, HLS)
- `Movie`, `Episode`, `SeasonEpisode` - Concrete playable types
- `TVShow` - Container for seasons
- `Season` - Container for episodes
- `Multi` - Multi-episode item container

**Dependencies:**
- `plugin.Plugin`
- `listitem.ExtendedListItem`
- `utils` (cached_property, natural_sort, localize, popup_warning)
- `urllib.parse` for URL manipulation
- `inputstreamhelper` (optional)
- `xbmcgui` for dialogs

---

#### `client.py` (209 lines)
**Purpose:** HTTP client and API communication

**Classes:**
- `KinoApiRequestProcessor` ← urllib.request.BaseHandler
- `KinoApiDefaultErrorHandler` ← urllib.request.HTTPDefaultErrorHandler
- `KinoApiErrorProcessor` ← urllib.request.HTTPErrorProcessor
- `KinoPubClient` - Main API client

**Responsibilities:**
- HTTP request handling
- Authorization header injection
- Proxy configuration (HTTP, SOCKS)
- Error handling (401, 429, others)
- Token refresh on 401
- Retry logic for 429
- JSON response parsing

**Key Methods:**
- `KinoPubClient.__call__(endpoint)` - Set endpoint for next request
- `KinoPubClient.get(data)` - GET request with query params
- `KinoPubClient.post(data)` - POST request with form data
- `KinoApiErrorProcessor.http_error_401()` - Auto token refresh
- `KinoApiErrorProcessor.http_error_429()` - Retry with backoff

**Dependencies:**
- `plugin.Plugin`
- `urllib.request`, `urllib.parse`, `urllib.error` for HTTP
- `http.client` for response handling
- `socks` for SOCKS proxy (via script.module.pysocks)
- `xbmc` for sleep

**Constants:**
- `TIMEOUT = 60` seconds

---

#### `auth.py` (231 lines)
**Purpose:** OAuth authentication and token management

**Classes:**
- `AuthException` ← Exception
- `AuthPendingException` ← AuthException
- `AuthExpiredException` ← AuthException
- `EmptyTokenException` ← AuthException
- `AuthDialog` - Progress dialog for device code flow
- `Auth` - OAuth device code implementation

**Responsibilities:**
- OAuth device code flow
- Device activation UI
- Token acquisition and refresh
- Token storage in settings
- Device info update (title, hardware, software)

**Key Methods:**
- `Auth.get_token()` - Main entry point (activate or refresh)
- `Auth._activate()` - Device code flow
- `Auth._get_device_code()` - Request user code
- `Auth._verify_device_code()` - Poll for authorization
- `Auth._get_device_token()` - Exchange code for tokens
- `Auth._refresh_token()` - Refresh access token
- `Auth._update_device_info()` - Send device metadata

**Constants:**
- `CLIENT_ID = "xbmc"`
- `CLIENT_SECRET = "cgg3gtifu46urtfp2zp1nqtba0k2ezxh"`
- `TIMEOUT = 60` seconds

**Dependencies:**
- `plugin.Plugin`
- `client.KinoApiRequestProcessor` for request handling
- `urllib.request` for OAuth API calls
- `utils` (cached_property, localize, popup_error)
- `xbmc`, `xbmcgui` for UI

---

#### `player.py` (108 lines)
**Purpose:** Video playback and state tracking

**Classes:**
- `Player` ← xbmc.Player

**Responsibilities:**
- Monitor playback events
- Track playback time (marktime)
- Determine watch status (watched/unwatched)
- Calculate resume points
- Send state updates to API (watching/marktime, watching/toggle)
- Token refresh if needed during long playback
- Trakt.tv scrobbling support

**Key Methods:**
- `onPlayBackStarted()` - Playback start event
- `onPlayBackStopped()` - Playback stop event (resume point logic)
- `onPlayBackEnded()` - Playback complete event (mark watched)
- `onPlaybackError()` - Error handling
- `set_marktime()` - Update current playback position

**Properties:**
- `should_make_resume_point` - Logic for resume point creation
- `should_mark_as_watched` - Logic based on percentage watched
- `should_reset_resume_point` - Logic for clearing resume
- `should_refresh_token` - Check if token expires during playback

**Dependencies:**
- `listitem.ExtendedListItem` (for properties)
- `xbmc`, `xbmcgui` for player and window properties

---

#### `listitem.py` (143 lines)
**Purpose:** Extended Kodi ListItem with addon-specific features

**Classes:**
- `ExtendedListItem` ← xbmcgui.ListItem

**Responsibilities:**
- Create Kodi ListItems with video metadata
- Set artwork (poster, fanart, thumbnail, icon)
- Set video info tags
- Add context menu items (watched, watchlist, bookmarks, comments, similar)
- Handle resume time calculation
- Mark items with adverts

**Context Menu Items:**
- Toggle watched/unwatched
- Add/remove from watchlist
- Edit bookmarks
- View comments
- Show similar items

**Dependencies:**
- `plugin.Plugin`
- `utils.localize`
- `xbmcgui.ListItem`

---

#### `settings.py` (74 lines)
**Purpose:** Addon settings management

**Classes:**
- `Settings`

**Responsibilities:**
- Read/write addon settings
- Provide typed property access to settings
- Handle authentication tokens
- Manage API URLs

**Key Properties:**
- `access_token`, `refresh_token`, `access_token_expire` - Auth tokens
- `video_quality` - Preferred quality (2160p, 1080p, 720p, 480p)
- `stream_type` - Stream format (hls, hls2, hls4)
- `ask_quality` - Show quality dialog (true/false)
- `mark_advert` - Mark items with ads (true/false)
- `exclude_anime` - Exclude anime from listings (true/false)
- `sort_by`, `sort_direction` - Default sorting
- `history_max_qty` - Search history limit
- Various `show_*` flags for menu visibility

**API URLs:**
- `api_url` - Main API endpoint
- `oauth_api_url` - OAuth endpoint

**Dependencies:**
- `xbmcaddon` for settings access

---

#### `logger.py` (59 lines)
**Purpose:** Logging and debugging

**Classes:**
- `Logger`

**Responsibilities:**
- Log messages at different levels (debug, info, warning, error, fatal)
- Format log messages with context
- Support Kodi log integration

**Log Levels:**
- `debug()` - Debug messages (disabled in production)
- `info()` - Informational messages
- `warning()` - Warning messages
- `error()` - Error messages
- `fatal()` - Fatal errors

**Dependencies:**
- `plugin.Plugin`
- `xbmc` for logging

---

#### `search_history.py` (47 lines)
**Purpose:** Search history persistence

**Classes:**
- `SearchHistory`

**Responsibilities:**
- Store recent search queries
- Retrieve recent searches
- Limit history size
- Clear all history

**Storage:** Uses window properties for persistence

**Dependencies:**
- `plugin.Plugin`
- `xbmcgui.Window`

---

#### `xbmc_settings.py` (102 lines)
**Purpose:** Kodi system settings access

**Classes:**
- `XbmcSettings` - Base class for JSON-RPC settings access
- `XbmcProxySettings` ← XbmcSettings - Proxy configuration

**Responsibilities:**
- Read Kodi system settings via JSON-RPC
- Parse proxy configuration
- Validate proxy settings
- Determine proxy type (HTTP, SOCKS4, SOCKS5)

**Proxy Properties:**
- `is_enabled` - Proxy enabled flag
- `type` - Proxy type (http, socks4, socks5, socks5r)
- `host`, `port` - Proxy server details
- `username`, `password` - Proxy credentials
- `is_http`, `is_socks`, `is_socks4`, `is_socks5` - Type checks
- `with_auth` - Requires authentication
- `is_correct` - Validation status

**Dependencies:**
- `plugin.Plugin`
- `xbmc` for JSON-RPC

---

#### `utils.py` (50 lines)
**Purpose:** Utility functions and helpers

**Classes:**
- `cached_property` - Property caching decorator

**Functions:**
- `localize(string_id)` - Get localized string
- `popup_info(message)` - Show info notification
- `popup_error(message)` - Show error notification
- `popup_warning(message)` - Show warning notification
- `natural_sort(items)` - Natural sorting for quality strings

**Dependencies:**
- `xbmcaddon` for localization
- `xbmcgui` for notifications

---

## Class Hierarchy Diagram

```
ItemEntity (modeling.py)
├── PlayableItem
│   ├── Movie - Single playable movie
│   ├── Episode - Single episode in Multi
│   └── SeasonEpisode - Episode in TV show season
├── TVShow - Container with seasons
├── Season - Container with episodes
└── Multi - Container with episodes (not in seasons)

ItemsCollection (modeling.py)
└── (Standalone) - Factory for ItemEntity instances

Plugin (plugin.py)
└── (Singleton) - Coordinator for all subsystems

Auth (auth.py)
└── (Instance per plugin) - OAuth device flow

AuthException (auth.py)
├── AuthPendingException - Authorization pending
├── AuthExpiredException - Token expired
└── EmptyTokenException - Missing token

KinoPubClient (client.py)
└── (Instance per plugin) - API communication

KinoApiRequestProcessor ← urllib.request.BaseHandler
└── Request preprocessing (auth, proxy)

KinoApiErrorProcessor ← urllib.request.HTTPErrorProcessor
└── Error handling (401, 429)

KinoApiDefaultErrorHandler ← urllib.request.HTTPDefaultErrorHandler
└── Default error handling

Player ← xbmc.Player
└── Playback monitoring and state tracking

ExtendedListItem ← xbmcgui.ListItem
└── Enhanced ListItem with context menus

Routing (routing.py)
└── Route registration and dispatch

UrlRule (routing.py)
└── Pattern matching

RoutingException ← Exception
└── Routing errors

Settings (settings.py)
└── Addon settings access

Logger (logger.py)
└── Logging facade

SearchHistory (search_history.py)
└── Search history management

XbmcSettings (xbmc_settings.py)
└── System settings access

XbmcProxySettings ← XbmcSettings
└── Proxy configuration

cached_property (utils.py)
└── Property caching decorator
```

---

## Dependency Graph

### Module Dependencies

```
main.py
├── plugin.Plugin (singleton)
├── modeling (ItemEntity, Multi, TVShow)
├── player.Player
├── utils (localize, popup_info)
└── xbmc* (UI modules)

plugin.py
├── auth.Auth
├── client.KinoPubClient
├── routing.Routing
├── logger.Logger
├── modeling.ItemsCollection
├── search_history.SearchHistory
├── settings.Settings
├── xbmc_settings.XbmcProxySettings
├── listitem.ExtendedListItem (factory)
└── xbmcaddon

modeling.py
├── plugin.Plugin
├── listitem.ExtendedListItem
├── utils (cached_property, natural_sort, localize, popup_warning)
├── inputstreamhelper (optional)
└── xbmcgui

client.py
├── plugin.Plugin
├── utils (localize, popup_error)
├── socks (from script.module.pysocks)
└── urllib.*

auth.py
├── plugin.Plugin
├── client.KinoApiRequestProcessor
├── utils (cached_property, localize, popup_error)
├── xbmc
└── xbmcgui

player.py
├── listitem.ExtendedListItem
├── xbmc
└── xbmcgui

routing.py
├── plugin.Plugin (type check only)
├── xbmc
└── xbmcvfs

listitem.py
├── plugin.Plugin
├── utils.localize
└── xbmcgui

settings.py
└── xbmcaddon

logger.py
├── plugin.Plugin
└── xbmc

search_history.py
├── plugin.Plugin
└── xbmcgui

xbmc_settings.py
├── plugin.Plugin
└── xbmc

utils.py
├── xbmcaddon
└── xbmcgui
```

### Circular Dependency Note

**Issue:** `plugin.Plugin` imports most modules, and those modules type-check against `Plugin`.

**Mitigation:** TYPE_CHECKING guard used in most modules:
```python
if TYPE_CHECKING:
    from resources.lib.plugin import Plugin
```

This allows type hints without runtime circular imports.

---

## External Dependencies

### Kodi Modules (Built-in)

- `xbmc` - Core Kodi functionality, player, logging
- `xbmcaddon` - Addon settings and localization
- `xbmcgui` - UI elements (dialogs, windows, listitems)
- `xbmcplugin` - Plugin functionality (directory listing, etc.)
- `xbmcvfs` - Virtual file system

### Python Standard Library

- `urllib.request`, `urllib.parse`, `urllib.error` - HTTP client
- `http.client` - HTTP response handling
- `json` - JSON parsing
- `re` - Regular expressions (routing)
- `sys` - System arguments
- `time` - Timestamps
- `typing` - Type hints
- `collections.namedtuple` - Simple data structures
- `datetime` - Date handling
- `platform` - System info
- `base64` - Encoding for proxy auth
- `socket` - Network operations

### External Add-ons

#### Required
- `script.module.pysocks` (version 1.7.0+)
  - Provides `socks` module for SOCKS proxy support
  - Used in `client.py` for proxy configuration

#### Optional
- `script.module.inputstreamhelper` (version 0.5.7+)
  - Provides `inputstreamhelper` module
  - Used in `modeling.py` for HLS playback via InputStream Adaptive
  - Gracefully handled if not available (try/except import)

- `inputstream.adaptive`
  - Not imported but configured via properties
  - Used for HLS/DASH streaming when enabled

---

## Global State and Singletons

### Singleton Pattern

**Plugin Instance:**
```python
# In main.py
from resources.lib.plugin import Plugin
plugin = Plugin()
```

This creates a module-level singleton that is:
- Instantiated once on addon start
- Reused across all route handlers
- Holds all state (auth, settings, routing, etc.)

### ClassVar Settings

```python
# In plugin.py
class Plugin:
    PLUGIN_ID: ClassVar[str] = xbmcaddon.Addon().getAddonInfo("id")
    PLUGIN_URL: ClassVar[str] = f"plugin://{PLUGIN_ID}"
    settings: ClassVar[Settings] = Settings()
```

These are shared across all Plugin instances (though only one exists).

### Window Properties

**Purpose:** Share data between navigation and playback

**Usage in Plugin:**
```python
def set_window_property(self, data: Dict[str, ItemEntity]):
    """Store serialized playback data in window property"""
    window = xbmcgui.Window(10000)
    window.setProperty(f"{PLUGIN_ID}-playback_data", pickle.dumps(data))

def get_window_property(self, item_id: str):
    """Retrieve item from window property by ID"""
    window = xbmcgui.Window(10000)
    data = window.getProperty(f"{PLUGIN_ID}-playback_data")
    if data:
        playback_data = pickle.loads(data)
        return playback_data.get(item_id)
```

**Data Stored:**
- Item entities for playback (Movie, TVShow, Multi)
- Prevents redundant API calls during navigation
- Cleared on playback start or manual clear

---

## Initialization Flow

1. **Addon Start** (`src/addon.py`)
   - Import `plugin` from `main.py`
   - Call `plugin.run()`

2. **Plugin Initialization** (`plugin.py.__init__`)
   - Parse sys.argv (path, handle, kwargs)
   - Instantiate Auth
   - Instantiate Logger
   - Instantiate Routing
   - Instantiate SearchHistory
   - Build main menu items
   - Instantiate ItemsCollection
   - Instantiate KinoPubClient
   - Instantiate XbmcProxySettings

3. **Route Dispatch** (`plugin.run()`)
   - Call `routing.dispatch(path)`
   - Match path to route
   - Extract parameters
   - Invoke handler function

4. **Handler Execution** (e.g., `index()`, `items()`, etc.)
   - Access plugin singleton
   - Make API calls via `plugin.client()`
   - Render items via `render_items()`
   - Return directory or resolved item

---

## Key Patterns

### Factory Pattern

**ItemsCollection** acts as factory for ItemEntity subtypes:

```python
def instantiate_from_item_data(self, item_data: Dict):
    cls = Multi if item_data.get("subtype") == "multi" else CONTENT_TYPE_MAP[item_data["type"]]
    return cls(parent=self, item_data=item_data)
```

### Decorator Pattern

**@plugin.routing.route()** registers routes:

```python
@plugin.routing.route("/items/<content_type>/")
def headings(content_type: str):
    ...
```

### Property Caching

**@cached_property** from utils:

```python
@cached_property
def watching_info(self) -> Dict:
    return self.plugin.client("watching").get(data={"id": self.item_id})
```

### Handler Chain (urllib.request)

Stacked handlers for HTTP requests:

```python
self.opener = urllib.request.build_opener(
    KinoApiRequestProcessor(self.plugin),    # 1. Add auth, proxy
    KinoApiErrorProcessor(self.plugin),      # 2. Handle 401, 429
    KinoApiDefaultErrorHandler(self.plugin), # 3. Handle others
)
```

---

## Module Coupling Analysis

### High Coupling
- `plugin.py` → All modules (coordinator)
- `main.py` → `plugin`, `modeling`, `player` (view layer)
- `modeling.py` → `plugin`, `listitem`, `utils` (domain layer)

### Medium Coupling
- `client.py` → `plugin`, `utils` (API layer)
- `auth.py` → `plugin`, `client`, `utils` (auth layer)
- `player.py` → `listitem` (playback layer)

### Low Coupling
- `routing.py` → `plugin` (type check only)
- `settings.py` → `xbmcaddon` (data layer)
- `logger.py` → `plugin`, `xbmc` (utility)
- `utils.py` → `xbmcaddon`, `xbmcgui` (utility)

---

## Summary

- **13 modules**, **31 classes**, **2,474 lines of code**
- **Singleton architecture** with centralized Plugin coordinator
- **Layered design**: Views (main.py) → Domain (modeling.py) → Data (client.py, auth.py)
- **Decorator-based routing** with regex pattern matching
- **Class hierarchy** for content types (ItemEntity → PlayableItem → Movie/Episode/etc.)
- **Handler chain** for HTTP error handling and retries
- **Window properties** for cross-navigation state sharing
- **Optional dependencies** gracefully handled (inputstreamhelper)
- **Type hints throughout** with TYPE_CHECKING guards to avoid circular imports

---

## References

- Module files: `src/resources/lib/*.py`
- Entry point: `src/addon.py`
- Settings schema: `src/resources/settings.xml`
- Dependencies: `src/addon.xml` (requires section)
