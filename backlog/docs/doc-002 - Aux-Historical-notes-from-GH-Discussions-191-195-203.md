---
id: doc-002
title: 'Aux: Historical notes from GH Discussions (#191/#195/#203)'
type: other
created_date: '2025-12-14 12:59'
---
# Aux: Historical notes from GH Discussions (#191/#195/#203)

## Discussion #191 (watching / Container.Update / RunAddon)
- Claim: playback could be triggered via `plugin://video.kino.pub/watching/` or `Container.Update`/`RunAddon` flows.
- Status: VERIFIED. Current code has route `/watching/` in `src/resources/lib/main.py` (lists in-progress TV shows). Playbacks still go through `setResolvedUrl` in `main.py` → `Player`.

## Discussion #195 (library integration request)
- Claim: maintainer wasn’t planning to implement library integration; expectation is community-driven changes.
- Status: VERIFIED (contextual). Matches current scope: no library/TMDbHelper integration present; we must add integration on addon #1 side only.

## Discussion #203 (search/play plugin URLs needing KinoPub REST id)
- Claim: plugin:// routes usable:
  - search: `plugin://video.kino.pub/search/<type>/results/?title=<name>`
  - play: `plugin://video.kino.pub/play/<id>?season_index=<num>&index=<num>`; requires KinoPub internal `id`.
- Status: VERIFIED. Current routes in `src/resources/lib/main.py`:
  - `/search/<content_type>/results/` consumes query params (`title` etc.) via `plugin.kwargs` and calls ItemsCollection search.
  - `/play/<item_id>` accepts optional `season_index` and `index` (1-based) and resolves playback via `ItemsCollection.get_playable` + `Player` using `setResolvedUrl`.
- Note: No external-id (tmdb/imdb) resolver exists; integration must resolve to KinoPub `id` via search/matching.
