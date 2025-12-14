# Routes Documentation

Complete routing specification for the kodi.kino.pub addon.

## Entry Point

**File:** `src/addon.py`

```python
from resources.lib.main import plugin

if __name__ == "__main__":
    plugin.run()
```

The main entry point imports the `plugin` singleton and calls `run()`, which dispatches to the appropriate route handler based on the URL path.

---

## Routing Architecture

**File:** `src/resources/lib/routing.py`

### Routing Class

The `Routing` class handles URL pattern matching and dispatch:

- **Pattern Matching**: Uses `UrlRule` class with regex-based matching
- **URL Building**: `build_url()` constructs plugin URLs
- **Icon Paths**: `build_icon_path()` resolves media file paths
- **Dispatch**: `dispatch()` matches path to handler and invokes with extracted parameters

### URL Pattern Syntax

```
<param_name>        - String parameter (matches [^/]+)
<string:param_name> - Explicit string parameter
<path:param_name>   - Path parameter (matches .*)
```

### URL Structure

```
plugin://video.kino.pub/<path>?<query_params>
```

Example: `plugin://video.kino.pub/items/movies/?page=2&sort=-rating`

---

## Route Inventory

Total routes: **34**

### Authentication Routes

#### `/login/`
- **Function:** `login()`
- **Line:** 84
- **Purpose:** Initiate OAuth device code flow
- **Parameters:** None
- **Returns:** None (shows auth dialog)
- **Implementation:** Calls `plugin.auth.get_token()`

#### `/reset_auth/`
- **Function:** `reset_auth()`
- **Line:** 89
- **Purpose:** Clear authentication tokens
- **Parameters:** None
- **Returns:** Container refresh
- **Implementation:** Clears access_token, access_token_expire, refresh_token from settings

---

### Main Navigation Routes

#### `/`
- **Function:** `index()`
- **Line:** 97
- **Purpose:** Main screen - display login or main menu
- **Parameters:** None
- **Returns:** Directory listing
- **Logic:**
  - If no access_token: Show "Activate device" option
  - Else: Show main menu items (from `plugin.main_menu_items`)
- **Menu Items:** Profile, Search, TV, Collections, Movies, Serials, TV Shows, Concerts, etc.

---

### Content Browsing Routes

#### `/items/<content_type>/`
- **Function:** `headings(content_type: str)`
- **Line:** 123
- **Purpose:** Show category navigation headings
- **Path Parameters:**
  - `content_type`: Content category (movies, serials, tvshows, concerts, documovies, docuserials, 3d, all)
- **Returns:** Directory with headings: search, fresh, hot, popular, alphabet, genres, sort
- **Query Parameters:** None

#### `/items/<content_type>/<heading>/`
- **Function:** `items(content_type: str, heading: str)`
- **Line:** 135
- **Purpose:** Display items for a specific heading/category
- **Path Parameters:**
  - `content_type`: Content category
  - `heading`: Navigation heading (fresh, hot, popular, sort, alphabet, genres, search)
- **Query Parameters:**
  - `page`: int (pagination)
  - `start_from`: int (for anime exclusion pagination)
  - Additional params from `plugin.kwargs`
- **Special Handling:**
  - `alphabet` → calls `alphabet(content_type)`
  - `genres` → calls `genres(content_type)`
  - `search` → calls `search(content_type)`
  - Others → API call to `items/{heading}` or `items` with sorting
- **Returns:** Item listing with pagination

#### `/items/<content_type>/genres/<genre>/`
- **Function:** `genre_items(content_type: str, genre: str)`
- **Line:** 174
- **Purpose:** Display items filtered by genre
- **Path Parameters:**
  - `content_type`: Content category
  - `genre`: Genre ID
- **Query Parameters:**
  - `page`: int (pagination)
  - Sorting params from `plugin.sorting_params`
- **API Call:** `items` with `type`, `genre`, and sorting params
- **Returns:** Item listing with pagination

#### `/items/<content_type>/alphabet/<letter>/`
- **Function:** `alphabet_items(content_type: str, letter: str)`
- **Line:** 201
- **Purpose:** Display items starting with specific letter
- **Path Parameters:**
  - `content_type`: Content category
  - `letter`: Letter (А-Я, A-Z)
- **Query Parameters:**
  - `page`: int (pagination)
  - `sort`: string (default: "title")
