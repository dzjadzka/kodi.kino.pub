# Data Flow and State Management

Documentation of data flow patterns, state storage, and cache strategies in the kodi.kino.pub addon.

## Overview

The addon uses multiple layers for data flow and state persistence:

1. **Addon Settings** - Persistent configuration (xbmcaddon)
2. **Window Properties** - Temporary session state (xbmcgui.Window)
3. **API Layer** - Remote data fetching (KinoPubClient)
4. **Domain Models** - In-memory object graph (modeling.py)
5. **Kodi ListItems** - UI presentation layer

---

## Data Flow Diagrams

### 1. Browse Flow (User browsing content)

```
User Action
    ↓
Route Handler (main.py)
    ↓
Plugin.items.get(endpoint, data) ───→ KinoPubClient.get() ───→ kino.pub API
    ↓                                           ↓
ItemsCollection.instantiate_from_item_data()   API Response (JSON)
    ↓
ItemEntity subclass (Movie/TVShow/Multi)
    ↓
ItemEntity.list_item property
    ↓
ExtendedListItem (with video_info, artwork, context menus)
    ↓
xbmcplugin.addDirectoryItem()
    ↓
Kodi UI (Directory listing)
```

**Example:** User navigates to Movies → Fresh

```python
# Route: /items/movies/fresh/
def items(content_type='movies', heading='fresh'):
    data = {'type': 'movie'}
    response = plugin.items.get('items/fresh', data=data)  # API call
    # response.items = [Movie(...), Movie(...), ...]
    render_items(response.items, 'movies')
    render_pagination(response.pagination)
```

---

### 2. Search Flow

```
User Input (xbmc.Keyboard)
    ↓
SearchHistory.save(query)  ───→ Window Property (search_history)
    ↓
Redirect to /search/<type>/results/?title=<query>
    ↓
Plugin.items.get('items', data={'title': query})
    ↓
[Same as Browse Flow from API call onwards]
```

**Data Flow:**

1. User triggers `/new_search/movies/`
2. `xbmc.Keyboard().doModal()` shows input dialog
3. Query saved to SearchHistory
4. Redirect to `/search/movies/results/?title=<query>`
5. API call: `GET /items?type=movie&title=<query>`
6. Results rendered as items

**Search History Storage:**

```python
# In search_history.py
def save(self, title: str):
    history = self.recent  # Get from window property
    if title in history:
        history.remove(title)
    history.insert(0, title)
    history = history[:self.max_qty]  # Limit size
    window = xbmcgui.Window(10000)
    window.setProperty(
        f"{self.plugin.PLUGIN_ID}-search_history", 
        pickle.dumps(history)
    )
```

---

### 3. Playback Flow

```
User selects item to play
    ↓
/play/<item_id>?season_index=1&index=3
    ↓
Plugin.items.instantiate_from_item_id(item_id)
    ├─→ Check Window Property first (cache)
    └─→ If not found: API call GET /items/{item_id}
    ↓
Plugin.items.get_playable(item, season_index, index)
    ↓
PlayableItem.playable_list_item
    ├─→ PlayableItem.media_url (resolve video URL)
    │   ├─→ Select quality (settings or dialog)
    │   ├─→ Select stream type (hls/hls2/hls4)
    │   └─→ Add CDN location parameter
    ├─→ PlayableItem.hls_properties (InputStream Adaptive)
    └─→ ExtendedListItem (with path, properties, subtitles)
    ↓
Player(list_item)  ───→ xbmcplugin.setResolvedUrl()
    ↓
Kodi Player starts
    ↓
Player.onPlayBackStarted()
    ├─→ Clear window property
    ├─→ Refresh token if needed
    └─→ Set Trakt.tv property
    ↓
[Playback monitoring every 1 second]
Player.set_marktime()
    ↓
Player.onPlayBackStopped() / onPlayBackEnded()
    ├─→ Calculate resume point or watched status
    └─→ API call: watching/marktime or watching/toggle
```

**Window Property Cache:**

Before playback, items are cached in window property:

