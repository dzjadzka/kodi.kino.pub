---
id: task-017.01
title: 'Spike: map TMDbHelper player JSON schema and invocation points'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
updated_date: '2025-12-14 13:00'
labels:
  - kodi
  - tmdbhelper
  - player
  - analysis
dependencies: []
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Map TMDbHelper player JSON schema and invocation points (read-only): document keys, placeholders, step model, player selection, and launch methods, confirming current behavior for user players. Use findings to keep contract deterministic (no code changes to TMDbHelper).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Notes list player JSON keys, assert/fallback/is_resolvable behavior, step execution model with examples (netflix, composite_for_plex, jellycon, youtube)
- [ ] #2 Document where player JSON is read (PlayerFiles/PlayerMeta), how selection dialog works (PlayerItems/PlayerDefault), and supplied data keys (tmdb/imdb/tvdb/title/year/season/episode)
- [ ] #3 Enumerate launch methods (plugin:// URLs, keyboard/dialog actions, setResolvedUrl expectations) with file/function references
- [ ] #4 Confirm user player path (`special://profile/addon_data/plugin.video.themoviedb.helper/players/`) and success/failure handling; no open questions left
<!-- AC:END -->