- **API Call:** `items` with `type`, `letter`, and sorting params
- **Returns:** Item listing with pagination

---

### Search Routes

#### `/new_search/<content_type>/`
- **Function:** `new_search(content_type: str)`
- **Line:** 210
- **Purpose:** Show keyboard input for new search
- **Path Parameters:**
  - `content_type`: Content category to search within
- **Returns:** Redirect to search results
- **Implementation:**
  1. Shows xbmc.Keyboard dialog
  2. Saves search term to history
  3. Redirects to `/search/<content_type>/results/?title=<query>`

#### `/search/<content_type>/`
- **Function:** `search(content_type: str)`
- **Line:** 223
- **Purpose:** Display search interface with history
- **Path Parameters:**
  - `content_type`: Content category
- **Returns:** Directory listing with "New search" option and search history
- **Implementation:** Shows recent searches from `plugin.search_history.recent`

#### `/search/<content_type>/results/`
- **Function:** `search_results(content_type: str)`
- **Line:** 239
- **Purpose:** Display search results
- **Path Parameters:**
  - `content_type`: Content category
- **Query Parameters:**
  - `title`: string (search query)
  - `page`: int (pagination)
  - Sorting params
- **API Call:** `items` with search query
- **Returns:** Item listing with pagination

#### `/clean_search_history/`
- **Function:** `clean_search_history()`
- **Line:** 251
- **Purpose:** Clear search history
- **Parameters:** None
- **Returns:** Container refresh after confirmation dialog

---

### TV/Live Channels Routes

#### `/tv/`
- **Function:** `tv()`
- **Line:** 156
- **Purpose:** Display live TV channels
- **Parameters:** None
- **API Call:** `tv/index`
- **Returns:** Directory listing of TV channels with stream URLs
- **Implementation:** Lists channels with logos and direct stream links

---

### Video Playback Routes

#### `/seasons/<item_id>/`
- **Function:** `seasons(item_id: str)`
- **Line:** 260
- **Purpose:** Display seasons for a TV show
- **Path Parameters:**
  - `item_id`: TV show item ID
- **Returns:** Directory listing of seasons
- **Implementation:** 
  - Instantiates TVShow from item_id
  - Lists all seasons from `tvshow.seasons`
  - Sets window property for playback data

#### `/episodes/<item_id>/`
- **Function:** `episodes(item_id: str)`
- **Line:** 270
- **Purpose:** Display episodes for multi-episode item
- **Path Parameters:**
  - `item_id`: Multi item ID
- **Returns:** Directory listing of episodes
- **Implementation:**
  - Instantiates Multi collection from item_id
  - Lists all videos from `collection.videos`
  - Sets window property for playback data

#### `/season_episodes/<item_id>/<season_number>/`
- **Function:** `season_episodes(item_id: str, season_number: str)`
- **Line:** 280
- **Purpose:** Display episodes for specific season
- **Path Parameters:**
  - `item_id`: TV show item ID
  - `season_number`: Season number (1-indexed)
- **Returns:** Directory listing of episodes
- **Implementation:**
  - Instantiates TVShow from item_id
  - Lists episodes from `tvshow.seasons[season_number-1].episodes`
  - Sets window property for playback data

#### `/play/<item_id>`
- **Function:** `play(item_id: str)`
- **Line:** 290
- **Purpose:** Resolve and play video
- **Path Parameters:**
  - `item_id`: Item ID to play
- **Query Parameters:**
  - `season_index`: int (for TV shows)
  - `index`: int (episode index)
- **Returns:** Resolved playable ListItem
- **Implementation:**
  1. Instantiates item from item_id
  2. Gets playable item (movie or specific episode)
  3. Creates Player with playable_list_item
  4. Monitors playback with marktime updates every 1 second

#### `/trailer/<item_id>`
- **Function:** `trailer(item_id: str)`
- **Line:** 303
- **Purpose:** Play item trailer
- **Path Parameters:**
  - `item_id`: Item ID
- **API Call:** `items/trailer` with item ID
- **Returns:** Resolved trailer URL
- **Implementation:** Extracts trailer URL from API response and plays

---

### Bookmarks Routes

