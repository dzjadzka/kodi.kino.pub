# API Data Models and Response Structures

Complete documentation of API response formats and data models used in the kodi.kino.pub addon.

## Overview

**Response Format:** JSON  
**Encoding:** UTF-8  
**Content Type:** application/json

All API responses follow a consistent envelope structure with status codes and data payloads.

---

## Response Envelope Structure

### Standard Success Response

```json
{
  "status": 200,
  "items": [...],
  "pagination": {...}
}
```

**Fields:**
- `status` (int) - HTTP status code (200 = success)
- `items` (array) - Collection of items (for list endpoints)
- `item` (object) - Single item (for detail endpoints)
- `pagination` (object, optional) - Pagination metadata

### Single Item Response

```json
{
  "status": 200,
  "item": {...}
}
```

Used by endpoints like `/items/<id>`, `/watching`, `/user`

---

## Pagination Model

**Structure:**

```json
{
  "current": 1,
  "total": 50,
  "perpage": 50,
  "start_from": 100
}
```

**Fields:**
- `current` (int) - Current page number (1-indexed)
- `total` (int) - Total number of pages
- `perpage` (int) - Items per page (typically 50)
- `start_from` (int, optional) - Starting index for anime exclusion

**Usage:** `data_flow.md` documents pagination handling

**Code Reference:** `main.py:37-57` - `render_pagination()`

---

## Content Type Mapping

**Code:** `main.py:22-31`, `modeling.py:524-528`

```python
content_type_map = {
    "all": "tvshow",       # Mixed content
    "serial": "tvshow",    # TV series
    "docuserial": "tvshow",# Documentary series
    "tvshow": "tvshow",    # TV shows
    "concert": "musicvideo",# Concerts
    "3d": "movie",         # 3D movies
    "documovie": "movie",  # Documentary films
    "movie": "movie",      # Movies
}

CONTENT_TYPE_MAP = {
    "movie": Movie,
    "serial": TVShow,
    "tvshow": TVShow,
    "concert": Movie,
    "documovie": Movie,
    "docuserial": TVShow,
    "3d": Movie,
}
```

**Content Types:**
1. `movie` - Feature films
2. `serial` - Multi-season TV series
3. `tvshow` - TV shows/programs
4. `concert` - Concert recordings
5. `documovie` - Documentary films
6. `docuserial` - Documentary series
7. `3d` - 3D content
8. `all` - Mixed content

---

## Item Data Model

### Base Item Structure

All content items share this base structure:

```json
{
  "id": 123456,
  "type": "movie|serial|tvshow|concert|documovie|docuserial|3d",
  "subtype": "multi",
  "title": "The Matrix",
  "year": 1999,
  "rating": 8.5,
  "rating_votes": 150000,
  "kinopoisk_rating": 8.0,
  "kinopoisk": 8.0,
  "imdb_rating": 8.7,
  "imdb": "0133093",
  "plot": "A computer hacker learns about the true nature of reality...",
  "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
  "director": "Lana Wachowski, Lilly Wachowski",
  "genres": [
    {"id": 1, "title": "Action"},
    {"id": 2, "title": "Sci-Fi"}
  ],
  "countries": [
    {"id": 1, "title": "USA"}
  ],
  "poster": "https://...",
  "posters": {
    "small": "https://.../small.jpg",
    "medium": "https://.../medium.jpg",
    "big": "https://.../big.jpg",
    "wide": "https://.../wide.jpg"
  },
  "advert": false,
  "in_watchlist": 0,
  "subscribed": false,
  "new": 0,
  "watching": {
    "status": 0,
    "time": 0,
    "duration": 5400
  },
  "created_at": 1234567890,
  "updated_at": 1234567890,
  "trailer": [...],
  "videos": [...],
  "seasons": [...]
}
```

### Field Descriptions

#### Identifiers
- `id` (int) - Unique item identifier
- `type` (string) - Content type
- `subtype` (string, optional) - "multi" for multi-episode items

#### Metadata
- `title` (string) - Title
- `year` (int) - Release year
- `plot` (string) - Description/synopsis
- `cast` (string) - Comma-separated actor names
- `director` (string) - Director name(s)

