# UI and Menu Structure

Complete menu hierarchy and navigation paths for the kodi.kino.pub addon.

## Overview

The addon uses a hierarchical directory structure with dynamic menu items based on:
- User authentication status
- Settings configuration (show_* flags)
- Content availability
- Navigation context

---

## Main Menu (Root `/`)

### Unauthenticated State

When `plugin.settings.access_token` is empty:

```
📂 Main Menu
└── 🔐 Activate device (/login/)
```

### Authenticated State

When user is logged in, main menu shows configured items:

```
📂 Main Menu
├── 👤 Profile (/profile/)                     [always shown]
├── 🔍 Search (/items/all/)                    [if show_search]
├── 📺 TV (/tv/)                               [if show_tv]
├── 📚 Collections (/collections/)             [if show_collections]
├── 🔄 By <sort> <direction> (/items/all/sort/) [if show_sort]
├── 🎬 Movies (/items/movies/)                 [if show_movies]
├── 📺 TV series (/items/serials/)             [if show_serials]
├── 📺 TV show (/items/tvshow/)                [if show_tvshows]
├── 🎭 3D (/items/3d/)                         [if show_3d]
├── 🎤 Concerts (/items/concerts/)             [if show_concerts]
├── 📽️ Documentary (/items/documovies/)        [if show_documovies]
├── 📺 Documentary series (/items/docuserials/) [if show_docuserials]
├── 🔖 Bookmarks (/bookmarks/)                 [always shown]
├── 👁️ I'm watching (/watching/)               [always shown]
└── 🎬 Watching movies (/watching_movies/)     [always shown]
```

**Settings Control:** Each menu item's visibility controlled by corresponding `show_*` setting.

---

## Content Type Menu Hierarchy

### Generic Content Type Structure

All content types (movies, serials, tvshows, etc.) share this navigation pattern:

```
/items/<content_type>/
├── 🔍 Search
│   ├── ➕ New search → (keyboard input)
│   ├── 📜 Recent search 1 → Results
│   ├── 📜 Recent search 2 → Results
│   └── ...
├── 🆕 Fresh → Item list
├── 🔥 Hot → Item list
├── ⭐ Popular → Item list
├── 🔤 Alphabet
│   ├── А → Items starting with А
│   ├── Б → Items starting with Б
│   ├── ... (all Cyrillic and Latin letters)
│   └── Z → Items starting with Z
├── 🎭 Genres
│   ├── Action → Items in genre
│   ├── Comedy → Items in genre
│   └── ... (all genres for content type)
└── 🔄 Sort → Sorted item list
```

### Content Types

1. **All** (`/items/all/`) - All content types mixed
2. **Movies** (`/items/movies/`) - Feature films
3. **TV series** (`/items/serials/`) - Multi-season shows
4. **TV shows** (`/items/tvshow/`) - Single shows/programs
5. **3D** (`/items/3d/`) - 3D content
6. **Concerts** (`/items/concerts/`) - Concert recordings
7. **Documentary** (`/items/documovies/`) - Documentary films
8. **Documentary series** (`/items/docuserials/`) - Documentary series

---

## Navigation Tree (Full Detail)

### 1. Profile Branch

```
/ → Profile (/profile/)
└── [Dialog showing account data]
    ├── User name
    ├── Registration date
    └── Subscription days remaining
```

**Route:** `/profile/`  
**UI Type:** Dialog (non-navigable)  
**Data:** User info from API `GET /user`

---

### 2. Search Branch

```
/ → Search (/items/all/)
└── All headings
    └── Search (/items/all/search/)
        ├── ➕ New search (/new_search/all/)
        │   └── [Keyboard dialog] → /search/all/results/?title=<query>
        │       └── 📄 Search results (with pagination)
        ├── 📜 Search history item 1 (/search/all/results/?title=<saved>)
        │   └── 📄 Results (with pagination)
        └── ... (up to history_max_qty items)
```

**Search History Actions:**
- Reset available via: Settings → Search history settings → Reset search history

---

### 3. TV (Live Channels) Branch

```
/ → TV (/tv/)
└── 📺 Channel 1 (direct stream URL)
    📺 Channel 2 (direct stream URL)
    ...
```

**Route:** `/tv/`  
**Data:** `GET /tv/index`  
**Items:** Direct playable streams (not directories)

