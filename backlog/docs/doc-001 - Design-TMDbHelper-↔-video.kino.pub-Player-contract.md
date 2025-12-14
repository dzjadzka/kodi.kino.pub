---
id: doc-001
title: 'Design: TMDbHelper ↔ video.kino.pub Player contract'
type: other
created_date: '2025-12-14 12:44'
updated_date: '2025-12-14 15:05'
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
- Models in `src/resources/lib/modeling.py`: movies/episodes identified by KinoPub internal `id`. Episodes use the show `item_id` with `season_index` (1-based) and `index` (1-based episode within season). VideoInfoTag includes `season`, `episode`, `tvshowtitle`, `imdbnumber`; no tmdb/tvdb ids.
- No resolver for external ids (tmdb/imdb/tvdb). Matching must use title/year and KinoPub search.

## Historical notes (validated)
- Discussion #203 routes confirmed: search via `/search/<type>/results/?title=...`; play via `/play/<id>?season_index=&index=` requires KinoPub `id` (see Aux doc doc-002).
- Playback uses `setResolvedUrl`; TMDbHelper player can be `is_resolvable=true` once we supply deterministic routes.

## Decisions (no open questions)
1) **External ids**: Not supported in addon #1. Integration uses title/year (movies) and show title + season/episode (episodes). Future external-id resolver optional.
2) **Search entrypoint**: Use existing non-interactive search route `/search/<content_type>/results/?title=...` with `content_type=movies` or `serials`. URL-encode titles (`{title_url}`, `{showname_url}`) to avoid keyboard prompts.
3) **Playback URLs**: Use existing `/play/<item_id>` (movies) and `/play/<item_id>?season_index=&index=` (episodes), 1-based indices. Player JSON drills down via search results to reach season/episode entries.
4) **is_resolvable**: Set to `true` in player JSON because addon #1 uses `setResolvedUrl`.
5) **Fallback**: If matching fails at any step, fall back to search listing so the user can pick manually; movies unaffected.
6) **Metadata requirement**: Season/episode listitems must expose `season` and `episode` infolabels (already set in `modeling.py` video_info). TMDbHelper matches on these values during navigation.

## Target contract (implemented for player JSON)
- Player JSON (user-supplied) for TMDbHelper:
  - `plugin`: `video.kino.pub`, `provider`: `kino.pub`, `priority`: ~200.
  - `assert`: movies require `title`+`year`; episodes require `showname`+`season`+`episode`.
  - `play_movie`: `plugin://video.kino.pub/search/movies/results/?title={title_url}&year={year}` → regex match on title/year.
  - `play_episode`: `plugin://video.kino.pub/search/serials/results/?title={showname_url}` → match show title → match season `{season}` → match episode `{episode}` (and regex `s0*{season}e0*{episode}` as fallback) → play.
  - `search_movie` / `search_episode`: same URLs (encoded) without strict matching for fallback.
  - `is_resolvable`: true.
- User installs JSON into TMDbHelper userdata: `special://profile/addon_data/plugin.video.themoviedb.helper/players/` (not shipped in TMDbHelper repo).

## Next steps alignment
- Validate listitem metadata for seasons/episodes (should already provide season/episode numbers via `modeling.py`). Fix minimally if any gaps appear in logs.
- Keep regression-safe: movie flow unchanged; search route remains backward compatible.
- Test checklist in `docs/tmdbhelper-integration-testing.md` for movies/episodes, localized titles, ambiguous matches, season/episode >1; logs should show search URL, auto-selection, and `setResolvedUrl`.
