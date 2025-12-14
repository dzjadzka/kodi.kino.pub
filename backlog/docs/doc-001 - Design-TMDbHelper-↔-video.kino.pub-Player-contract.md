---
id: doc-001
title: 'Design: TMDbHelper ↔ video.kino.pub Player contract'
type: other
created_date: '2025-12-14 12:44'
updated_date: '2025-12-14 13:00'
---
# Design: TMDbHelper ↔ video.kino.pub Player contract

## TMDbHelper player system (plugin.video.themoviedb.helper)
- Player definitions live in `resources/players/*.json` (bundled) plus user overrides at `special://profile/addon_data/plugin.video.themoviedb.helper/players/`.
- Keys: `name`, `plugin` (or list of plugins), `priority`, `provider`, `assert`, `fallback`, `play_movie|play_episode|search_movie|search_episode` step arrays, `is_resolvable`, `make_playlist`, optional `language`, `disabled`.
- Steps support plugin:// URLs and action maps (keyboard input, regex item match, early `return` on season/episode, dialog control). Examples: `netflix.json`, `composite_for_plex.json`, `jellycon.json`, `youtube.json`.
- Available placeholders (Player-Function.md): `{tmdb}`, `{imdb}`, `{tvdb}`, `{trakt}`, `{slug}`, `{name}`, `{title}`, `{year}`, `{season}`, `{episode}`, `{showname}`, etc. TMDbHelper supplies tmdb/imdb/tvdb ids plus title/year/season/episode.
- Loader: `tmdbhelper.lib.player.config.files.PlayerFiles` + `PlayerMeta` read JSON from bundled/user/saved dirs, verify addons enabled, compute priority. Dialog selection via `PlayerItems`/`PlayerDefault`; `is_resolvable=true` uses `setResolvedUrl` flow.
- Playerstring (monitor/scrobbler) carries tmdb_type, tmdb_id/tvshow.tmdb, imdb_id, tvdb_id, season, episode.

## video.kino.pub (addon #1) playback model (current)
- Routes in `src/resources/lib/main.py`.
  - Playback: `plugin://video.kino.pub/play/<item_id>[?season_index=&index=]` → resolves via `ItemsCollection.get_playable` → `Player` (`src/resources/lib/player.py`) using `setResolvedUrl` (is_resolvable=true).
  - Search (non-interactive): `plugin://video.kino.pub/search/<content_type>/results/?title=<q>`; content_type can be `movies`, `serials`, `all`, etc. Query params become `plugin.kwargs` and feed `ItemsCollection.get("items", data)`.
  - Watching list: `/watching/`, etc. (not required for TMDbHelper).
- Models in `src/resources/lib/modeling.py`: movies/episodes identified by KinoPub internal `id`. Episodes use the show `item_id` with `season_index` (1-based) and `index` (1-based episode within season). VideoInfoTag includes `imdbnumber` but no tmdb/tvdb ids.
- No resolver for external ids (tmdb/imdb/tvdb). Matching must use title/year and KinoPub search.

## Historical notes (validated)
- Discussion #203 routes confirmed: search via `/search/<type>/results/?title=...`; play via `/play/<id>?season_index=&index=` requires KinoPub `id` (see Aux doc doc-002).
- Playback uses `setResolvedUrl`; TMDbHelper player can be `is_resolvable=true` once we supply deterministic routes.

## Decisions (no open questions)
1) **External ids**: Not supported in addon #1. Integration will match by title/year (movies) and by show title + season/episode (episodes). Documented; future external-id resolver optional but not required.
2) **Search entrypoint**: Use existing non-interactive search route `/search/<content_type>/results/?title=...` with `content_type=movies` or `serials`. This avoids on-screen keyboard and is backward compatible.
3) **Playback URLs**: Use existing `/play/<item_id>` (movies) and `/play/<item_id>?season_index=&index=` (episodes), 1-based indices. Player JSON will drill down via search results to reach the episode entry when needed.
4) **is_resolvable**: Set to `true` in player JSON because addon #1 uses `setResolvedUrl`.
5) **Fallback**: If direct match fails, fall back to search listing (search_movie/search_episode) so the user can choose; TMDbHelper dialog handles selection per standard behavior.

## Target contract (to implement)
- Player JSON (user-supplied) for TMDbHelper:
  - `plugin`: `video.kino.pub`, `provider`: `kino.pub`, `priority`: moderate (e.g., 200).
  - `assert`: movies require `title`+`year`; episodes require `showname`+`season`+`episode`.
  - `play_movie`: open `plugin://video.kino.pub/search/movies/results/?title={title}&year={year}` then regex match on title/year to play.
  - `play_episode`: open `plugin://video.kino.pub/search/serials/results/?title={showname}` then match show title, season, episode, following Netflix-style steps to open season and episode.
  - `search_movie` / `search_episode`: same URLs without strict matching for fallback.
  - `is_resolvable`: true.
- No TMDbHelper changes required; player JSON to be placed in TMDbHelper user players directory (`special://profile/addon_data/plugin.video.themoviedb.helper/players/`) or shipped in this repo under `integrations/tmdbhelper/players/` for users to copy.

## Next steps alignment
- Implement/stabilize non-interactive search usage and ensure search respects `title` param in addon #1 (minimal code touch, backward compatible).
- Provide the user player JSON file and installation instructions.
- Add regression-safe resolver/matching logic (title/year; season/episode) and document limitations (no external-id matching).
- Create test checklist (movies/episodes, ambiguous titles, auth token refresh).
