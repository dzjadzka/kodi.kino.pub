# Search and history

Search UI and persistence are handled by routes in `src/resources/lib/main.py` and `SearchHistory` (`src/resources/lib/search_history.py`).

## Search entry points
- From main menu: Search → `/search/all/` (or type-specific).
- Inside headings: `/items/<type>/` includes a **Search** entry.
- Route `/search/<type>/` shows **New search** plus recent history items.

## Running a search
1. Choose **New search** → on-screen keyboard → query saved to history.
2. Results load via `/search/<type>/results/` calling `items` API with current sort/filter settings.

## History persistence
- Stored in `special://userdata/addon_data/video.kino.pub/history` JSON.
- `history_max_qty` setting limits how many recent items are shown (default 10); older entries remain on disk but are trimmed in the UI slice.
- Duplicates are moved to the top when re-used.

## Clearing history
- Route `/clean_search_history/` asks for confirmation, then wipes the saved list and refreshes the container.

## Sources
- src/resources/lib/main.py (search routes)
- src/resources/lib/search_history.py
