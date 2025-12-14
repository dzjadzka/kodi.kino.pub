---
id: task-017.07
title: 'Test Plan: TMDbHelper ↔ video.kino.pub player integration'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
updated_date: '2025-12-14 13:00'
labels:
  - kodi
  - tmdbhelper
  - player
  - testing
dependencies:
  - task-017.04
  - task-017.05
  - task-017.06
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Define test coverage for TMDbHelper ↔ video.kino.pub integration using the agreed contract. Focus on manual cases (movies/episodes) and regressions ensuring existing addon #1 playback is unaffected.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Manual test checklist includes: play_movie via TMDbHelper using new player JSON; play_episode with season/episode; no-match/ambiguous title fallback; auth/token expiry handling
- [ ] #2 Note whether automation is feasible; if not, mark manual-only and reference existing test harness limits
- [ ] #3 Regression checks listed to ensure default video.kino.pub UI playback and search remain intact
- [ ] #4 Test plan captured in task notes and linked to doc-001
<!-- AC:END -->
