---
id: task-017.06
title: 'Design: TMDbHelper player UX/settings for video.kino.pub'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
updated_date: '2025-12-14 13:00'
labels:
  - kodi
  - tmdbhelper
  - player
  - ux
dependencies:
  - task-017.03
  - task-017.04
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Define TMDbHelper player UX/settings for video.kino.pub: priority/provider choice, messaging when addon/auth missing, and any addon #1 toggles (if needed). No TMDbHelper changes.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Document chosen priority/provider and how player appears in TMDbHelper (combined vs separate players)
- [ ] #2 Define behavior when video.kino.pub not installed or user not authenticated (expected TMDbHelper dialog + addon’s own errors)
- [ ] #3 State whether addon #1 needs a setting to enable/disable TMDbHelper integration (default off unless proven unnecessary); if not needed, document decision
- [ ] #4 Update doc-001 notes with UX decisions and fallback messaging
<!-- AC:END -->