```python
# In main.py - seasons(), episodes(), season_episodes()
plugin.set_window_property({tvshow.item_id: tvshow})

# Later in /play/<item_id>
item = plugin.items.instantiate_from_item_id(item_id)
# ↓ Checks window property first:
def instantiate_from_item_id(self, item_id: str):
    item = self.plugin.get_window_property(item_id)  # Try cache
    if item:
        return item
    item_data = self.get_api_item(item_id)  # Fallback to API
    return self.instantiate_from_item_data(item_data)
```

**Purpose:** Avoid redundant API calls when user navigates TV Show → Season → Episode → Play

---

### 4. Authentication Flow

```
User navigates to /login/
    ↓
Auth.get_token()
    ├─→ If no access_token: Auth._activate()
    └─→ If has access_token: Auth._refresh_token()
    ↓
Device Code Flow (_activate):
    Auth._get_device_code() ───→ POST /oauth/device
        ↓
    (user_code, device_code, verification_uri)
        ↓
    AuthDialog shows code and URL
        ↓
    [User visits URL and enters code on external device]
        ↓
    Auth._verify_device_code() ───→ POST /oauth/device_token (polling)
        ↓
    (access_token, refresh_token, expires_in)
        ↓
    Auth._update_settings()
        ├─→ Settings.access_token = <token>
        ├─→ Settings.refresh_token = <token>
        └─→ Settings.access_token_expire = <timestamp>
        ↓
    Auth._update_device_info() ───→ POST /device/notify

Token Refresh (_refresh_token):
    POST /oauth/token with refresh_token
        ↓
    (new access_token, new refresh_token, expires_in)
        ↓
    Auth._update_settings() (same as above)
```

**Token Usage in API Calls:**

```python
# In client.py - KinoApiRequestProcessor.https_request()
request.add_header("Authorization", f"Bearer {self.plugin.settings.access_token}")
```

**Auto-Refresh on 401:**

```python
# In client.py - KinoApiErrorProcessor.http_error_401()
def http_error_401(self, request, ...):
    if request.recursion_counter_401 > 0:
        sys.exit()  # Prevent infinite loop
    request.recursion_counter_401 += 1
    self.plugin.auth.get_token()  # Refresh token
    return self.parent.open(request, timeout=TIMEOUT)  # Retry
```

---

### 5. Bookmarks Flow

```
User selects "Edit bookmarks" on item
    ↓
/edit_bookmarks/<item_id>
    ↓
GET /bookmarks/get-item-folders?item=<id> ───→ Current folders for item
GET /bookmarks ───→ All available folders
    ↓
xbmcgui.Dialog().multiselect(folders, preselect=current)
    ↓
User selects/deselects folders
    ↓
Compute diff:
    folders_to_add = selected - current
    folders_to_remove = current - selected
    ↓
For each folder to add:
    POST /bookmarks/add?item=<id>&folder=<folder_id>
For each folder to remove:
    POST /bookmarks/remove-item?item=<id>&folder=<folder_id>
    ↓
Popup notification
Container.Refresh
```

---

### 6. Watching/Watch Status Flow

```
User clicks "Mark as watched" context menu
    ↓
/toggle_watched/<item_id>?season=1&video=3
    ↓
GET /watching/toggle?id=<id>&season=1&video=3&status=1
    ↓
If video parameter present:
    GET /watching/marktime?id=<id>&season=1&video=3&time=0
    (Reset resume point to 0)
    ↓
Plugin.clear_window_property() (invalidate cache)
Container.Refresh
```

**Watching List:**

```
/watching/ (TV Shows) or /watching_movies/
    ↓
GET /watching/serials?subscribed=1  or  GET /watching/movies
    ↓
For each item_data:
    ItemsCollection.instantiate_from_item_id(item_data['id'])
    ↓
Render as directory listing
```

---

## Settings Storage and Access

### Settings Architecture

**Location:** xbmcaddon settings (persistent across sessions)

**Schema:** `src/resources/settings.xml` (246 lines)

**Access Layer:** `settings.py` - Typed property wrappers

### Settings Categories

#### 1. Authentication Settings

**Storage:** String settings (encrypted by Kodi)

