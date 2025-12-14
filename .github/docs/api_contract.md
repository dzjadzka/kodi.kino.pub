# API Contract Documentation

Complete API specification for the kino.pub service integration.

**Version:** Based on kodi.kino.pub addon analysis (2023-2025)  
**Base URL:** `https://api.service.kino.pub/v1`  
**OAuth URL:** `https://api.service.kino.pub/oauth2/device`  
**Protocol:** HTTPS only  
**Format:** JSON

---

## Authentication

### OAuth 2.0 Device Authorization Grant (RFC 8628)

**Client Credentials:**
- `client_id`: `xbmc`
- `client_secret`: `cgg3gtifu46urtfp2zp1nqtba0k2ezxh`

#### Device Code Request

```http
POST /oauth2/device
Content-Type: application/x-www-form-urlencoded

grant_type=device_code&client_id=xbmc&client_secret=cgg3gtifu46urtfp2zp1nqtba0k2ezxh
```

**Response (200):**
```json
{
  "status": 200,
  "code": "abc123...",
  "user_code": "ABCD12",
  "verification_uri": "https://kino.pub/device",
  "interval": 5,
  "expires_in": 300
}
```

#### Token Exchange (Polling)

```http
POST /oauth2/device
Content-Type: application/x-www-form-urlencoded

grant_type=device_token&client_id=xbmc&code={device_code}&client_secret=cgg3gtifu46urtfp2zp1nqtba0k2ezxh
```

**Response - Pending (400):**
```json
{
  "error": "authorization_pending"
}
```

**Response - Success (200):**
```json
{
  "status": 200,
  "access_token": "eyJ...",
  "refresh_token": "def...",
  "expires_in": 3600,
  "token_type": "bearer"
}
```

#### Token Refresh

```http
POST /oauth2/device
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token={refresh_token}&client_id=xbmc&client_secret=cgg3gtifu46urtfp2zp1nqtba0k2ezxh
```

**Response (200):**
```json
{
  "status": 200,
  "access_token": "eyJ...",
  "refresh_token": "def...",
  "expires_in": 3600,
  "token_type": "bearer"
}
```

---

## Request Headers

All authenticated requests must include:

```http
Authorization: ******
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...
```

---

## Content Endpoints

### GET /items

Browse and search content with filters.

**Query Parameters:**
- `type` (string, optional) - `movie|serial|tvshow|concert|documovie|docuserial|3d`
- `title` (string, optional) - Search query
- `genre` (int, optional) - Genre ID filter
- `letter` (string, optional) - First letter filter (А-Я, A-Z)
- `page` (int, default: 1) - Page number
- `perpage` (int, default: 50) - Items per page
- `sort` (string, optional) - Sort field with direction: `-rating`, `+title`, etc.
- `start_from` (int, optional) - Starting index (anime exclusion)

**Sort Fields:**
- `updated`, `created`, `year`, `title`, `rating`, `kinopoisk_rating`, `imdb_rating`, `views`, `watchers`

**Response (200):**
```json
{
  "status": 200,
  "items": [{item_object}, ...],
  "pagination": {
    "current": 1,
    "total": 50,
    "perpage": 50
  }
}
```

---

### GET /items/{id}

Get single item details.

**Path Parameters:**
- `id` (int) - Item ID

**Response (200):**
```json
{
  "status": 200,
  "item": {item_object}
}
```

---

### GET /items/fresh

Recently added content.

**Query Parameters:** Same as `/items`

**Response:** Same as `/items`

---

### GET /items/hot

Trending/hot content.

**Query Parameters:** Same as `/items`

**Response:** Same as `/items`

---

### GET /items/popular

Popular content.

**Query Parameters:** Same as `/items`

**Response:** Same as `/items`

---

### GET /items/comments

Get comments for an item.

**Query Parameters:**
- `id` (int, required) - Item ID

