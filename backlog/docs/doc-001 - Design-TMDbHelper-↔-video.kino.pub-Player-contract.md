---
id: doc-001
title: 'Design: TMDbHelper ↔ video.kino.pub Player contract'
type: other
created_date: '2025-12-14 12:44'
---
# Design: TMDbHelper ↔ video.kino.pub Player contract

## TMDbHelper player system (plugin.video.themoviedb.helper)
- Player definitions are JSON files under `resources/players/*.json` (bundled) plus user/overrides (`special://profile/addon_data/plugin.video.themoviedb.helper/players/`).
- Keys: `name`, `plugin` (id), optional list `plugins`, `priority`, `provider`, `assert` (required fields to show player), `fallback`, `play_movie|play_episode|search_movie|search_episode` (step arrays), `is_resolvable`, `make_playlist`, `language` (translation lookup), `disabled`.
- Step arrays combine plugin:// URLs and action maps: keyboard input, regex match on list items, return early when season/episode match, dialog handling. Examples: `netflix.json`, `composite_for_plex.json`, `jellycon.json`, `youtube.json`.
- Input keys available for formatting (from Player-Function.md): `{tmdb}`, `{imdb}`, `{tvdb}`, `{trakt}`, `{slug}`, `{name}`, `{title}`, `{year}`, `{season}`, `{episode}`, `{showname}`, etc. TMDbHelper can supply tmdb/imdb/tvdb ids and show/episode numbers.
- Player loading: `tmdbhelper.lib.player.config.files.PlayerFiles` aggregates JSON from bundled/user/saved dirs; `PlayerMeta` computes priority and checks addon enabled. Dialog selection uses `PlayerItems`/`PlayerDefault`, allows combined players and fallback chains. `is_resolvable` true => uses `setResolvedUrl` flow.
- Playerstring (monitor/scrobbler) stores current playback metadata: tmdb_type, tmdb_id (or tvshow tmdb for episode), imdb_id, tvdb_id, season/episode.

## Plugin video.kino.pub (P1) playback model
- Navigation and routes in `src/resources/lib/main.py`; playback routes `plugin://video.kino.pub/play/<item_id>[?season_index=&index=]` for movies/episodes, trailer route `.../trailer/<item_id>`.
- Item models in `src/resources/lib/modeling.py`: internal `item_id` from KinoPub API; episodes reuse show `item_id` with `season_index` and `index` params. Movies/episodes resolve via `ItemsCollection.get_playable` then `Player` (`player.py`) which uses `setResolvedUrl` and refreshes tokens.
- Metadata includes imdb id (`imdbnumber`), ratings, titles, seasons/episodes, but there is **no external id entrypoint**: URLs use KinoPub internal ids, browsing/search flows hit KinoPub API via title-based search and listing endpoints (`main.py` headings/search`).

## Integration contract needs
- TMDbHelper passes tmdb/imdb/tvdb ids, titles, year, season, episode to player JSON steps. To launch P1 directly, we need a plugin:// URL or script entry that can resolve to play a specific movie/episode using those fields.
- Current P1 lacks endpoints to search by tmdb/imdb or direct playback by external id. It only plays by KinoPub `item_id` discovered via its own API/browse/search UI.
- Potential integration options (to be validated):
  - Add a new route to P1 that accepts imdb/tmdb/title params, performs KinoPub API search and resolves first/best match to internal id, then redirects to `/play/<id>`.
  - Alternatively, define TMDbHelper player JSON to open P1 search UI and rely on regex matching, but need to confirm P1 exposes search via plugin:// parameters (currently only interactive search flow `/new_search/<content_type>/` with keyboard prompt).
- is_resolvable: P1 uses `setResolvedUrl` once playback URL known; likely `is_resolvable=true` once proper resolver exists.

## Open questions / gaps
1) Does KinoPub API expose search by imdb/tmdb ids? (not found in repo docs); if not, need strategy (title/year search or new API call).
2) Can P1 accept query parameters to bypass on-screen keyboard for search? If not, need new route to accept query text for TMDbHelper automation.
3) For episodes, how to map TMDbHelper season/episode numbers to KinoPub `season_index` and `index`? (assumes 1-based; confirm against API data format).
4) Are there content type restrictions (movies vs serials vs tvshows) that affect search endpoints or paths (e.g., `/items/<type>/` requirements)?
5) How should fallback behave when multiple matches returned (e.g., different releases or translations)? Define matching heuristic (title regex? year?).

## Findings for player schema examples
- `netflix.json`: uses keyboard automation + regex matching on results; requires title/year or showname/season/episode.
- `composite_for_plex.json`: uses query string search URL with title; asserts title+year for movies.
- `jellycon.json`: simple search URL with title, optional fallback to parentid variant.
- `youtube.json`: search via plugin URL with `{name_url}` / `{title}` keys; uses dialog as needed.

## Candidate contract sketch (to be validated in tasks)
- Player JSON for P1 likely needs `play_movie` URL like `plugin://video.kino.pub/search_play?title={title}&year={year}` if implemented; episodes `...&season={season}&episode={episode}&showname={showname}`.
- Assert keys: start with `title/year` for movies; `showname/season/episode` for episodes.
- Mark `is_resolvable` true once P1 resolver uses `setResolvedUrl`.

This doc should be updated after spikes clarify API capabilities and route design.