#### `/bookmarks/`
- **Function:** `bookmarks()`
- **Line:** 312
- **Purpose:** Display bookmark folders
- **Parameters:** None
- **API Call:** `bookmarks`
- **Returns:** Directory listing
- **Implementation:**
  - Shows "Create folder" option
  - Lists all bookmark folders with folder-id and views properties
  - Context menu: Delete folder (remove_bookmarks_folder)

#### `/bookmarks/<folder_id>/`
- **Function:** `show_bookmark_folder(folder_id: str)`
- **Line:** 336
- **Purpose:** Display items in bookmark folder
- **Path Parameters:**
  - `folder_id`: Folder ID
- **Query Parameters:**
  - `page`: int (pagination)
- **API Call:** `bookmarks/{folder_id}`
- **Returns:** Item listing with pagination

#### `/edit_bookmarks/<item_id>`
- **Function:** `edit_bookmarks(item_id: str)`
- **Line:** 430
- **Purpose:** Add/remove item from bookmark folders
- **Path Parameters:**
  - `item_id`: Item ID
- **Parameters:** None
- **Returns:** None (shows multiselect dialog)
- **Implementation:**
  1. Gets current folders for item (`bookmarks/get-item-folders`)
  2. Gets all available folders (`bookmarks`)
  3. Shows multiselect dialog
  4. Computes folders to add/remove
  5. Calls `bookmarks/add` and `bookmarks/remove-item` as needed

#### `/remove_bookmarks_folder/<folder_id>`
- **Function:** `remove_bookmarks_folder(folder_id: str)`
- **Line:** 465
- **Purpose:** Delete bookmark folder
- **Path Parameters:**
  - `folder_id`: Folder ID to delete
- **API Call:** `bookmarks/remove-folder` POST
- **Returns:** Container refresh

#### `/create_bookmarks_folder`
- **Function:** `create_bookmarks_folder()`
- **Line:** 471
- **Purpose:** Create new bookmark folder
- **Parameters:** None
- **Returns:** Container refresh
- **Implementation:**
  1. Shows keyboard dialog for folder name
  2. Calls `bookmarks/create` POST with title
  3. Refreshes container

---

### Watching/Watchlist Routes

#### `/watching/`
- **Function:** `watching()`
- **Line:** 343
- **Purpose:** Display TV shows in watchlist
- **Parameters:** None
- **Returns:** Directory listing of subscribed TV shows
- **Implementation:** Lists items from `plugin.items.watching_tvshows`

#### `/watching_movies/`
- **Function:** `watching_movies()`
- **Line:** 351
- **Purpose:** Display movies in watching history
- **Parameters:** None
- **Returns:** Directory listing of movies
- **Implementation:** Lists items from `plugin.items.watching_movies`

#### `/toggle_watched/<item_id>`
- **Function:** `toggle_watched(item_id: str)`
- **Line:** 405
- **Purpose:** Mark item/episode as watched/unwatched
- **Path Parameters:**
  - `item_id`: Item ID
- **Query Parameters:**
  - `season`: int (optional, for TV shows)
  - `video`: int (optional, episode number)
- **API Calls:** 
  - `watching/toggle` to toggle watched status
  - `watching/marktime` to reset time to 0 if needed
- **Returns:** Container refresh

#### `/toggle_watchlist/<item_id>`
- **Function:** `toggle_watchlist(item_id: str)`
- **Line:** 416
- **Purpose:** Add/remove TV show from watchlist
- **Path Parameters:**
  - `item_id`: TV show ID
- **Query Parameters:**
  - `added`: int (0 or 1, current state)
- **API Call:** `watching/togglewatchlist`
- **Returns:** Popup notification and container refresh

---

### Collections Routes

#### `/collections/`
- **Function:** `collections()`
- **Line:** 363
- **Purpose:** Display collection sorting options
- **Parameters:** None
- **Returns:** Directory with sorting options (Fresh, Hot, Popular)

#### `/collections/<sorting>/`
- **Function:** `sorted_collections(sorting: str)`
- **Line:** 386
- **Purpose:** Display collections sorted by criteria
- **Path Parameters:**
  - `sorting`: Sort field (created, watchers, views)
- **Query Parameters:**
  - `page`: int (pagination)
- **API Call:** `collections/index` with `sort=-{sorting}`
- **Returns:** Collection listing with pagination