```python
# In settings.py
@property
def access_token(self) -> str:
    return self.addon.getSetting("access_token")

@access_token.setter
def access_token(self, value: str):
    self.addon.setSetting("access_token", value)
```

**Settings:**
- `access_token` - JWT access token
- `refresh_token` - OAuth refresh token
- `access_token_expire` - Expiration timestamp (seconds since epoch)

**Lifecycle:**
- Set by: `Auth._update_settings()`
- Read by: `KinoApiRequestProcessor` for Authorization header
- Cleared by: `/reset_auth/` route
- Refreshed by: `Auth._refresh_token()` on expiry or 401

---

#### 2. Playback Settings

**User-configurable via settings dialog:**

```xml
<setting id="video_quality" type="string" default="1080p">
    <constraints>
        <options>
            <option>2160p</option>
            <option>1080p</option>
            <option>720p</option>
            <option>480p</option>
        </options>
    </constraints>
</setting>
```

**Settings:**
- `video_quality` - Preferred quality (2160p/1080p/720p/480p)
- `stream_type` - HLS variant (hls/hls2/hls4)
- `ask_quality` - Show quality selector dialog (boolean)
- `mark_advert` - Mark items with ads (boolean)
- `use_inputstream_adaptive` - Use InputStream Adaptive (boolean)
- `loc` - CDN location (ru/nl)

**Used in:**
```python
# In modeling.py - PlayableItem.media_url
desired_quality = self.plugin.settings.video_quality
desired_stream_type = self.plugin.settings.stream_type
ask_quality = self.plugin.settings.ask_quality

if ask_quality == "true":
    return self._get_media_url_from_dialog()  # Show quality selector
```

---

#### 3. UI/Menu Settings

**Control main menu visibility:**

```python
# In plugin.py
MainMenuItem(
    localize(32053),  # "Movies"
    self.routing.build_url("items", "movies/"),
    self.routing.build_icon_path("movies"),
    True,  # is_dir
    self.settings.show_movies,  # is_displayed (from settings)
)
```

**Settings:**
- `show_search`, `show_last`, `show_hot`, `show_popular`, `show_sort`
- `show_tv`, `show_collections`
- `show_movies`, `show_serials`, `show_tvshows`, `show_concerts`
- `show_3d`, `show_documovies`, `show_docuserials`

All default to `true`.

---

#### 4. Sorting Settings

**Default sort order:**

```python
@property
def sorting_params(self) -> Dict[str, str]:
    return {"sort": f"{self.settings.sort_by}{self.settings.sorting_direction_param}"}
```

**Settings:**
- `sort_by` - Field to sort by (updated/created/year/title/rating/kinopoisk_rating/imdb_rating/views/watchers)
- `sort_direction` - Sort direction (desc/asc)

**Used in:** API calls to `/items` with `sort=-rating` parameter

---

#### 5. Search History Settings

**Settings:**
- `history_max_qty` - Maximum search history entries (10/15/20)

**Storage:** Window property (see below)

---

### Settings Access Pattern

**Centralized access via Plugin.settings:**

```python
# ClassVar shared across instances
class Plugin:
    settings: ClassVar[Settings] = Settings()
```

**Usage throughout codebase:**

```python
if plugin.settings.access_token:
    # Authenticated
if plugin.settings.exclude_anime == "true":
    # Apply anime exclusion
quality = plugin.settings.video_quality
```

**Type coercion:** Most settings are strings, even booleans ("true"/"false")

---

## Window Property State

### Purpose

Temporary state storage within a Kodi session using Window(10000) properties.

**Advantages:**
- Fast access (no disk I/O)
- Session-scoped (cleared on restart)
- Can store complex objects (via pickle)

**Disadvantages:**
- Not persistent
- Memory-resident
- Requires serialization for complex types

### Playback Data Cache

**Location:** Window(10000) property `video.kino.pub-playback_data`

**Storage Format:** Pickled and base64-encoded dictionary

