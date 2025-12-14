# API Endpoints Documentation

Complete inventory of all kino.pub API endpoints used by the addon.

## Overview

**Base URL:** Configured in settings (default appears to be kino.pub API)

**Authentication:** Bearer token in Authorization header

**Response Format:** JSON

**Total Unique Endpoints:** 27+ (19 direct + 8+ via items.get())

---

## API Architecture

### Request Structure

```http
GET /v1/<endpoint>?<query_params> HTTP/1.1
Host: api.service.kino.pub
Authorization: Bearer <access_token>
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...
```

### Response Structure

```json
{
  "status": 200,
  "items": [...],
  "pagination": {
    "current": 1,
    "total": 10,
    "perpage": 50
  }
}
```

**Common Response Fields:**
- `status` - HTTP status code (200 = success)
- `items` - Array of item objects (for collection endpoints)
- `item` - Single item object (for single item endpoints)
- `pagination` - Pagination metadata (for paginated endpoints)

---

## Authentication Endpoints

### OAuth Device Code Flow

#### `POST /oauth/device`

**Purpose:** Request device code for device flow authentication

**Request Body:**
```
grant_type=device_code
client_id=xbmc
client_secret=cgg3gtifu46urtfp2zp1nqtba0k2ezxh
```

**Response:**
```json
{
  "status": 200,
  "code": "<device_code>",
  "user_code": "<4-6_char_code>",
  "verification_uri": "https://kino.pub/device",
  "interval": 5,
  "expires_in": 300
}
```

**Fields:**
- `code` - Device code for polling
- `user_code` - Code user enters on website
- `verification_uri` - URL user visits to activate
- `interval` - Polling interval in seconds
- `expires_in` - Code expiration time

**Used by:** `auth.py:131-143` - `Auth._get_device_code()`

---

#### `POST /oauth/device_token`

**Purpose:** Exchange device code for access token (polling)

**Request Body:**
```
grant_type=device_token
client_id=xbmc
code=<device_code>
client_secret=cgg3gtifu46urtfp2zp1nqtba0k2ezxh
```

**Success Response:**
```json
{
  "status": 200,
  "access_token": "<jwt_token>",
  "refresh_token": "<refresh_token>",
  "expires_in": 3600,
  "token_type": "bearer"
}
```

**Pending Response (400):**
```json
{
  "error": "authorization_pending",
  "error_description": "..."
}
```

**Expired Response (400):**
```json
{
  "error": "code_expired",
  "error_description": "..."
}
```

**Used by:** `auth.py:145-154` - `Auth._get_device_token()`

**Polling:** Every 5 seconds for up to 5 minutes

---

#### `POST /oauth/token` (refresh)

**Purpose:** Refresh access token using refresh token

**Request Body:**
```
grant_type=refresh_token
refresh_token=<refresh_token>
client_id=xbmc
client_secret=cgg3gtifu46urtfp2zp1nqtba0k2ezxh
```

**Response:**
```json
{
  "status": 200,
  "access_token": "<new_jwt_token>",
  "refresh_token": "<new_refresh_token>",
  "expires_in": 3600,
  "token_type": "bearer"
}
```

**Used by:** `auth.py:156-169` - `Auth._refresh_token()`

**Trigger:** 
- Automatic on 401 error
- Before playback if token expires during playback

---

### Device Management

#### `POST /device/notify`

**Purpose:** Register/update device information

**Request Body:**
```
title=<device_friendly_name>
hardware=<platform.machine()>
software=Kodi <version>
```

**Response:**
```json
{
  "status": 200
}
```

**Used by:** `auth.py:171-182` - `Auth._update_device_info()`

**Called:** After successful device activation

**Example:**
```
title=Living Room Kodi
hardware=x86_64
software=Kodi 20.0
```

---

## Items/Content Endpoints

### `GET /items`

**Purpose:** Get items with filtering and sorting

**Query Parameters:**
- `type` - Content type filter (movie/serial/tvshow/concert/documovie/docuserial/3d) or null for all
- `title` - Search query
- `genre` - Genre ID filter
- `letter` - First letter filter (А-Я, A-Z)
- `page` - Page number (default: 1)
- `perpage` - Items per page (default: 50)
- `sort` - Sort field with direction prefix (+/-), e.g., `-rating`, `+title`
- `start_from` - Starting index for anime exclusion