---

### 4. Collections Branch

```
/ → Collections (/collections/)
├── 🆕 Fresh (/collections/created/)
│   └── 📚 Collection 1
│       Collection 2
│       ... (with pagination)
├── 🔥 Hot (/collections/watchers/)
│   └── [Same structure]
└── ⭐ Popular (/collections/views/)
    └── [Same structure]

Collection details (/collection/<id>/)
└── 🎬 Movie 1
    🎬 Movie 2
    ...
```

---

### 5. Content Items Branch

Using Movies as example (applies to all content types):

```
/ → Movies (/items/movies/)
├── 🔍 Search
│   └── [See Search Branch above]
├── 🆕 Fresh (/items/movies/fresh/)
│   └── 🎬 Movie 1 → Movie details
│       🎬 Movie 2 → Movie details
│       ...
│       ▶️ Next (if more pages)
│       🏠 Home
├── 🔥 Hot (/items/movies/hot/)
│   └── [Same structure]
├── ⭐ Popular (/items/movies/popular/)
│   └── [Same structure]
├── 🔤 Alphabet (/items/movies/alphabet/)
│   ├── А (/items/movies/alphabet/А/)
│   │   └── 🎬 Movies starting with А (with pagination)
│   ├── Б (/items/movies/alphabet/Б/)
│   └── ... (all letters)
├── 🎭 Genres (/items/movies/genres/)
│   ├── Genre selection page
│   │   ├── Action (/items/movies/genres/<genre_id>/)
│   │   │   └── 🎬 Action movies (with pagination)
│   │   ├── Comedy
│   │   └── ...
└── 🔄 By <sort> <direction> (/items/movies/sort/)
    └── 🎬 Sorted movies (with pagination)
```

---

### 6. Movie Item Details

When user selects a movie:

```
🎬 Movie Title
├── ▶️ Play (/play/<item_id>)
└── [Context Menu]
    ├── ✓ Mark as seen / Mark as unseen
    ├── 🔖 Change bookmarks
    ├── 💬 kino.pub comments
    ├── 🔗 Similar movies
    └── 🎬 Trailer (if available)
```

**Direct playback** if single video, or quality selection dialog if `ask_quality=true`.

---

### 7. TV Show Item Details

When user selects a TV show:

```
📺 TV Show Title
└── Seasons (/seasons/<item_id>/)
    ├── Season 1 (/season_episodes/<item_id>/1/)
    │   ├── 📺 S01E01 → Play
    │   ├── 📺 S01E02 → Play
    │   └── ...
    ├── Season 2 (/season_episodes/<item_id>/2/)
    └── ...

[Context Menu on show]
├── ⭐ Will watch / Won't watch (toggle watchlist)
├── ✓ Mark as seen / Mark as unseen
├── 🔖 Change bookmarks
├── 💬 kino.pub comments
└── 🔗 Similar movies
```

---

### 8. Multi-Episode Item Details

For items with multiple videos but no seasons:

```
📺 Multi Title
└── Episodes (/episodes/<item_id>/)
    ├── 📺 Episode 1 → Play
    ├── 📺 Episode 2 → Play
    └── ...

[Context Menu]
├── ✓ Mark as seen / Mark as unseen
├── 🔖 Change bookmarks
├── 💬 kino.pub comments
└── 🔗 Similar movies
```

---

### 9. Bookmarks Branch

```
/ → Bookmarks (/bookmarks/)
├── ➕ Make a folder (/create_bookmarks_folder)
│   └── [Keyboard dialog] → Creates folder
├── 📁 Folder 1 (/bookmarks/<folder_id>/)
│   ├── 🎬 Item 1
│   ├── 🎬 Item 2
│   └── ... (with pagination)
│   └── [Context Menu: Delete folder]
├── 📁 Folder 2
└── ...
```

**Folder Properties:**
- `folder-id` - Folder identifier
- `views` - Number of items in folder

---

### 10. Watching Branch

```
/ → I'm watching (/watching/)
└── 📺 Subscribed Show 1 (+<new_episodes>)
    📺 Subscribed Show 2 (+<new_episodes>)
    ...

[Shows with new episodes highlighted in yellow]

/ → Watching movies (/watching_movies/)
└── 🎬 Movie with resume point
    🎬 Movie with resume point
    ...
```

