---
id: task-017.02
title: 'Spike: determine video.kino.pub playable URL contract and search capabilities'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
updated_date: '2025-12-14 13:00'
labels:
  - kodi
  - player
  - analysis
dependencies: []
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Determine video.kino.pub playable URL contract and search capabilities from current code. Confirm machine-callable routes (/play/<id>, /search/<type>/results/?title=) and parameter expectations, indices, and identifier availability. No open questions left; document safe defaults.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Document playback URLs and params for movies/episodes (1-based season_index/index) with file references in main.py/modeling.py/player.py
- [ ] #2 List available identifiers (internal id required; imdbnumber present; no tmdb/tvdb) and state that external ids are unsupported
- [ ] #3 Confirm non-interactive search route `/search/<content_type>/results/?title=` works and note recommended content_type values (movies, serials); record limitations
- [ ] #4 Record decisions for matching strategy (title/year; showname+season+episode) and fallback behavior; no open questions
<!-- AC:END -->
