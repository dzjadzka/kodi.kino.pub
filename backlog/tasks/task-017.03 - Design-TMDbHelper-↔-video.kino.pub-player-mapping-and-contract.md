---
id: task-017.03
title: 'Design: TMDbHelper ↔ video.kino.pub player mapping and contract'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
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
Propose the player contract between TMDbHelper and video.kino.pub: required asserts/keys, URL schema or route additions for direct play/search, matching rules for movie vs episode, and fallback/ambiguity handling. Align with Design doc doc-001.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Contract doc updated (doc-001) with concrete URL/route proposal for movie and episode playback and expected parameters
- [ ] #2 Defines assert keys and TMDbHelper step flow (play vs search) for the new player JSON
- [ ] #3 Outlines matching heuristics (title/year, season/episode) and ambiguity fallback behavior
- [ ] #4 Lists open questions and decisions needed from API capabilities and validates dependencies
<!-- AC:END -->