#### Ratings
- `rating` (float) - Combined/average rating
- `rating_votes` (int) - Number of votes
- `kinopoisk_rating` (float) - Kinopoisk rating (Russian film database)
- `kinopoisk` (float) - Alias for kinopoisk_rating
- `imdb_rating` (float) - IMDB rating
- `imdb` (string) - IMDB ID (without "tt" prefix)

#### Classification
- `genres` (array) - Genre objects `[{id, title}]`
- `countries` (array) - Country objects `[{id, title}]`

#### Artwork
- `poster` (string, deprecated) - Legacy poster URL
- `posters` (object) - Multi-size poster URLs
  - `small` - Small thumbnail
  - `medium` - Medium size
  - `big` - Large poster
  - `wide` - Widescreen/fanart

#### Flags
- `advert` (boolean) - Has advertisements
- `in_watchlist` (int) - In user's watchlist (0/1)
- `subscribed` (boolean) - Subscribed to (for TV shows)
- `new` (int) - Number of new unwatched episodes

#### Watch Status
- `watching` (object) - Watch progress
  - `status` (int) - 0=unwatched, 1=watched
  - `time` (int) - Resume position (seconds)
  - `duration` (int) - Total duration (seconds)

#### Timestamps
- `created_at` (int) - Creation timestamp (Unix epoch)
- `updated_at` (int) - Last update timestamp

#### Media
- `trailer` (array, optional) - Trailer objects
- `videos` (array) - Video files (for movies, multi-episode)
- `seasons` (array) - Seasons (for TV shows)

---

## Video File Structure

### Video Object

```json
{
  "id": 789,
  "title": "Episode 1: Pilot",
  "number": 1,
  "snumber": 1,
  "thumbnail": "https://.../thumb.jpg",
  "duration": 1440,
  "advert": false,
  "watching": {
    "status": 0,
    "time": 0,
    "duration": 1440
  },
  "files": [
    {
      "quality": "1080p",
      "url": {
        "hls": "https://.../index.m3u8",
        "hls2": "https://.../index.m3u8",
        "hls4": "https://.../master.m3u8"
      }
    },
    {
      "quality": "720p",
      "url": {
        "hls": "https://.../index.m3u8",
        "hls2": "https://.../index.m3u8",
        "hls4": "https://.../master.m3u8"
      }
    },
    {
      "quality": "480p",
      "url": {...}
    }
  ],
  "subtitles": [
    {
      "lang": "eng",
      "url": "https://.../subtitles_en.srt"
    },
    {
      "lang": "rus",
      "url": "https://.../subtitles_ru.srt"
    }
  ]
}
```

### Fields

#### Video Metadata
- `id` (int) - Video identifier
- `title` (string) - Episode/video title
- `number` (int) - Episode number within season/series
- `snumber` (int) - Season number (for TV shows)
- `thumbnail` (string) - Thumbnail URL
- `duration` (int) - Duration in seconds

#### Files Array
Array of quality/URL combinations:
- `quality` (string) - Quality level
  - `"2160p"` - 4K UHD
  - `"1080p"` - Full HD
  - `"720p"` - HD
  - `"480p"` - SD
- `url` (object) - Streaming URLs by type
  - `hls` - HTTP Live Streaming (basic)
  - `hls2` - HLS variant 2
  - `hls4` - HLS variant 4 (typically MPEG-DASH)

#### Subtitles Array
- `lang` (string) - Language code (eng, rus, etc.)
- `url` (string) - Subtitle file URL (.srt format)

---

## TV Show Structure

### Season Object

```json
{
  "number": 1,
  "watching": {
    "status": 0,
    "time": 0,
    "duration": 0
  },
  "episodes": [
    {
      "id": 1001,
      "title": "S01E01: Pilot",
      "number": 1,
      "snumber": 1,
      "thumbnail": "https://...",
      "watching": {
        "status": 0,
        "time": 0,
        "duration": 1440
      },
      "files": [...],
      "subtitles": [...]
    },
    ...
  ]
}
```

### Fields