**Response:**
```json
{
  "status": 200,
  "items": [
    {
      "id": 123456,
      "type": "movie",
      "title": "The Matrix",
      "year": 1999,
      "rating": 8.7,
      "kinopoisk": 8.5,
      "imdb": 8.7,
      "posters": {
        "small": "https://...",
        "medium": "https://...",
        "big": "https://...",
        "wide": "https://..."
      },
      "videos": [...],
      "subtype": "multi",  // For multi-episode items
      ...
    },
    ...
  ],
  "pagination": {
    "current": 1,
    "total": 50,
    "perpage": 50
  }
}
```

**Used by:**
- `main.py:149,151` - Items by heading (fresh/hot/popular/sort)
- `main.py:178` - Genre items
- `main.py:205` - Alphabet items
- `main.py:246` - Search results

**Sort Options:**
- `updated` - Last update time
- `created` - Creation time
- `year` - Release year
- `title` - Title alphabetically
- `rating` - Combined rating
- `kinopoisk_rating` - Kinopoisk rating
- `imdb_rating` - IMDB rating
- `views` - View count
- `watchers` - Watcher count

**Direction:** `-` (desc) or `+` (asc)

---

### `GET /items/<id>`

**Purpose:** Get single item details

**Query Parameters:** None

**Response:**
```json
{
  "status": 200,
  "item": {
    "id": 123456,
    "type": "serial",
    "title": "Friends",
    "year": 1994,
    "seasons": [
      {
        "number": 1,
        "episodes": [
          {
            "id": 123,
            "title": "Episode 1",
            "number": 1,
            "watching": {
              "status": 0,
              "time": 0,
              "duration": 1440
            },
            "files": [
              {
                "quality": "1080p",
                "url": {
                  "hls": "https://...",
                  "hls2": "https://...",
                  "hls4": "https://..."
                }
              }
            ],
            "subtitles": [...],
            ...
          }
        ]
      }
    ],
    ...
  }
}
```

**Used by:** `modeling.py:68-69` - `ItemsCollection.get_api_item()`

**Called:** When item not in window property cache

---

### `GET /items/fresh`

**Purpose:** Get recently added items

**Query Parameters:** Same as `/items` (type, page, etc.)

**Response:** Same structure as `/items`

**Used by:** `main.py:151` - Fresh heading

---

### `GET /items/hot`

**Purpose:** Get hot/trending items

**Query Parameters:** Same as `/items`

**Response:** Same structure as `/items`

**Used by:** `main.py:151` - Hot heading

---

### `GET /items/popular`

**Purpose:** Get popular items

**Query Parameters:** Same as `/items`

**Response:** Same structure as `/items`

**Used by:** `main.py:151` - Popular heading

---

### `GET /items/comments`

**Purpose:** Get comments for an item

**Query Parameters:**
- `id` - Item ID

**Response:**
```json
{
  "status": 200,
  "item": {
    "id": 123456,
    "title": "The Matrix"
  },
  "comments": [
    {
      "user": {
        "name": "UserName"
      },
      "message": "Comment text...",
      "rating": 5,
      "created_at": 1234567890
    },
    ...
  ]
}
```

**Used by:** `main.py:500` - Comments dialog

---

### `GET /items/trailer`

**Purpose:** Get trailer URL for item

**Query Parameters:**
- `id` - Item ID

**Response:**
```json
{
  "status": 200,
  "trailer": [
    {
      "url": "https://...",
      "quality": "1080p"
    }
  ]
}
```

**Used by:** `main.py:305` - Trailer playback

---

### `GET /items/similar`

**Purpose:** Get similar items

**Query Parameters:**
- `id` - Item ID

**Response:**
```json
{
  "status": 200,
  "items": [...]  // Same structure as /items
}
```

**Used by:** `main.py:522` - Similar items listing

---

## Watching/State Endpoints

### `GET /watching`

**Purpose:** Get watching information for item

**Query Parameters:**
- `id` - Item ID

