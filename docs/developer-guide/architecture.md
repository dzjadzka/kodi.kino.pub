# Architecture

High-level flow and key modules for the kino.pub Kodi add-on.

## Entrypoint and routing
- `src/addon.py` imports `plugin` from `resources.lib.main` and runs `plugin.run()`.
- `Plugin` initializes settings, auth, logger, routing, search history, items collection, KinoPub client, and proxy settings.
- `Routing` (`src/resources/lib/routing.py`) maps URL-like paths (e.g., `/login/`, `/items/<type>/`) to view functions in `main.py`; builds plugin URLs and dispatches based on regex rules.

## Main plugin orchestration
- `main.py` defines routes for login/reset auth, main menu, browsing headings, search, collections, bookmarks, watching, TV, playback, comments/similar, trailers, and utility actions.
- `Plugin._main_menu_items` lists top-level navigation entries with visibility controlled by settings.

## Models and items
- `modeling.py` (not exhaustively detailed here) provides item entities (`ItemEntity`, `TVShow`, `Multi`, etc.) used by `ItemsCollection` to hydrate list items and playback data.
- `ExtendedListItem` (`listitem.py`) wraps `xbmcgui.ListItem` adding context menus (watchlist, watched/unwatched, bookmarks, comments, similar) and metadata helpers.

## Helpers
- `auth.py` handles device-code OAuth, token refresh, and device registration.
- `client.py` wraps API calls with proxy support, auth headers, and HTTP error handling.
- `search_history.py` persists search queries under addon data.
- `settings.py` maps Kodi settings to convenience properties (sorting, API URLs, testing flag) and advancedsettings defaults.
- `player.py` tracks playback/resume/watched status and sets Trakt scrobble properties.
- `logger.py` configures rotating file logging when `KINO_PUB_TEST` is set.
- `xbmc_settings.py` reads system settings (proxy) via JSON-RPC.

## Sources
- src/addon.py
- src/resources/lib/{main.py,plugin.py,routing.py,modeling.py,listitem.py,auth.py,client.py,search_history.py,settings.py,player.py,logger.py,xbmc_settings.py}
