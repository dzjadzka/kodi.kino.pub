---
id: task-017.03
title: 'Design: TMDbHelper ↔ video.kino.pub player mapping and contract'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
updated_date: '2025-12-14 13:00'
labels:
  - kodi
  - tmdbhelper
  - player
  - design
dependencies:
  - task-017.01
  - task-017.02
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Finalize player contract between TMDbHelper and video.kino.pub using existing routes. Define asserts, URL schema, matching rules, and fallback behavior per doc-001 decisions; no TMDbHelper changes.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Doc-001 updated with finalized contract (URLs, asserts, is_resolvable=true, matching rules) and decisions (no external-id support; title/year and season/episode matching)
- [ ] #2 Defines play_movie/play_episode/search flows using `/search/<type>/results/?title=` and `/play/<id>[?season_index=&index=]` with 1-based indices
- [ ] #3 Fallback behavior documented (search listing if match fails) and ambiguity handling defined
- [ ] #4 No open questions remain; references to code files included
<!-- AC:END -->
