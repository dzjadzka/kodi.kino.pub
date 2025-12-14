# Documentation Structure

Grounded in the current repository layout and code.

## Existing docs
- README.md — add-on overview, key features, Kodi version support, installation from repository ZIP and manual install steps.
- CONTRIBUTING.md — development setup (Python 3.6+), dev dependencies, podman requirement, test/pre-commit workflow.

## Proposed tree (derive content from noted sources)
- backlog/docs/overview.md — TODO: summarize add-on purpose and supported Kodi versions from README.md and metadata in src/addon.xml (id/name/provider, provides=video).
- backlog/docs/user-guide/
  - installation.md — TODO: restructure README.md install instructions (repo add-on ZIP path, manual release ZIP).
  - authentication.md — TODO: document device-code flow and token refresh from resources/lib/auth.py and the /login route in resources/lib/main.py.
  - navigation.md — TODO: describe main menu entries from Plugin._main_menu_items in resources/lib/plugin.py and user flows exposed in resources/lib/main.py (search, fresh/hot/popular, collections, TV, bookmarks, watching, items/<type> headings).
  - search-and-history.md — TODO: cover search UI plus history persistence logic from resources/lib/search_history.py and search routes in resources/lib/main.py.
  - bookmarks-and-watchlist.md — TODO: explain bookmark folders, edit/remove/create routes, watchlist toggle, mark watched/unwatched, and context menu items from resources/lib/main.py and resources/lib/listitem.py.
  - playback.md — TODO: outline playback/resume behavior, quality selection, trailer handling, and Trakt scrobble properties from resources/lib/player.py and resources/lib/modeling.py.
  - settings.md — TODO: enumerate user-facing settings from src/resources/settings.xml and Settings helper in resources/lib/settings.py (video quality/stream type, ask_quality, mark_advert, exclude_anime, inputstream adaptive toggle/install helper, loc, history_max_qty, sorting, etc.).
  - proxy-and-network.md — TODO: describe system proxy usage and validation from resources/lib/xbmc_settings.py and request processing in resources/lib/client.py.
  - localization.md — TODO: point to resources/language/ for translations and reference localization keys (320xx) used across UI strings.
- backlog/docs/developer-guide/
  - architecture.md — TODO: outline entrypoint (src/addon.py), routing system (resources/lib/routing.py), plugin orchestration (resources/lib/plugin.py), models/entities (resources/lib/modeling.py), and helpers (utils, listitem, logger).
  - api-integration.md — TODO: list KinoPub API endpoints currently called (items, watching, bookmarks, collections, genres, user, device/notify, comments, similar, trailer) as seen in resources/lib/main.py and resources/lib/client.py; note auth headers and error handling.
  - testing.md — TODO: document unit vs integration tests: pytest harness, podman-based Kodi + mockserver setup from tests/conftest.py/helpers.py, expected_results fixtures, and proxy coverage (tests/test_proxy.py).
  - build-and-release.md — TODO: capture Makefile targets (video_addon, repo_addon, repo, deploy), required env vars (VERSION, NETLIFY_AUTH_TOKEN, NETLIFY_SITE_ID), and packaging of src/addon.py/resources plus repo_src assets.
  - settings-and-env.md — TODO: explain KINO_PUB_TEST flag impact on Settings.api_url and Logger configuration (resources/lib/settings.py, resources/lib/logger.py).