**Response (200):**
```json
{
  "status": 200,
  "item": {
    "id": 123,
    "title": "Item Title"
  },
  "comments": [
    {
      "user": {"id": 1, "name": "Username"},
      "message": "Comment text",
      "rating": 5,
      "created_at": 1234567890
    }
  ]
}
```

---

### GET /items/trailer

Get trailer for an item.

**Query Parameters:**
- `id` (int, required) - Item ID

**Response (200):**
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

---

### GET /items/similar

Get similar items.

**Query Parameters:**
- `id` (int, required) - Item ID

**Response (200):**
```json
{
  "status": 200,
  "items": [{item_object}, ...]
}
```

---

## Watch Status Endpoints

### GET /watching

Get watching status for an item.

**Query Parameters:**
- `id` (int, required) - Item ID

**Response (200):**
```json
{
  "status": 200,
  "item": {
    "id": 123,
    "status": 1,
    "time": 1234,
    "duration": 5400
  }
}
```

---

### GET /watching/toggle

Toggle watched status.

**Query Parameters:**
- `id` (int, required) - Item ID
- `status` (int, required) - 0=unwatched, 1=watched
- `season` (int, optional) - Season number
- `video` (int, optional) - Video/episode number

**Response (200):**
```json
{
  "status": 200
}
```

---

### GET /watching/marktime

Set resume point.

**Query Parameters:**
- `id` (int, required) - Item ID
- `time` (int, required) - Resume position in seconds (0 to clear)
- `season` (int, optional) - Season number
- `video` (int, optional) - Video/episode number

**Response (200):**
```json
{
  "status": 200
}
```

---

### GET /watching/movies

Get movies with resume points.

**Response (200):**
```json
{
  "status": 200,
  "items": [{item_object}, ...]
}
```

---

### GET /watching/serials

Get subscribed TV shows.

**Query Parameters:**
- `subscribed` (int, optional) - 1 = only subscribed

**Response (200):**
```json
{
  "status": 200,
  "items": [
    {
      "id": 123,
      "title": "Show Title",
      "new": 3,
      "subscribed": true,
      ...
    }
  ]
}
```

---

### GET /watching/togglewatchlist

Add/remove TV show from watchlist.

**Query Parameters:**
- `id` (int, required) - TV show ID

**Response (200):**
```json
{
  "status": 200
}
```

---

## Bookmarks Endpoints

### GET /bookmarks

Get all bookmark folders.

**Response (200):**
```json
{
  "status": 200,
  "items": [
    {
      "id": 1,
      "title": "Favorites",
      "views": 15,
      "created_at": 1234567890
    }
  ]
}
```

---

### GET /bookmarks/{folder_id}

Get items in bookmark folder.

**Path Parameters:**
- `folder_id` (int) - Folder ID

**Query Parameters:**
- `page` (int, optional) - Page number

**Response (200):**
```json
{
  "status": 200,
  "items": [{item_object}, ...],
  "pagination": {...}
}
```

---

### GET /bookmarks/get-item-folders

Get folders containing specific item.

**Query Parameters:**
- `item` (int, required) - Item ID

**Response (200):**
```json
{
  "status": 200,
  "folders": [
    {"id": 1, "title": "Favorites"}
  ]
}
```

---

### POST /bookmarks/create

Create new bookmark folder.

**Request Body (application/x-www-form-urlencoded):**
```
title={folder_name}
```

**Response (200):**
```json
{
  "status": 200,
  "folder": {
    "id": 123,
    "title": "My Folder"
  }
}
```

---

### POST /bookmarks/add

Add item to bookmark folder.

**Request Body:**
```
item={item_id}&folder={folder_id}
```

**Response (200):**
```json
{
  "status": 200
}
```

---

### POST /bookmarks/remove-item

Remove item from bookmark folder.

**Request Body:**
```
item={item_id}&folder={folder_id}
```

**Response (200):**
```json
{
  "status": 200
}
```

---

### POST /bookmarks/remove-folder

Delete bookmark folder.

**Request Body:**
```
folder={folder_id}
```

**Response (200):**
```json
{
  "status": 200
}
```

---

## Collections Endpoints

