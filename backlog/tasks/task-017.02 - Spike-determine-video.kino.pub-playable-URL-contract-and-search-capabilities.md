---
id: task-017.02
title: 'Spike: determine video.kino.pub playable URL contract and search capabilities'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
labels:
  - kodi
  - player
  - analysis
dependencies: []
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Investigate how video.kino.pub resolves playback: existing routes/params (/play/<item_id>, season_index/index), search flows, whether queries can be provided non-interactively, and availability of external ids (imdb/tmdb/tvdb) in data models. Identify gaps for TMDbHelper integration.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Document current playback URLs and required params for movies/episodes (including season_index/index handling) with file references
- [ ] #2 List available identifiers in item metadata (imdbnumber, titles, year) and note absence of tmdb/tvdb mapping
- [ ] #3 Clarify search entry points and whether programmatic search input exists; note any limitations
- [ ] #4 Record open questions about API support for searching by external ids and propose options to investigate
<!-- AC:END -->
