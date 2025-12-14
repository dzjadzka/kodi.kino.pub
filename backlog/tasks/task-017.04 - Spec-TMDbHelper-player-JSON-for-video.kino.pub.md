---
id: task-017.04
title: 'Spec: TMDbHelper player JSON for video.kino.pub'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
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
Draft the TMDbHelper player JSON definition for video.kino.pub including assert keys, play/search steps, resolvable flag, provider/priority, and any fallback behavior. Ready for future implementation once resolver routes are available.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 JSON skeleton written and stored in notes/doc with fields filled (name, plugin id video.kino.pub, priority/provider, assert, play_movie/play_episode/search variants, is_resolvable)
- [ ] #2 Steps align with agreed contract (parameters for movie and episode) and avoid unsupported flows (e.g., no interactive keyboard if route supports query params)
- [ ] #3 Fallback behavior defined (e.g., switch to search mode if direct resolve fails)
- [ ] #4 Open issues (e.g., missing resolver route) explicitly called out
<!-- AC:END -->
