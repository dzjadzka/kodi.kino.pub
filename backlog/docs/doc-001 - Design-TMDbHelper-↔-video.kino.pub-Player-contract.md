---
id: doc-001
title: 'Design: TMDbHelper ↔ video.kino.pub Player contract'
type: other
created_date: '2025-12-14 12:44'
updated_date: '2025-12-14 16:58'
---
# Design: TMDbHelper ↔ video.kino.pub Player contract

## Summary / Decision
- TMDbHelper remains read-only; integration is via user player JSON placed in `special://profile/addon_data/plugin.video.themoviedb.helper/players/kino_pub.json`.
- video.kino.pub provides non-interactive routes: `search/movies/results`, `search/serials/results`, `seasons/<id>/`, `season_episodes/<id>/<season>/`, `play/<id>?season_index=&index=`; playback uses `setResolvedUrl` (is_resolvable=true).
- Episode auto-select confirmed in 17:34 log after adding explicit `return` step (season+episode match) in player JSON; no folder navigation.
- Season/Episode metadata available via `Season.video_info` and `SeasonEpisode.video_info` (season, episode, tvshowtitle, duration, playcount) in `src/resources/lib/modeling.py`; no changes required.
- Installer route in addon copies player JSON into TMDbHelper userdata; service runs on login to ensure presence. If missing, fallback is manual copy.

## Player JSON (user-installed)
Path in repo: `integrations/tmdbhelper/players/kino_pub.json`
Key fields:
- `plugin`: video.kino.pub; `priority`: 200; `is_resolvable`: true
- `assert`: movies need title+year; episodes need showname+season+episode
- `play_movie`: `plugin://video.kino.pub/search/movies/results/?title={title_url}&year={year}` → match title/year
- `play_episode` steps (final):
  1) `plugin://video.kino.pub/search/serials/results/?title={showname_url}`
  2) match show title `(.*{showname}.*)`
  3) match season `{season}`
  4) **return** on season+episode match (`{season}`, `{episode}`)
  5) regex fallback on label `s0*{season}e0*{episode}`
  6) regex fallback on title `s0*{season}e0*{episode}`
- `fallback`: play_episode → search_episode; play_movie → search_movie

## Verification (logs)
- 17:34 session: TMDbHelper selected KinoPub, executed search→seasons→season_episodes→play with `season_index=1&index=1`, then playback started without folder navigation; log shows “lib.player - Play with KinoPub: Resolving… kino_pub.json play_episode” and no further Container.Update beyond the intended search.
- Earlier failures (dummy.mp4) were due to missing player JSON or missing return step; both addressed.

## Open items
- None; episode autoselect works with current player JSON and existing metadata.

## References
- Code: `src/resources/lib/modeling.py` (Season/SeasonEpisode video_info), `src/resources/lib/main.py`, `src/resources/lib/tmdbhelper_installer.py`
- Player JSON: `integrations/tmdbhelper/players/kino_pub.json`
- Log: 2025-12-14 17:34 run confirms success.
