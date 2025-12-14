# TMDbHelper ↔ video.kino.pub integration testing

## Install player JSON
- Copy `integrations/tmdbhelper/players/kino_pub.json` to `special://profile/addon_data/plugin.video.themoviedb.helper/players/` (Kodi profile).
- Ensure `video.kino.pub` add-on is installed and authorized (device code login).

## Expected play flow (episodes)
1. TMDbHelper opens `plugin://video.kino.pub/search/serials/results/?title=<showname>`.
2. Listitem matching the show title is selected automatically.
3. Season list: selects season matching `{season}` (1-based).
4. Episodes list: selects episode matching `{episode}` and starts playback via `setResolvedUrl`.
5. If matching fails at any step, TMDbHelper falls back to showing the listing (user can pick manually).

## What to watch in kodi.log
- Look for TMDbHelper player steps calling the above URLs.
- Confirm listitem matches using `season`/`episode` infolabels; on success the log should show navigation into season and episode, followed by `setResolvedUrl` from video.kino.pub.
- Failures: no match on show/season/episode → expect remaining in listing; verify regex `s0*<season>e0*<episode>` if needed.

## Manual checklist
- Single-match show (e.g., unique title), play S01E01 → should auto-play.
- Localized title (Cyrillic) → ensure regex match on show title works; play S01E01.
- Ambiguous title (multiple matches) → expect fallback to listing; manual selection still works.
- Season > 1 and episode > 1 → ensure 1-based indices select correct episode.
- Regression: play a movie via TMDbHelper with the same player; ensure normal playback. Also confirm native video.kino.pub UI playback/search unaffected.
