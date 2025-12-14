# API integration

KinoPub API calls are orchestrated via `KinoPubClient` (`src/resources/lib/client.py`) and routes in `src/resources/lib/main.py`.

## Authentication and headers
- All requests include `Authorization: Bearer <access_token>` set in request processor.
- OAuth device/refresh handled by `Auth` against `oauth_api_url`; tokens stored in settings.
- Error handling: 401 triggers token refresh/retry; 429 retries with backoff; fatal errors show popups and exit.

## Core endpoints used
- Items: `items`, `items/<heading>` (fresh/hot/popular/alphabet/genres/sort/search results), `items/similar`, `items/trailer`.
- Genres: `genres` for listing by type.
- TV: `tv/index` for channels.
- Collections: `collections/index`, `collections/view`.
- Bookmarks: `bookmarks`, `bookmarks/<folder_id>`, `bookmarks/get-item-folders`, `bookmarks/add`, `bookmarks/remove-item`, `bookmarks/create`, `bookmarks/remove-folder`.
- Watching: `watching/marktime`, `watching/toggle`, `watching/togglewatchlist`.
- User: `user` profile data.
- Comments: `items/comments`.
- Similar: `items/similar`.
- Device notify: `device/notify` (after activation).

## Request patterns and data
- GET queries are urlencoded and appended; POST payloads urlencoded with UTF-8.
- Sorting params derived from settings (`sort_by`, `sort_direction`), with exclude anime flag when applicable.
- Pagination data from API surfaces `next page` handling in UI.

## Sources
- src/resources/lib/client.py
- src/resources/lib/main.py