#### `/collection/<item_id>/`
- **Function:** `collection(item_id: str)`
- **Line:** 398
- **Purpose:** Display items in a collection
- **Path Parameters:**
  - `item_id`: Collection ID
- **API Call:** `collections/view` with collection ID
- **Returns:** Item listing

---

### User/Social Routes

#### `/profile/`
- **Function:** `profile()`
- **Line:** 483
- **Purpose:** Display user account information
- **Parameters:** None
- **API Call:** `user`
- **Returns:** None (shows dialog)
- **Implementation:** Shows dialog with username, registration date, subscription days

#### `/comments/<item_id>`
- **Function:** `comments(item_id: str)`
- **Line:** 498
- **Purpose:** Display kino.pub comments for item
- **Path Parameters:**
  - `item_id`: Item ID
- **API Call:** `items/comments`
- **Returns:** None (shows text viewer dialog)
- **Implementation:** Shows comments with ratings in text viewer

#### `/similar/<item_id>`
- **Function:** `similar(item_id: str)`
- **Line:** 520
- **Purpose:** Display similar items
- **Path Parameters:**
  - `item_id`: Item ID
- **Query Parameters:**
  - `title`: string (item title for empty state)
- **API Call:** `items/similar`
- **Returns:** Item listing or empty dialog
- **Implementation:** Shows similar items or "empty" dialog if none found

---

### Settings/Utility Routes

#### `/inputstream_helper_install/`
- **Function:** `install_inputstream_helper()`
- **Line:** 532
- **Purpose:** Install inputstreamhelper addon
- **Parameters:** None
- **Returns:** Popup notification
- **Implementation:** 
  - Checks if already installed
  - If not, triggers addon installation via `InstallAddon()`

#### `/inputstream_adaptive_settings/`
- **Function:** `inputstream_adaptive_settings()`
- **Line:** 542
- **Purpose:** Open inputstream.adaptive settings
- **Parameters:** None
- **Returns:** None (opens settings dialog)
- **Implementation:** Calls `xbmcaddon.Addon("inputstream.adaptive").openSettings()`

---

## URL Building Mechanisms

### `build_url(func_name, *args, **kwargs)`

**Location:** `routing.py:38-40`

Constructs plugin URLs:

```python
def build_url(self, func_name: str, *args, **kwargs) -> str:
    path = "/".join([func_name] + [str(arg) for arg in args])
    return urlunsplit(("plugin", self.plugin.PLUGIN_ID, path, urlencode(kwargs), ""))
```

**Usage Examples:**

```python
# Simple route
plugin.routing.build_url("login/")
# → plugin://video.kino.pub/login/

# With path parameters
plugin.routing.build_url("items", "movies", "hot/")
# → plugin://video.kino.pub/items/movies/hot/

# With query parameters
plugin.routing.build_url("search", "movies", "results/", title="matrix", page=2)
# → plugin://video.kino.pub/search/movies/results/?title=matrix&page=2

# With item ID
plugin.routing.build_url("play", item_id, season_index=1, index=3)
# → plugin://video.kino.pub/play/{item_id}?season_index=1&index=3
```

### `add_kwargs_to_url(**kwargs)`

**Location:** `routing.py:42-45`

Adds/updates query parameters on current URL:

```python
def add_kwargs_to_url(self, **kwargs) -> str:
    self.plugin.kwargs.update(kwargs)
    query_params = urlencode(self.plugin.kwargs)
    return urlunsplit(("plugin", self.plugin.PLUGIN_ID, self.plugin.path, query_params, ""))
```

**Usage:** Pagination - adds page parameter to current route

### `build_icon_path(name)`

**Location:** `routing.py:75-79`

Resolves icon paths:

```python
def build_icon_path(self, name: str) -> str:
    return xbmcvfs.translatePath(
        f"special://home/addons/{self.plugin.PLUGIN_ID}/resources/media/{name}.png"
    )
```

**Usage:** `plugin.routing.build_icon_path("search")` → `/path/to/addons/video.kino.pub/resources/media/search.png`

---

## Route Dispatch Mechanism

**Location:** `routing.py:63-73`

```python
def dispatch(self, path: str) -> None:
    for view_func, rules in self._rules.items():
        for rule in rules:
            kwargs = rule.match(path)
            if kwargs is not None:
                self.plugin.logger.debug(
                    f"Dispatching to '{view_func.__name__}', args: {kwargs}"
                )
                view_func(**kwargs)
                return
    raise RoutingException(f'No route to path "{path}"')
```

