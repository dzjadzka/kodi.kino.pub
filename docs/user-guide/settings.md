# Settings

User-facing settings are defined in `src/resources/settings.xml` and interpreted by `Settings` helper (`src/resources/lib/settings.py`).

## Playback and quality
- `stream_type` (hls/hls2/hls4) with optional `ask_quality` prompt (HLS only).
- `video_quality` default for HLS when not prompting (2160p/1080p/720p/480p).
- `mark_advert` toggles "(!)" marker on items flagged with ads.
- `exclude_anime` hides anime when supported by API filters.

## InputStream Adaptive
- `use_inputstream_adaptive` toggle (enabled only if addon installed).
- `inputstream_helper_install` action installs helper; `inputstream_adaptive_settings` opens addon settings.

## Sorting
- `sort_by` (updated/created/year/title/rating/kinopoisk_rating/imdb_rating/views/watchers).
- `sort_direction` (asc/desc). Helper exposes localized titles and param suffixes for API calls.

## Search history
- `history_max_qty` controls how many recent searches are shown.
- `reset_search_history` button triggers `/clean_search_history/`.

## Auth reset
- `reset_auth` clears stored tokens via `/reset_auth/`.

## Menu visibility
- Toggles for showing search, last/fresh, hot, popular, sort, TV, collections, movies, serials, TV shows, 3D, concerts, docu-movies, docu-serials.

## Localization
- `loc` chooses language (ru/nl) for UI content where supported.

## Advanced defaults
- `Settings.advanced(...)` reads Kodi advancedsettings.xml with defaults: playcountminimumpercent=90, ignoresecondsatstart=180, ignorepercentatend=8.

## Sources
- src/resources/settings.xml
- src/resources/lib/settings.py
