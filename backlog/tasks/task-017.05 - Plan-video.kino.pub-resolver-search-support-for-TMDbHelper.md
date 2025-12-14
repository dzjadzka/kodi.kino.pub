---
id: task-017.05
title: 'Plan: video.kino.pub resolver/search support for TMDbHelper'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
labels:
  - kodi
  - player
  - design
dependencies:
  - task-017.02
  - task-017.03
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Outline required changes in video.kino.pub to support TMDbHelper playback: new route(s) to accept external ids/title/year/season/episode, resolve to internal item_id, and redirect to /play. Include API lookup strategy and token/auth considerations.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Proposed route signatures and parameters documented (e.g., plugin://video.kino.pub/play_resolve?title=...&year=...&season=...&episode=...&imdb=...)
- [ ] #2 Lookup algorithm defined (search endpoints, matching heuristics, handling multiple results) with references to existing API calls
- [ ] #3 Error/edge handling described (no match, multiple matches, auth failures), including user messaging plan
- [ ] #4 Risks noted (lack of external-id support in KinoPub API) with mitigation options or spikes
<!-- AC:END -->