**Data Sources:**
- `/watching/` → `GET /watching/serials?subscribed=1`
- `/watching_movies/` → `GET /watching/movies`

---

## Context Menus

### Movie/Episode Context Menu

Available on playable items:

```
Context Menu (Right-click / Menu button)
├── ✓ Mark as seen / Mark as unseen (/toggle_watched/<item_id>?video=1)
├── 🔖 Change bookmarks (/edit_bookmarks/<item_id>)
│   └── [Multiselect dialog with folder checkboxes]
├── 💬 kino.pub comments (/comments/<item_id>)
│   └── [Text viewer with comments and ratings]
└── 🔗 Similar movies (/similar/<item_id>?title=<title>)
    └── Item list or empty dialog
```

### TV Show Context Menu

Additional item for shows:

```
Context Menu
├── ⭐ Will watch / Won't watch (/toggle_watchlist/<item_id>?added=0|1)
├── ✓ Mark as seen / Mark as unseen
├── 🔖 Change bookmarks
├── 💬 kino.pub comments
└── 🔗 Similar movies
```

### Season Context Menu

```
Context Menu
├── ✓ Mark as seen / Mark as unseen (/toggle_watched/<item_id>?season=1)
│   (Marks entire season)
└── [Other items inherited from show]
```

### Bookmark Folder Context Menu

```
Context Menu
└── 🗑️ Delete (/remove_bookmarks_folder/<folder_id>)
```

---

## Settings Menu

Accessed via: Kodi Settings → Add-ons → Video add-ons → kino.pub → Configure

### Settings Categories

```
⚙️ Settings
├── 📺 General
│   ├── Video Settings
│   │   ├── Video quality [2160p/1080p/720p/480p] (default: 1080p)
│   │   ├── Streaming type [hls/hls2/hls4] (default: hls4)
│   │   ├── CDN location [Russia/Netherlands] (default: Russia)
│   │   ├── Ask about video quality [toggle] (default: false)
│   │   ├── Mark videos with ads [toggle] (default: false)
│   │   └── Exclude anime [toggle] (default: false)
│   ├── InputStream Adaptive
│   │   ├── Use InputStream Adaptive [toggle] (default: false)
│   │   ├── Install InputStream helper [action button]
│   │   └── Configure InputStream Adaptive [action button]
│   ├── Sorting
│   │   ├── Sort by [dropdown: updated/created/year/title/rating/kinopoisk_rating/imdb_rating/views/watchers]
│   │   │   (default: rating)
│   │   └── Sort direction [desc/asc] (default: desc)
│   ├── Search history settings
│   │   ├── Search history entries [10/15/20] (default: 10)
│   │   └── Reset search history [action button]
│   └── Authentication
│       └── Reset auth [action button]
└── 📋 Main menu elements
    ├── Search [toggle] (default: true)
    ├── Fresh [toggle] (default: true)
    ├── Hot [toggle] (default: true)
    ├── Popular [toggle] (default: true)
    ├── Sorting [toggle] (default: true)
    ├── TV [toggle] (default: true)
    ├── Collections [toggle] (default: true)
    ├── Movies [toggle] (default: true)
    ├── TV series [toggle] (default: true)
    ├── TV show [toggle] (default: true)
    ├── 3D [toggle] (default: true)
    ├── Concerts [toggle] (default: true)
    ├── Documentary [toggle] (default: true)
    └── Documentary series [toggle] (default: true)
```

**Settings IDs:** Match settings.xml schema (e.g., `video_quality`, `show_movies`, etc.)

---

## Pagination

Pages with many items include pagination controls at the end:

```
[Item list]
...
├── ▶️ Next (if more pages available)
└── 🏠 Home (returns to /)
```

**Implementation:**
- `Next` button appears when `pagination.current + 1 <= pagination.total`
- Adds `page` query parameter to current URL
- For anime exclusion, includes `start_from` parameter

---

## Localization Strings

All UI strings are localized via `localize(string_id)`.

### Complete String Mapping