**Response:**
```json
{
  "status": 200,
  "item": {
    "id": 123456,
    "status": 1,  // 0=unwatched, 1=watched
    "time": 1234,  // Resume position in seconds
    "duration": 5400,  // Total duration in seconds
    "updated_at": 1234567890
  }
}
```

**Used by:** `modeling.py:201-202` - `ItemEntity.watching_info`

**Cached:** Via `@cached_property` per object instance

---

### `GET /watching/toggle`

**Purpose:** Toggle watched status

**Query Parameters:**
- `id` - Item ID
- `status` - New status (0=unwatched, 1=watched)
- `season` - Season number (optional, for TV shows)
- `video` - Video/episode number (optional)

**Response:**
```json
{
  "status": 200
}
```

**Used by:**
- `main.py:408` - Toggle watched context menu
- `player.py:88,103` - Auto-mark as watched on playback end

**Side Effects:** Updates watch status in database

---

### `GET /watching/marktime`

**Purpose:** Set resume point

**Query Parameters:**
- `id` - Item ID
- `time` - Resume position in seconds (0 to clear)
- `season` - Season number (optional, for TV shows)
- `video` - Video/episode number (optional)

**Response:**
```json
{
  "status": 200
}
```

**Used by:**
- `main.py:411` - Clear resume point on toggle watched
- `player.py:84` - Save resume point on playback stop

**Side Effects:** Updates resume position in database

---

### `GET /watching/movies`

**Purpose:** Get movies with resume points

**Query Parameters:** None

**Response:**
```json
{
  "status": 200,
  "items": [...]  // Movies with watching.time > 0
}
```

**Used by:** `modeling.py:50-55` - Watching movies list

---

### `GET /watching/serials`

**Purpose:** Get subscribed TV shows

**Query Parameters:**
- `subscribed` - Filter (1 = only subscribed)

**Response:**
```json
{
  "status": 200,
  "items": [
    {
      "id": 123,
      "title": "Friends",
      "new": 3,  // New episodes since last watch
      "subscribed": true,
      ...
    },
    ...
  ]
}
```

**Used by:** `modeling.py:57-66` - Watching TV shows list

---

### `GET /watching/togglewatchlist`

**Purpose:** Add/remove TV show from watchlist

**Query Parameters:**
- `id` - TV show ID

**Response:**
```json
{
  "status": 200
}
```

**Used by:** `main.py:419` - Toggle watchlist context menu

**Side Effects:** Toggles subscription status

---

## Bookmarks Endpoints

### `GET /bookmarks`

**Purpose:** Get all bookmark folders

**Query Parameters:** None

**Response:**
```json
{
  "status": 200,
  "items": [
    {
      "id": 1,
      "title": "Favorites",
      "views": 15,  // Item count
      "created_at": 1234567890
    },
    ...
  ]
}
```

**Used by:**
- `main.py:319` - Bookmarks folder list
- `main.py:433` - Edit bookmarks (get all folders)

---

### `GET /bookmarks/<folder_id>`

**Purpose:** Get items in bookmark folder

**Query Parameters:**
- `page` - Page number

**Response:**
```json
{
  "status": 200,
  "items": [...],  // Same structure as /items
  "pagination": {...}
}
```

**Used by:** `main.py:338` - Show bookmark folder contents

---

### `GET /bookmarks/get-item-folders`

**Purpose:** Get folders containing specific item

**Query Parameters:**
- `item` - Item ID

**Response:**
```json
{
  "status": 200,
  "folders": [
    {
      "id": 1,
      "title": "Favorites"
    },
    ...
  ]
}
```

**Used by:** `main.py:432` - Edit bookmarks (get current folders)

---

### `POST /bookmarks/create`

**Purpose:** Create new bookmark folder

**Request Body:**
```
title=<folder_name>
```

**Response:**
```json
{
  "status": 200,
  "folder": {
    "id": 123,
    "title": "My New Folder"
  }
}
```

**Used by:** `main.py:479` - Create bookmarks folder

---

### `POST /bookmarks/add`

**Purpose:** Add item to bookmark folder

**Request Body:**
```
item=<item_id>
folder=<folder_id>
```

**Response:**
```json
{
  "status": 200
}
```

**Used by:** `main.py:456` - Edit bookmarks (add to folders)

---

### `POST /bookmarks/remove-item`

