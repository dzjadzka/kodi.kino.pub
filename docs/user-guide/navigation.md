# Navigation

Main menu entries come from `Plugin._main_menu_items` (`src/resources/lib/plugin.py`) and route into handlers in `src/resources/lib/main.py`.

## Main menu items
- Profile (`/profile/`) — user info, subscription days.
- Search (`/search/all/`) — if enabled; lists history and starts new searches.
- Bookmarks (`/bookmarks/`) — folders plus create/delete actions.
- Watching (`/watching/`) and Watching Movies (`/watching_movies/`) — in-progress items.
- Fresh (`/items/all/fresh/`), Popular (`/items/all/popular/`), Hot (`/items/all/hot/`), Sort (`/items/all/sort/`).
- TV (`/tv/`) — live channels.
- Collections (`/collections/`) — fresh/hot/popular groupings.
- Content by type: Movies, Serials, TV Shows, 3D, Concerts, Docu-movies, Docu-serials (`/items/<type>/`).

## Items/<content_type>/ headings
- Headings route: search, fresh, hot, popular, alphabet, genres, sort. Each builds a list then calls `items()` which fetches data and paginates.

## Examples of flows
- Search flow: open `/search/<type>/` → choose **New search** or a history entry → results at `/search/<type>/results/`.
- Collections: `/collections/` lists Fresh/Hot/Popular → `/collections/<sorting>/` → pick collection → `/collection/<id>/` shows items.
- Bookmarks: `/bookmarks/` shows folders; selecting a folder fetches items; context menu offers delete folder and edit bookmarks per item.

## Sources
- src/resources/lib/plugin.py (main menu definition)
- src/resources/lib/main.py (routes)
