# Bookmarks and watchlist

Routes and context menu actions live in `src/resources/lib/main.py` and list item helpers in `src/resources/lib/listitem.py`.

## Bookmarks folders
- Open `/bookmarks/` to see folders plus **Make a folder** action.
- Context menu on folders: Delete (calls `/remove_bookmarks_folder/<id>`).
- Create folder: `/create_bookmarks_folder` prompts for a name and refreshes the list.
- Selecting a folder fetches items via `bookmarks/<folder_id>` with pagination.

## Editing item bookmarks
- Context menu entry **Change bookmarks** triggers `/edit_bookmarks/<item_id>` to multi-select folders; adds/removes via `bookmarks/add` and `bookmarks/remove-item`.
- Popup confirms when bookmarks change.

## Watchlist toggle
- Context menu **Will watch/Won't watch** uses `/toggle_watchlist/<item_id>`; shows popup for add/remove.

## Watched/unwatched markers
- Context menu **Mark as seen/Mark as unseen** uses `/toggle_watched/<item_id>` with season/episode params when applicable; resets resume time for videos when needed.

## Sources
- src/resources/lib/main.py (bookmark/watchlist routes)
- src/resources/lib/listitem.py (context menus)