- `number` (int) - Season number (1-indexed)
- `watching` (object) - Aggregated watch status for season
- `episodes` (array) - Episode objects (same structure as Video Object)

### Episode Numbering

- `number` - Episode number within season (1, 2, 3, ...)
- `snumber` - Season number (1, 2, 3, ...)
- Title format: `"S{snumber:02d}E{number:02d}: {title}"`
  - Example: "S01E05: The One with the East German Laundry Detergent"

---

## Multi-Episode Structure

For items with `subtype: "multi"`:

```json
{
  "id": 123,
  "type": "movie",
  "subtype": "multi",
  "title": "Lord of the Rings Extended Edition",
  "videos": [
    {
      "id": 1,
      "title": "Part 1: The Fellowship of the Ring",
      "number": 1,
      "files": [...],
      "subtitles": [...]
    },
    {
      "id": 2,
      "title": "Part 2: The Two Towers",
      "number": 2,
      "files": [...],
      "subtitles": [...]
    },
    ...
  ]
}
```

**Difference from TV Shows:** No seasons, flat video list

---

## Model Class Hierarchy

### Python Classes

**Location:** `modeling.py:149-529`

```
ItemEntity (base class)
├── PlayableItem (adds playback capabilities)
│   ├── Movie - Single playable movie
│   ├── Episode - Episode in Multi item
│   └── SeasonEpisode - Episode in TV show season
├── TVShow - Container with seasons
├── Season - Container with episodes
└── Multi - Container with episodes (no seasons)
```

### ItemEntity (Base Class)

**Code:** `modeling.py:149-230`

**Properties:**
- `item_id` - From `item["id"]`
- `title` - From `item["title"]`
- `plot` - Formatted with ratings
- `video_info` - Kodi video info dict
- `trailer_url` - Trailer route URL
- `watching_info` - API watching data (cached)
- `list_item` - ExtendedListItem for Kodi

**video_info Structure:**

```python
{
    "year": int,
    "genre": "Action, Sci-Fi",  # Comma-separated
    "rating": float,  # IMDB or Kinopoisk
    "cast": ["Actor 1", "Actor 2", ...],
    "director": "Director Name",
    "plot": "Formatted plot with ratings",
    "title": "Title",
    "imdbnumber": "0133093",  # IMDB ID
    "votes": int,
    "country": "USA, UK",  # Comma-separated
}
```

### PlayableItem (Playback Class)

**Code:** `modeling.py:232-332`

**Additional Properties:**
- `video_data` - Video object from API
- `media_url` - Resolved playback URL
- `hls_properties` - InputStream Adaptive props
- `playable_list_item` - ListItem with playback path

**Quality Selection Logic:**

```python
# From modeling.py:269-282
desired_quality = self.plugin.settings.video_quality  # "1080p"
desired_stream_type = self.plugin.settings.stream_type  # "hls4"

if ask_quality == "true":
    # Show dialog
    return self._get_media_url_from_dialog()

files = {file_["quality"]: file_["url"] for file_ in self.video_data["files"]}
try:
    return files[desired_quality][desired_stream_type]
except KeyError:
    # Fallback to highest quality
    return files[natural_sort(list(files.keys()))[-1]][desired_stream_type]
```

**CDN Location:** Adds `?loc=ru` or `?loc=nl` query parameter

### Movie Class

**Code:** `modeling.py:490-529`

**video_info Additions:**
- `mediatype`: "movie"
- `playcount`: From `watching["status"]`
- `duration`: From `videos[0]["duration"]`
- `time`: Resume time from `watching["time"]`

**video_data:** Returns `item["videos"][0]` (first video)

### TVShow Class

**Code:** `modeling.py:334-366`

**Properties:**
- `seasons` - List of Season objects
- `is_in_watchlist` - Boolean from `item.get("from_watching")` or `subscribed`

**Title Format (if in watchlist):**
```python
f"{self.title} : [COLOR FFFFF000]+{self.item['new']}[/COLOR]"
# Example: "Friends : +3" (3 new episodes)
```

**video_info:**
- `mediatype`: "tvshow"
- `tvshowtitle`: Title
- `playcount`: Based on all episodes watched

