---
id: task-017.04
title: 'Spec: TMDbHelper player JSON for video.kino.pub'
status: Done
assignee: []
created_date: '2025-12-14 12:45'
updated_date: '2025-12-14 16:57'
labels:
  - kodi
  - tmdbhelper
  - player
  - spec
dependencies:
  - task-017.03
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Draft user player JSON for TMDbHelper to call video.kino.pub using the agreed contract. Store JSON in repo (e.g., integrations/tmdbhelper/players/kino_pub.json) for users to copy into TMDbHelper userdata; no TMDbHelper code changes.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Player JSON written with plugin id video.kino.pub, provider kino.pub, priority (~200), is_resolvable=true
- [ ] #2 Asserts set: play_movie requires title+year; play_episode requires showname+season+episode; search variants use title/showname
- [ ] #3 Steps use non-interactive URLs `/search/movies/results/?title={title}&year={year}` and `/search/serials/results/?title={showname}` with regex matching and season/episode traversal; fallback search entries provided
- [ ] #4 Notes include install path (`special://profile/addon_data/plugin.video.themoviedb.helper/players/`) and any limitations (no external-id lookup)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Player JSON finalized with sequential season→episode steps and early return when season/episode match; tested in 17:34 log: TMDbHelper resolves episode without opening folders.
<!-- SECTION:NOTES:END -->