```python
def set_window_property(self, value: Dict) -> None:
    self.clear_window_property()
    pickled = codecs.encode(pickle.dumps(value), "base64").decode("utf-8")
    xbmcgui.Window(10000).setProperty("video.kino.pub-playback_data", pickled)

def get_window_property(self, item_id: str) -> Union[TVShow, Multi, Movie]:
    data = xbmcgui.Window(10000).getProperty("video.kino.pub-playback_data").encode("utf-8")
    items = pickle.loads(codecs.decode(data, "base64"))
    item = items.get(int(item_id), {})
    if item:
        item._plugin = self  # Restore plugin reference
    return item
```

**Data Stored:** Dictionary of `{item_id: ItemEntity}`

**Set by:**
- `/seasons/<item_id>/` - Stores TVShow
- `/episodes/<item_id>/` - Stores Multi
- `/season_episodes/<item_id>/<season_number>/` - Stores TVShow

**Retrieved by:**
- `/play/<item_id>` - Gets cached item to avoid API call
- `ItemsCollection.instantiate_from_item_id()` - Checks cache first

**Cleared by:**
- `Player.onPlayBackStarted()` - Clears after playback starts
- `/toggle_watched/`, `/toggle_watchlist/` - Clears on state changes

**Lifecycle:**

```
User navigates to TV Show
    ↓
/seasons/<item_id>/ sets window property {item_id: TVShow(...)}
    ↓
User navigates to Season
    ↓
/season_episodes/<item_id>/<season_number>/ reuses cached TVShow
    ↓
User clicks Play on Episode
    ↓
/play/<item_id> gets TVShow from cache (no API call!)
    ↓
Playback starts → Player.onPlayBackStarted() clears cache
```

---

### Search History

**Location:** Window(10000) property `video.kino.pub-search_history`

**Storage Format:** Pickled list of strings

```python
# In search_history.py
@property
def recent(self) -> List[str]:
    window = xbmcgui.Window(10000)
    data = window.getProperty(f"{self.plugin.PLUGIN_ID}-search_history")
    if data:
        return pickle.loads(codecs.decode(data.encode("utf-8"), "base64"))
    return []

def save(self, title: str):
    history = self.recent
    if title in history:
        history.remove(title)
    history.insert(0, title)  # Most recent first
    history = history[:self.max_qty]  # Limit size
    pickled = codecs.encode(pickle.dumps(history), "base64").decode("utf-8")
    window = xbmcgui.Window(10000).setProperty(
        f"{self.plugin.PLUGIN_ID}-search_history", pickled
    )
```

**Lifecycle:**
- Persists within a session
- Cleared on Kodi restart
- Limited by `settings.history_max_qty` (10/15/20)

---

### Trakt.tv Integration

**Location:** Window(10000) property `script.trakt.ids`

**Set by:** `Player.onPlayBackStarted()`

```python
def onPlayBackStarted(self) -> None:
    imdb_id = f"tt{int(self.list_item.getProperty('imdbnumber')):07d}"
    ids = json.dumps({"imdb": imdb_id})
    xbmcgui.Window(10000).setProperty("script.trakt.ids", ids)
```

**Purpose:** Provide item IDs to script.trakt addon for scrobbling

**Format:** JSON string `{"imdb": "tt0133093"}`

---

## Cache Strategies

### API Response Caching

**No explicit caching** of API responses to disk or memory.

**Implicit caching:**
1. Window property cache for navigation (see above)
2. Kodi's directory cache (`cacheToDisc` parameter)

**Directory Cache Control:**

```python
# In main.py
xbmcplugin.endOfDirectory(plugin.handle)  # Default: cacheToDisc=True
xbmcplugin.endOfDirectory(plugin.handle, cacheToDisc=False)  # For seasons/episodes
```

**When cache disabled:**
- `/seasons/<item_id>/` - Always fetch fresh
- `/episodes/<item_id>/` - Always fetch fresh
- `/season_episodes/<item_id>/<season_number>/` - Always fetch fresh
- `/similar/<item_id>` - Always fetch fresh

**Rationale:** These views show dynamic data (new episodes, watch status) that should be fresh.

---

### Cached Properties

**Pattern:** `@cached_property` decorator from utils.py

```python
class cached_property:
    def __init__(self, func):
        self.__doc__ = func.__doc__
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value
```

**Usage in modeling.py:**