### Season Class

**Code:** `modeling.py:368-397`

**Properties:**
- `season_number` - From `season_data["number"]`
- `episodes` - List of SeasonEpisode objects

**Title Format:**
```python
f"{localize(32045)} {self.season_number}" if ended else 
f"{localize(32046)} {self.season_number}"
# "ended Season 1" or "on air Season 1"
```

### SeasonEpisode Class

**Code:** `modeling.py:399-436`

**video_info Additions:**
- `mediatype`: "episode"
- `episode`: Episode number
- `season`: Season number
- `tvshowtitle`: TV show title

**Properties:**
- `season_number`, `video_number` - From video data

### Multi Class

**Code:** `modeling.py:438-456`

**Structure:** Similar to TVShow but no seasons

**videos Property:** List of Episode objects (flat, no seasons)

### Episode Class

**Code:** `modeling.py:458-488`

**video_info:**
- `mediatype`: "episode"
- `episode`: Video number
- `tvshowtitle`: Parent title

**video_data:** From parent's videos array

---

## Error Response Format

### Standard Error

```json
{
  "error": "error_code",
  "error_description": "Human readable message"
}
```

**Common Error Codes:**
- `authorization_pending` - Auth not complete (400)
- `code_expired` - Device code expired (400)
- `authorization_expired` - Refresh token expired (400)
- `invalid_refresh_token` - Invalid refresh token (400)

**HTTP Status Codes:**
- 200 - Success
- 400 - Bad request / Auth errors
- 401 - Unauthorized (triggers auto refresh)
- 429 - Too many requests (triggers retry)
- 5xx - Server errors

---

## Special Responses

### User Response

**Endpoint:** `GET /user`

```json
{
  "status": 200,
  "user": {
    "id": 123,
    "username": "user@example.com",
    "email": "user@example.com",
    "reg_date": 1234567890,
    "subscription": {
      "active": true,
      "days": 365,
      "end_time": 1234567890
    },
    "profile": {
      "name": "User Name"
    }
  }
}
```

**Usage:** Profile dialog (`main.py:485`)

### TV Channels Response

**Endpoint:** `GET /tv/index`

```json
{
  "status": 200,
  "channels": [
    {
      "id": 1,
      "title": "Channel 1",
      "stream": "https://.../stream.m3u8",
      "logos": {
        "s": "https://.../logo_s.png",
        "m": "https://.../logo_m.png",
        "l": "https://.../logo_l.png"
      }
    },
    ...
  ]
}
```

**Usage:** TV channels list (`main.py:158`)

### Comments Response

**Endpoint:** `GET /items/comments?id=<id>`

```json
{
  "status": 200,
  "item": {
    "id": 123,
    "title": "The Matrix"
  },
  "comments": [
    {
      "user": {
        "id": 456,
        "name": "UserName",
        "avatar": "https://..."
      },
      "message": "Great movie!",
      "rating": 5,
      "created_at": 1234567890
    },
    ...
  ]
}
```

**Usage:** Comments dialog (`main.py:500`)

**Rating Display:**
- Positive (>0): Green `(+5)`
- Negative (<0): Red `(-2)`
- Neutral (0): No color

### Trailer Response

**Endpoint:** `GET /items/trailer?id=<id>`

```json
{
  "status": 200,
  "trailer": [
    {
      "url": "https://.../trailer.mp4",
      "quality": "1080p",
      "duration": 120
    }
  ]
}
```

**Usage:** Trailer playback (`main.py:305`)

### Genres Response

**Endpoint:** `GET /genres?type=movie`

```json
{
  "status": 200,
  "items": [
    {"id": 1, "title": "Action"},
    {"id": 2, "title": "Comedy"},
    {"id": 3, "title": "Drama"},
    ...
  ]
}
```

**Usage:** Genre selection (`main.py:166`)

---

## Data Transformation

### API → Python Model

**Code:** `modeling.py:80-86`

```python
def instantiate_from_item_data(
    self, item_data: Dict, index: Optional[int] = None
) -> Union["TVShow", "Multi", "Movie"]:
    cls = Multi if item_data.get("subtype") == "multi" else CONTENT_TYPE_MAP[item_data["type"]]
    return cls(parent=self, item_data=item_data, index=index)
```