### GET /collections/index

Get collections list.

**Query Parameters:**
- `sort` (string, optional) - `-created`, `-watchers`, `-views`
- `page` (int, optional) - Page number

**Response (200):**
```json
{
  "status": 200,
  "items": [
    {
      "id": 123,
      "title": "Collection Title",
      "views": 1234,
      "watchers": 567
    }
  ],
  "pagination": {...}
}
```

---

### GET /collections/view

Get items in a collection.

**Query Parameters:**
- `id` (int, required) - Collection ID

**Response (200):**
```json
{
  "status": 200,
  "items": [{item_object}, ...]
}
```

---

## Other Endpoints

### GET /genres

Get available genres.

**Query Parameters:**
- `type` (string, optional) - Content type

**Response (200):**
```json
{
  "status": 200,
  "items": [
    {"id": 1, "title": "Action"},
    {"id": 2, "title": "Comedy"}
  ]
}
```

---

### GET /tv/index

Get live TV channels.

**Response (200):**
```json
{
  "status": 200,
  "channels": [
    {
      "id": 1,
      "title": "Channel 1",
      "stream": "https://.../stream.m3u8",
      "logos": {
        "s": "https://...",
        "m": "https://...",
        "l": "https://..."
      }
    }
  ]
}
```

---

### GET /user

Get current user information.

**Response (200):**
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

---

### POST /device/notify

Register/update device information.

**Request Body:**
```
title={device_name}&hardware={platform}&software={kodi_version}
```

**Response (200):**
```json
{
  "status": 200
}
```

---

## Data Models

### Item Object

```json
{
  "id": 123456,
  "type": "movie|serial|tvshow|concert|documovie|docuserial|3d",
  "subtype": "multi",
  "title": "Title",
  "year": 1999,
  "rating": 8.5,
  "rating_votes": 150000,
  "kinopoisk_rating": 8.0,
  "imdb_rating": 8.7,
  "imdb": "0133093",
  "plot": "Description...",
  "cast": "Actor1, Actor2",
  "director": "Director",
  "genres": [{"id": 1, "title": "Action"}],
  "countries": [{"id": 1, "title": "USA"}],
  "posters": {
    "small": "https://...",
    "medium": "https://...",
    "big": "https://...",
    "wide": "https://..."
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
  "trailer": [...],
  "videos": [...],
  "seasons": [...]
}
```

### Video Object

```json
{
  "id": 789,
  "title": "Episode 1",
  "number": 1,
  "snumber": 1,
  "duration": 1440,
  "files": [
    {
      "quality": "1080p",
      "url": {
        "hls": "https://.../index.m3u8",
        "hls2": "https://.../index.m3u8",
        "hls4": "https://.../master.m3u8"
      }
    }
  ],
  "subtitles": [
    {"lang": "eng", "url": "https://..."}
  ]
}
```

---

## Error Responses

### Standard Error Format

```json
{
  "error": "error_code",
  "error_description": "Human readable message"
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad request / OAuth errors
- `401` - Unauthorized (triggers auto token refresh)
- `429` - Too many requests (retry after delay)
- `5xx` - Server errors

### Common Error Codes

- `authorization_pending` - OAuth pending (400)
- `code_expired` - Device code expired (400)
- `authorization_expired` - Refresh token expired (400)
- `invalid_refresh_token` - Invalid refresh token (400)

---

## Rate Limiting

**429 Response Handling:**
- Retry after 5 second delay
- Maximum 3 retry attempts
- After 3 failures: Show error and exit

---

## Summary

**Total Endpoints:** 28  
**Authentication:** OAuth 2.0 Device Flow  
**Data Format:** JSON  
**Base URL:** `https://api.service.kino.pub/v1`  
**Timeout:** 60 seconds

**Endpoint Categories:**
- Authentication: 4 endpoints
- Content: 7 endpoints
- Watching/State: 6 endpoints
- Bookmarks: 7 endpoints
- Collections: 2 endpoints
- Other: 3 endpoints