**Purpose:** Remove item from bookmark folder

**Request Body:**
```
item=<item_id>
folder=<folder_id>
```

**Response:**
```json
{
  "status": 200
}
```

**Used by:** `main.py:458-460` - Edit bookmarks (remove from folders)

---

### `POST /bookmarks/remove-folder`

**Purpose:** Delete bookmark folder

**Request Body:**
```
folder=<folder_id>
```

**Response:**
```json
{
  "status": 200
}
```

**Used by:** `main.py:467` - Remove bookmarks folder

---

## Collections Endpoints

### `GET /collections/index`

**Purpose:** Get collections list

**Query Parameters:**
- `sort` - Sort field with direction (e.g., `-created`, `-watchers`, `-views`)
- `page` - Page number

**Response:**
```json
{
  "status": 200,
  "items": [
    {
      "id": 123,
      "title": "Best of 2023",
      "posters": {
        "medium": "https://..."
      },
      "views": 1234,
      "watchers": 567,
      "created_at": 1234567890
    },
    ...
  ],
  "pagination": {...}
}
```

**Used by:** `main.py:389` - Sorted collections

**Sort Fields:**
- `created` - Creation date
- `watchers` - Watcher count
- `views` - View count

---

### `GET /collections/view`

**Purpose:** Get items in a collection

**Query Parameters:**
- `id` - Collection ID

**Response:**
```json
{
  "status": 200,
  "items": [...]  // Same structure as /items
}
```

**Used by:** `main.py:400` - Collection contents

---

## Other Endpoints

### `GET /genres`

**Purpose:** Get available genres for content type

**Query Parameters:**
- `type` - Content type (movie/serial/etc.)

**Response:**
```json
{
  "status": 200,
  "items": [
    {
      "id": 1,
      "title": "Action"
    },
    {
      "id": 2,
      "title": "Comedy"
    },
    ...
  ]
}
```

**Used by:** `main.py:166` - Genres list

---

### `GET /tv/index`

**Purpose:** Get live TV channels

**Query Parameters:** None

**Response:**
```json
{
  "status": 200,
  "channels": [
    {
      "id": 1,
      "title": "Channel 1",
      "stream": "https://...",
      "logos": {
        "s": "https://...",
        "m": "https://...",
        "l": "https://..."
      }
    },
    ...
  ]
}
```

**Used by:** `main.py:158` - TV channels list

---

### `GET /user`

**Purpose:** Get current user information

**Query Parameters:** None

**Response:**
```json
{
  "status": 200,
  "user": {
    "id": 123,
    "username": "user@example.com",
    "reg_date": 1234567890,
    "subscription": {
      "active": true,
      "days": 365
    }
  }
}
```

**Used by:** `main.py:485` - Profile dialog

---

## Endpoint Usage Summary

### By Category

**Authentication (4 endpoints):**
- POST /oauth/device
- POST /oauth/device_token
- POST /oauth/token (refresh)
- POST /device/notify

**Items/Content (7 endpoints):**
- GET /items (with variants: fresh, hot, popular)
- GET /items/<id>
- GET /items/comments
- GET /items/trailer
- GET /items/similar

**Watching/State (6 endpoints):**
- GET /watching
- GET /watching/toggle
- GET /watching/marktime
- GET /watching/movies
- GET /watching/serials
- GET /watching/togglewatchlist

**Bookmarks (6 endpoints):**
- GET /bookmarks
- GET /bookmarks/<folder_id>
- GET /bookmarks/get-item-folders
- POST /bookmarks/create
- POST /bookmarks/add
- POST /bookmarks/remove-item
- POST /bookmarks/remove-folder

**Collections (2 endpoints):**
- GET /collections/index
- GET /collections/view

**Other (3 endpoints):**
- GET /genres
- GET /tv/index
- GET /user

**Total: 28 unique endpoints**

---

## Request Patterns

### Common Headers

```http
Authorization: Bearer <access_token>
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36
```

### GET Requests

```python
# Via KinoPubClient
response = plugin.client("items/fresh").get(data={"type": "movie", "page": 2})
```

Translates to:
```http
GET /items/fresh?type=movie&page=2 HTTP/1.1
```

### POST Requests

