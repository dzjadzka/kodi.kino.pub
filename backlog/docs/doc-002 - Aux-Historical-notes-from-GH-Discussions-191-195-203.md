---
id: doc-002
title: 'Aux: Historical notes from GH Discussions (#191/#195/#203)'
type: other
created_date: '2025-12-14 12:59'
updated_date: '2025-12-14 16:58'
---
# Aux: Historical notes from GH Discussions (#191/#195/#203)

Status of historical points (verified/changed/removed):
- VERIFIED: `plugin://video.kino.pub/search/serials/results?title=...` works (see current search route and logs).
- VERIFIED: `plugin://video.kino.pub/play/<id>?season_index=&index=` works with 1-based season/index; used by current player JSON, confirmed in 17:34 log (play/15419?season_index=1&index=1).
- VERIFIED: `watching` endpoint exists (`/watching?id=<id>`), used internally; route still present.
- CHANGED: Episode auto-select now uses season_episodes + play with return step in player JSON; TMDbHelper integration confirmed working in 17:34 log.
- REMOVED: Earlier assumption about needing Container.Update/runplugin for playback; current approach relies on setResolvedUrl.

References to current code/logs:
- Routes: `src/resources/lib/main.py` (`/search/...`, `/seasons/<id>/`, `/season_episodes/<id>/<season>/`, `/play/<id>`)
- Metadata: `src/resources/lib/modeling.py` (Season/SeasonEpisode video_info)
- Log confirmation: 2025-12-14 17:34 session shows direct episode playback after season/episode match.