**Flow:**

1. Extracts path from `sys.argv[0]` in `plugin.run()`
2. Iterates through registered routes
3. Uses regex matching via `UrlRule.match()`
4. Extracts path parameters as kwargs
5. Invokes matched function with kwargs
6. Raises `RoutingException` if no match found

---

## Query Parameter Handling

Query parameters are available via `plugin.kwargs`:

```python
# In plugin.py __init__:
self.kwargs = dict(parse_qsl(sys.argv[2].lstrip("?")))
```

**Common Query Parameters:**

- `page`: int - Pagination page number
- `title`: str - Search query
- `sort`: str - Sort field
- `season_index`: int - Season index for playback
- `index`: int - Episode index for playback
- `video`: int - Video number
- `season`: int - Season number
- `start_from`: int - Anime exclusion pagination offset

---

## Route Parameter Types

### Path Parameters

Extracted from URL path using regex:

- `<content_type>` → `(?P<content_type>[^/]+?)` - matches string
- `<item_id>` → `(?P<item_id>[^/]+?)` - matches string
- `<folder_id>` → `(?P<folder_id>[^/]+?)` - matches string
- `<genre>` → `(?P<genre>[^/]+?)` - matches string
- `<letter>` → `(?P<letter>[^/]+?)` - matches string
- `<season_number>` → `(?P<season_number>[^/]+?)` - matches string
- `<sorting>` → `(?P<sorting>[^/]+?)` - matches string
- `<heading>` → `(?P<heading>[^/]+?)` - matches string

### Validation

**No explicit validation** in routing layer. Type conversion happens in handler functions.

**Content Type Values:**
- `all` - All content
- `movies` - Movies
- `serials` - TV series
- `tvshows` - TV shows
- `concerts` - Concerts
- `documovies` - Documentary movies
- `docuserials` - Documentary series
- `3d` - 3D content

---

## Special Route Behaviors

### Non-Directory Routes (Executable Actions)

These routes don't return directory listings:

- `/login/` - Shows auth dialog
- `/reset_auth/` - Executes action
- `/new_search/<content_type>/` - Shows keyboard, redirects
- `/clean_search_history/` - Shows confirmation, executes
- `/play/<item_id>` - Resolves video
- `/trailer/<item_id>` - Resolves trailer
- `/toggle_watched/<item_id>` - Toggles state
- `/toggle_watchlist/<item_id>` - Toggles state
- `/edit_bookmarks/<item_id>` - Shows dialog
- `/remove_bookmarks_folder/<folder_id>` - Executes action
- `/create_bookmarks_folder` - Shows keyboard, creates
- `/profile/` - Shows dialog
- `/comments/<item_id>` - Shows text viewer
- `/inputstream_helper_install/` - Triggers install
- `/inputstream_adaptive_settings/` - Opens settings

### Redirect Routes

- `/new_search/<content_type>/` redirects to `/search/<content_type>/results/`

---

## Route Dependencies

### Authentication Required

Most routes require `plugin.settings.access_token` to be set. Exception:

- `/` - Shows login option if no token
- `/login/` - Authentication flow
- `/reset_auth/` - Clears auth

### Conditional Routes

- Playback routes require instantiated items from API or window properties
- Edit/toggle routes require item IDs from previous navigation

---

## Summary

- **Total Routes:** 34
- **Entry Point:** `src/addon.py` → `plugin.run()`
- **Router Implementation:** `src/resources/lib/routing.py`
- **Route Definitions:** `src/resources/lib/main.py`
- **Pattern Syntax:** Flask-like with `<param>` placeholders
- **URL Scheme:** `plugin://video.kino.pub/<path>?<query>`
- **Dispatch:** Regex-based pattern matching with parameter extraction
- **Parameter Sources:** Path parameters (regex groups) + Query parameters (sys.argv[2])

---

## References

- **Entry Point:** `src/addon.py:2-6`
- **Router Class:** `src/resources/lib/routing.py:23-79`
- **UrlRule Class:** `src/resources/lib/routing.py:82-117`
- **Route Handlers:** `src/resources/lib/main.py:84-545`
- **Plugin Initialization:** `src/resources/lib/plugin.py:46-57`