```python
# Via KinoPubClient
response = plugin.client("bookmarks/create").post(data={"title": "My Folder"})
```

Translates to:
```http
POST /bookmarks/create HTTP/1.1
Content-Type: application/x-www-form-urlencoded

title=My+Folder
```

---

## Error Handling

### HTTP Error Codes

- **200** - Success
- **400** - Bad request (auth pending, code expired, etc.)
- **401** - Unauthorized (triggers automatic token refresh)
- **429** - Too many requests (triggers retry with 5s delay, up to 3 attempts)
- **Other** - Fatal error, shows popup and exits

### Error Response Format

```json
{
  "error": "error_code",
  "error_description": "Human readable description"
}
```

**Common Error Codes:**
- `authorization_pending` - User hasn't authorized yet (device flow)
- `code_expired` - Device code expired
- `authorization_expired` - Refresh token expired
- `invalid_refresh_token` - Refresh token invalid

**Handler:** `client.py:85-152` - `KinoApiErrorProcessor`

---

## Rate Limiting

**429 Handling:**
- Retries after 5 second delay
- Maximum 3 attempts
- After 3 failures: Shows error popup and exits

**Implementation:** `client.py:132-151`

---

## Authentication Flow

```
1. User initiates /login/
2. POST /oauth/device → {user_code, device_code, verification_uri}
3. Show dialog with code and URL
4. Poll POST /oauth/device_token every 5s (up to 5 minutes)
   - 400 {error: "authorization_pending"} → Continue polling
   - 400 {error: "code_expired"} → Fail
   - 200 {access_token, refresh_token} → Success
5. Save tokens to settings
6. POST /device/notify with device info
7. All subsequent requests include: Authorization: Bearer <access_token>
8. On 401: Automatic POST /oauth/token to refresh
```

---

## Data Models

### Item Object

```json
{
  "id": 123456,
  "type": "movie|serial|tvshow|concert|documovie|docuserial|3d",
  "subtype": "multi",  // For multi-episode items
  "title": "Title",
  "year": 2023,
  "rating": 8.5,
  "kinopoisk": 8.0,
  "imdb": 8.7,
  "poster": "url",  // Deprecated, use posters
  "posters": {
    "small": "url",
    "medium": "url",
    "big": "url",
    "wide": "url"
  },
  "plot": "Description...",
  "cast": "Actor 1, Actor 2",
  "director": "Director Name",
  "genre": "Action, Thriller",
  "country": "USA",
  "advert": false,
  "subscribed": true,  // For TV shows in watchlist
  "new": 3,  // New unwatched episodes
  "watching": {
    "status": 0,  // 0=unwatched, 1=watched
    "time": 0,  // Resume position (seconds)
    "duration": 5400  // Total duration (seconds)
  },
  "videos": [...],  // Video files
  "seasons": [...],  // For TV shows
  ...
}
```

### Video Object

```json
{
  "id": 123,
  "title": "Episode 1",
  "number": 1,
  "thumbnail": "url",
  "watching": {
    "status": 0,
    "time": 0,
    "duration": 1440
  },
  "files": [
    {
      "quality": "1080p|720p|480p|2160p",
      "url": {
        "hls": "https://...",
        "hls2": "https://...",
        "hls4": "https://..."
      }
    }
  ],
  "subtitles": [
    {
      "lang": "eng",
      "url": "https://..."
    }
  ]
}
```

### Pagination Object

```json
{
  "current": 1,
  "total": 50,
  "perpage": 50,
  "start_from": 100  // For anime exclusion
}
```

---

## API Settings

**Configured in:** `settings.py:60-65`

```python
@property
def api_url(self) -> str:
    return "https://api.service.kino.pub/v1"

@property
def oauth_api_url(self) -> str:
    return "https://api.service.kino.pub/oauth2/device"
```

**Base URLs:**
- Main API: `https://api.service.kino.pub/v1`
- OAuth API: `https://api.service.kino.pub/oauth2/device`

---

## References

- Client implementation: `src/resources/lib/client.py`
- Authentication: `src/resources/lib/auth.py`
- Items collection: `src/resources/lib/modeling.py`
- Route handlers: `src/resources/lib/main.py`
- Error handling: `src/resources/lib/client.py:85-152`
