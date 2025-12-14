---
id: task-017.10
title: Verify listitem season/episode metadata for TMDbHelper matching
status: To Do
assignee: []
created_date: '2025-12-14 15:05'
labels:
  - kodi
  - player
  - qa
dependencies:
  - task-017.02
  - task-017.05
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Confirm video.kino.pub emits season/episode info in listitems (seasons and episodes) so TMDbHelper player steps can match and auto-select. Add minimal fixes if any fields missing.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Listitem metadata for seasons and episodes verified from code/logs (season, episode, tvshowtitle) and noted with file references
- [ ] #2 If gaps exist, minimal backward-compatible fix implemented in video.kino.pub to set season/episode infolabels
- [ ] #3 Result documented in task notes and referenced in doc-001
<!-- AC:END -->
