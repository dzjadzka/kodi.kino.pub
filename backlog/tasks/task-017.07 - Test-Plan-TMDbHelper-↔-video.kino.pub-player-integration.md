---
id: task-017.07
title: 'Test Plan: TMDbHelper ↔ video.kino.pub player integration'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
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
Define test coverage for the integration: unit/integration/manual flows to validate player JSON, resolver route, movie vs episode playback, error handling, and regression on existing kino.pub playback.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 List manual test cases: movie play via TMDbHelper -> kino.pub, episode play with season/episode, no-match handling, auth/token expired handling
- [ ] #2 Identify any automated test hooks (if feasible) or note if manual-only; include existing kino.pub test harness constraints
- [ ] #3 Regression checks noted to ensure default kino.pub UI playback unaffected
- [ ] #4 Test plan captured in task notes and linked to contract doc
<!-- AC:END -->