```python
@cached_property
def watching_info(self) -> Dict:
    return self.plugin.client("watching").get(data={"id": self.item_id})

@cached_property
def seasons(self) -> List[Season]:
    # Expensive computation, cached after first access
    ...
```

**Scope:** Cached per object instance, lifetime of object

---

### Cache Invalidation

**Window Property:**
- Manual: `Plugin.clear_window_property()`
- Called after state changes (toggle watched, toggle watchlist)
- Called on playback start

**Kodi Directory Cache:**
- Invalidated by `Container.Refresh` calls
- Triggered after bookmarks changes, history clear, etc.

**Cached Properties:**
- Never explicitly invalidated
- Object lifecycle determines cache lifetime
- New object = fresh cache

**No LRU or TTL:** No time-based or size-based eviction strategies

---

## State Transitions

### Authentication State

```
[No Token] 
    ↓ /login/ (device code flow)
[Has Token, Not Expired]
    ↓ 401 error or manual refresh
[Has Token, Expired]
    ↓ refresh_token
[Has Token, Not Expired]
    ↓ /reset_auth/
[No Token]
```

### Watch Status State

```
[Unwatched, No Resume]
    ↓ User watches 30%
[Unwatched, Resume at 30%]
    ↓ User watches to 95%
[Watched, No Resume]
    ↓ User clicks "Mark as unwatched"
[Unwatched, No Resume]
```

**Thresholds:**
- Resume point: Between `ignoresecondsatstart` and `playcountminimumpercent`
- Watched: Above `playcountminimumpercent` (default 90%)

### Watchlist State

```
[Not in Watchlist]
    ↓ /toggle_watchlist/<id>?added=0
[In Watchlist]
    ↓ /toggle_watchlist/<id>?added=1
[Not in Watchlist]
```

---

## Data Persistence Summary

| Data Type | Storage | Lifetime | Format | Invalidation |
|-----------|---------|----------|--------|--------------|
| Settings | xbmcaddon | Permanent | Key-value strings | Manual edit or reset |
| Auth tokens | xbmcaddon settings | Until refresh/reset | Strings | Token expiry, /reset_auth/ |
| Playback cache | Window property | Session | Pickled objects | Playback start, state changes |
| Search history | Window property | Session | Pickled list | Manual clear, session end |
| API responses | None (no cache) | N/A | N/A | N/A |
| Directory cache | Kodi internal | Per navigation | Kodi format | Container.Refresh |
| Cached properties | Object instance | Object lifetime | Python objects | Object garbage collection |

---

## Summary

### Data Flow Characteristics

1. **Request-Response Pattern:** Most flows are synchronous HTTP requests to API
2. **Stateless Route Handlers:** Each route handler is independent, shares state via Plugin singleton
3. **Lazy Loading:** Items fetched on-demand, not pre-loaded
4. **Cache-Aside:** Window property cache checked before API call
5. **Event-Driven Playback:** Player events trigger API updates

### State Management Characteristics

1. **Centralized Settings:** Plugin.settings ClassVar for global config
2. **Session State:** Window properties for temporary data
3. **No Database:** No local SQLite or file-based storage
4. **Serialization:** Pickle used for complex object storage
5. **Simple Invalidation:** Manual clears, no automatic expiry

### Performance Optimizations

1. **Window Property Cache:** Reduces API calls during navigation
2. **Cached Properties:** Prevents redundant computations
3. **Kodi Directory Cache:** Reduces redundant route invocations
4. **Quality Fallback:** Graceful degradation if preferred quality unavailable

### Potential Issues

1. **Pickle Security:** Deserializing pickled data from window properties (trusted source)
2. **No Cache TTL:** Stale data possible if window property not cleared
3. **Memory Growth:** Window properties not size-limited
4. **Race Conditions:** No locking on window property access (single-threaded Kodi)

---

## References

- Settings storage: `src/resources/lib/settings.py`
- Window properties: `src/resources/lib/plugin.py:233-250`
- Search history: `src/resources/lib/search_history.py`
- Playback cache: `src/resources/lib/main.py:260-287`
- Player events: `src/resources/lib/player.py`
- Settings schema: `src/resources/settings.xml`
