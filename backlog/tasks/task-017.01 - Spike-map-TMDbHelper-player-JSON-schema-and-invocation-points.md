---
id: task-017.01
title: 'Spike: map TMDbHelper player JSON schema and invocation points'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
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
Analyze TMDbHelper player system: how players JSON are loaded, required keys, available item data, invocation flows (dialog selection, default player, combined players), and playback launch methods (plugin://, search/play modes). Capture findings and gaps for using video.kino.pub as a player.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Notes list player JSON keys, assert/fallback/is_resolvable behavior, and step execution model with examples (e.g., netflix/composite/jellycon/youtube)
- [ ] #2 Entry points documented: where player JSON is read (PlayerFiles/PlayerMeta), how selection dialog works, and what data keys TMDbHelper supplies (tmdb/imdb/tvdb/title/year/season/episode)
- [ ] #3 Launch methods enumerated (plugin:// URLs, keyboard/dialog actions, setResolvedUrl expectations) with file/function references
- [ ] #4 Open questions or risks for integrating video.kino.pub recorded in task notes
<!-- AC:END -->