| ID | English | Usage |
|----|---------|-------|
| 32001 | Device activation | Auth dialog title |
| 32002 | Authentication error | Auth error popup |
| 32003 | Authentication failed | Auth failure popup |
| 32004 | Open | Auth instructions |
| 32005 | and enter the code | Auth instructions |
| 32006 | Server response status code | HTTP error prefix |
| 32007 | Try again | Retry message |
| 32008 | kino.pub does not respond | Connection error |
| 32009 | Won't watch | Remove from watchlist |
| 32010 | Will watch | Add to watchlist |
| 32011 | Mark as unseen | Context menu |
| 32012 | Mark as seen | Context menu |
| 32013 | Change bookmarks | Context menu |
| 32014 | kino.pub comments | Context menu |
| 32015 | Similar movies | Context menu |
| 32016 | Next | Pagination button |
| 32017 | Home | Pagination button |
| 32018 | Activate device | Login menu item |
| 32019 | Search | Menu/heading |
| 32020 | Fresh | Menu/heading |
| 32021 | Hot | Menu/heading |
| 32022 | Popular | Menu/heading |
| 32023 | Alphabet | Heading |
| 32024 | Genres | Heading |
| 32025 | New search | Search menu item |
| 32026 | Clean search history? | Confirmation dialog |
| 32027 | Trailer | Context menu |
| 32028 | Make a folder | Bookmarks menu item |
| 32029 | Delete | Context menu |
| 32030 | TV show has been added to the watchlist | Notification |
| 32031 | TV show has been removed from the watchlist | Notification |
| 32032 | Bookmarks folders | Dialog title |
| 32033 | Bookmarks have been changed | Notification |
| 32034 | Bookmarks folder name | Dialog title |
| 32035 | User name | Profile field |
| 32036 | Registration date | Profile field |
| 32037 | Subscription days remaining | Profile field |
| 32038 | Account data | Dialog title |
| 32039 | It's empty here | Empty state message |
| 32040 | Comments | Dialog title |
| 32042 | InputStream helper has been installed | Notification |
| 32043 | Choose video quality | Dialog title |
| 32044 | HLS stream is not supported | Warning |
| 32045 | ended | Status (past tense) |
| 32046 | on air | Status (live) |
| 32047 | Profile | Main menu |
| 32048 | Bookmarks | Main menu |
| 32049 | I'm watching | Main menu |
| 32050 | Watching movies | Main menu |
| 32051 | TV | Main menu |
| 32052 | Collections | Main menu |
| 32053 | Movies | Main menu |
| 32054 | TV series | Main menu |
| 32055 | TV show | Main menu |
| 32056 | Concerts | Main menu |
| 32057 | Documentary | Main menu |
| 32058 | Documentary series | Main menu |
| 32059 | last update | Sort option |
| 32060 | adding date | Sort option |
| 32061 | year | Sort option |
| 32062 | title | Sort option |
| 32063 | rating | Sort option |
| 32064 | Kinopoisk rating | Sort option |
| 32065 | views | Sort option |
| 32066 | watchers | Sort option |
| 32067 | desc | Sort direction |
| 32068 | asc | Sort direction |
| 32069 | General | Settings category |
| 32070 | Video quality | Setting label |
| 32071 | Streaming type | Setting label |
| 32072 | CDN location | Setting label |
| 32073 | Russia | CDN option |
| 32074 | Netherlands | CDN option |
| 32075 | Ask about video quality | Setting label |
| 32076 | Mark videos with ads | Setting label |
| 32077 | Exclude anime | Setting label |
| 32078 | InputStream Adaptive required | Settings group |
| 32079 | Use InputStream Adaptive | Setting label |
| 32080 | Install InputStream helper | Action button |
| 32081 | Sorting | Settings group / Menu heading |
| 32082 | Sort by | Setting label |
| 32083 | Sort direction | Setting label |
| 32084 | Search history settings | Settings group |
| 32085 | Search history entries | Setting label |
| 32086 | Reset search history | Action button |
| 32087 | Reset auth | Action button |
| 32088 | Main menu elements | Settings category |
| 32089 | By | Sort title prefix |
| 32090 | IMDB | Rating source |
| 32091 | 3D | Content type / Menu item |
| 32092 | Configure InputStream Adaptive | Action button |

**Language Files:**
- English: `src/resources/language/resource.language.en_gb/strings.po`
- Russian: `src/resources/language/resource.language.ru_ru/strings.po`
- Ukrainian: `src/resources/language/resource.language.uk_ua/strings.po`