**Mapping:**
- `type: "movie"` → `Movie`
- `type: "serial"` → `TVShow`
- `type: "tvshow"` → `TVShow`
- `type: "concert"` → `Movie`
- `subtype: "multi"` → `Multi` (overrides type)

### Python Model → Kodi ListItem

**Code:** `modeling.py:205-218`

```python
@property
def list_item(self) -> ExtendedListItem:
    li = self.plugin.list_item(
        name=getattr(self, "li_title", self.title),
        poster=self.item.get("posters", {}).get("big"),
        fanart=self.item.get("posters", {}).get("wide"),
        thumbnailImage=self.item.get("thumbnail", self.item.get("posters", {}).get("small", "")),
        properties={"id": self.item_id, **self.properties},
        video_info=self.video_info,
        addContextMenuItems=True,
    )
    li.markAdvert(self.item.get("advert", False))
    return li
```

**Kodi Properties Set:**
- `id` - Item ID
- `isPlayable` - For playable items
- `folder-id` - For bookmark folders
- `views` - For bookmark folders
- Plus model-specific properties

---

## Field Validation and Fallbacks

### Optional Fields

Many fields are optional in the API response. The code handles missing fields:

```python
# Safe access with .get()
poster = self.item.get("posters", {}).get("big")

# Rating fallback chain
rating = self.item.get("imdb_rating") or self.item.get("kinopoisk_rating") or 0.0

# Thumbnail fallback
thumbnailImage=self.item.get("thumbnail", self.item.get("posters", {}).get("small", ""))
```

### Type Coercion

```python
"year": int(self.item["year"])  # String → Int
"rating": float(rating)  # Any → Float
```

### Default Values

- `watching.status`: 0 (unwatched)
- `watching.time`: 0 (no resume)
- `advert`: False
- `new`: 0 (no new episodes)
- `subscribed`: False

---

## Metadata Enrichment

### Plot Formatting

**Code:** `modeling.py:166-176`

Adds ratings to plot:

```
IMDB: 8.7
Кинопоиск: 8.5

A computer hacker learns about the true nature...
```

### Title Formatting

**Watchlist Items:**
```python
f"{self.title} : [COLOR FFFFF000]+{self.item['new']}[/COLOR]"
```
Result: `"Friends : +3"` (yellow color for new episodes)

**Season Status:**
```python
f"{'ended' if ended else 'on air'} Season {number}"
```

**Advert Marking:**
```python
f"{title} (!)"  # If advert=true and mark_advert setting enabled
```

---

## Summary

### Data Model Characteristics

- **Hierarchical:** TVShow → Season → Episode
- **Polymorphic:** Same API item can map to different Python classes
- **Rich Metadata:** Ratings from multiple sources, genres, cast, etc.
- **Watch State:** Integrated watching/resume data
- **Quality Levels:** Multiple resolutions and stream types
- **Localized:** Subtitles in multiple languages
- **Artwork:** Multiple poster sizes for different UI contexts

### API Response Patterns

✅ Consistent envelope structure  
✅ Status codes in response body  
✅ Pagination for collections  
✅ Nested objects for related data  
✅ Optional fields handled gracefully  
✅ Timestamps as Unix epoch integers

### Implementation Quality

**Strengths:**
- Type hints throughout
- Cached properties for expensive operations
- Fallback chains for missing data
- Clean separation of concerns (API → Model → UI)
- Proper inheritance hierarchy

**Data Flow:**
```
API JSON → ItemsCollection.instantiate_from_item_data() 
         → ItemEntity/subclass __init__ 
         → .list_item property 
         → ExtendedListItem 
         → xbmcplugin.addDirectoryItem()
```

---

## References

- Data models: `src/resources/lib/modeling.py`
- Response handling: `src/resources/lib/client.py:167-179`
- Type mapping: `src/resources/lib/main.py:22-31`, `modeling.py:524-528`
- List item creation: `src/resources/lib/listitem.py`
- Video info formatting: `modeling.py:179-192`