---

## Icons and Media

**Location:** `src/resources/media/`

**Icon Naming:** `<name>.png` (e.g., `search.png`, `movies.png`)

**Used Icons (from code analysis):**
- `activate` - Device activation
- `profile` - User profile
- `search` - Search
- `search_history` - Search history items
- `fresh` - Fresh content
- `hot` - Hot content
- `popular` - Popular content
- `next_page` - Next page button
- `home` - Home button
- `tv` - TV channels
- `collections` - Collections
- `movies` - Movies
- `serials` - TV series
- `tvshows` - TV shows
- `3d` - 3D content
- `concerts` - Concerts
- `documovies` - Documentary films
- `docuserials` - Documentary series
- `bookmark` - Bookmark folder
- `create_bookmarks_folder` - Create folder action
- `sort` - Sorting
- `alphabet` - Alphabet navigation
- `genres` - Genres navigation

**Icon Resolution:** `plugin.routing.build_icon_path(name)` → `special://home/addons/video.kino.pub/resources/media/<name>.png`

---

## Navigation Patterns

### Breadcrumb Pattern

Navigation follows hierarchical breadcrumb:

```
/ → Content Type → Heading → Items → Item Details → Play
```

Example:
```
/ → Movies → Fresh → "The Matrix" → Play
/ → TV series → Alphabet → "F" → "Friends" → Season 1 → Episode 1 → Play
```

### Back Navigation

- Kodi handles back button automatically
- Each level returns to parent directory
- No explicit "Back" buttons in addon

### Refresh Pattern

Used after state changes:

```python
xbmc.executebuiltin("Container.Refresh")
```

Triggers:
- After toggle watched/unwatched
- After bookmark changes
- After folder creation/deletion
- After auth reset
- After search history clear

---

## UI State Indicators

### Resume Points

- Items with resume points show resume time in ListItem
- Playback resumes from saved position automatically

### Watch Status

- Watched items marked via playcount
- Visual indicator in Kodi (watched overlay)

### New Episodes

- Watchlist shows: `<title> : +<new_episodes>` in yellow color
- Example: `"Friends : +3"` (3 new episodes)

### Adverts

- Items with ads show `"<title> (!)"`  if `mark_advert=true`

### Empty States

- "It's empty here" (32039) shown when no results
- Examples: No similar movies, no comments

---

## Dialogs and Popups

### Keyboard Dialogs

- New search input
- Bookmark folder name input

### Multiselect Dialogs

- Edit bookmarks (select/deselect folders)

### Confirmation Dialogs

- Clean search history?

### Text Viewer Dialogs

- Comments display
- Similar movies (empty state)

### Info Dialogs

- Profile information (username, reg date, subscription days)

### Progress Dialogs

- Device activation (shows code and URL, polls for completion)

### Quality Selection Dialog

- Shown when `ask_quality=true`
- Lists available qualities
- User selects before playback

### Notifications/Popups

- "TV show has been added to the watchlist"
- "TV show has been removed from the watchlist"
- "Bookmarks have been changed"
- "InputStream helper has been installed"
- "HLS stream is not supported" (warning)
- Authentication errors
- HTTP errors

---

## Summary

### Menu Characteristics

- **Dynamic:** Based on auth status and settings
- **Hierarchical:** Multi-level navigation tree
- **Localized:** All strings support 3 languages (en/ru/uk)
- **Customizable:** Main menu items can be hidden via settings
- **Consistent:** Same navigation pattern across content types

### UI Patterns

- **Directory-based:** Uses Kodi's directory listing pattern
- **Context menus:** Right-click/menu for actions
- **Pagination:** Next/Home buttons for long lists
- **Dialogs:** For input, confirmation, and information display
- **Notifications:** Toast popups for feedback

### Navigation Features

- 34 routes covering all functionality
- Breadcrumb-style hierarchical navigation
- Deep linking support via plugin URLs
- Back button handled by Kodi
- Refresh on state changes

---

## References

- Main menu: `src/resources/lib/plugin.py:92-220`
- Route handlers: `src/resources/lib/main.py`
- Settings schema: `src/resources/settings.xml`
- Localization: `src/resources/language/*/strings.po`
- Icons: `src/resources/media/`
- Context menus: `src/resources/lib/listitem.py:56-122`
